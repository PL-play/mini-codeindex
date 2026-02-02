from __future__ import annotations

import asyncio
import fnmatch
import json
import hashlib
import logging
import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Iterable, Iterator, List, Optional, Sequence

from .chunking import Chunk, Config as ChunkConfig, TreeSitterChunker, format_scope, ScopeKind
from .db import VectorStore
from .embedding import Embedder
from .logging_utils import setup_logging

logger = logging.getLogger(__name__)


def _hash_file_sha256_sync(path: str) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            hasher.update(block)
    return hasher.hexdigest()


async def _hash_file_sha256(path: str) -> str:
    return await asyncio.to_thread(_hash_file_sha256_sync, path)


def _new_id() -> str:
    return uuid.uuid4().hex


_BINARY_EXTENSIONS = {
    # Images
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".bmp",
    ".tiff",
    # Archives / compressed
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
    ".zst",
    # Media
    ".mp3",
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".wav",
    ".flac",
    # Binaries / artifacts
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".a",
    ".o",
    ".obj",
    ".class",
    ".jar",
    ".pyc",
    ".pyo",
    ".whl",
    ".pdf",
}


def _is_probably_text_file_sync(
    path: str, *, chunk_cfg: ChunkConfig, sample_size: int = 8192
) -> bool:
    """Heuristic filter to skip binary files.

    We keep this simple and fast:
    - common binary extensions
    - NUL byte check
    - best-effort decode using configured encoding (or charset-normalizer in _auto)
    - control-character ratio heuristic
    """

    ext = os.path.splitext(path)[1].lower()
    if ext in _BINARY_EXTENSIONS:
        return False

    try:
        with open(path, "rb") as f:
            sample = f.read(sample_size)
    except OSError:
        return False

    if not sample:
        return True
    if b"\x00" in sample:
        return False

    # Decode probe.
    encoding = chunk_cfg.encoding
    if encoding == "_auto":
        try:
            from charset_normalizer import from_bytes

            match = from_bytes(sample).best()
            if match is None or match.encoding is None:
                return False
            encoding = match.encoding
        except Exception:
            return False

    try:
        sample.decode(encoding)
    except Exception:
        return False

    # Textiness heuristic: reject when too many control bytes.
    ctrl = 0
    for b in sample:
        if b in (9, 10, 13):
            continue
        if b < 32 or b == 127:
            ctrl += 1
    if ctrl / len(sample) > 0.30:
        return False

    return True


async def _is_probably_text_file(
    path: str, *, chunk_cfg: ChunkConfig, sample_size: int = 8192
) -> bool:
    return await asyncio.to_thread(
        _is_probably_text_file_sync, path, chunk_cfg=chunk_cfg, sample_size=sample_size
    )


@dataclass
class IndexConfig:
    """Configuration for an indexing run.

    This is intentionally minimal. We'll extend it as you decide on metadata,
    filtering, and update strategy.
    """

    root_dir: str

    recursive: bool = True
    include_hidden: bool = False

    include_globs: List[str] = field(default_factory=lambda: ["**/*"])
    exclude_globs: List[str] = field(
        default_factory=lambda: [
            "**/.git/**",
            "**/.venv/**",
            "**/__pycache__/**",
            "**/.pytest_cache/**",
            "**/chroma_data/**",
        ]
    )

    # When True, we still do chunk+embed, but we don't write to the backend.
    dry_run: bool = True


@dataclass
class IndexStats:
    files_seen: int = 0
    files_indexed: int = 0
    chunks_emitted: int = 0


def iter_candidate_files(cfg: IndexConfig) -> Iterator[str]:
    root = os.path.abspath(cfg.root_dir)

    def matches_any(rel_posix: str, patterns: list[str]) -> bool:
        """Match a posix-style relative path against glob-like patterns.

        Notes:
        - We use `fnmatch` for simplicity.
        - Treat a leading '**/' as optional so patterns like '**/*' also match
          root-level files (e.g. 'a.py').
        """

        for pat in patterns:
            if fnmatch.fnmatch(rel_posix, pat):
                return True
            if pat.startswith("**/") and fnmatch.fnmatch(rel_posix, pat[3:]):
                return True
        return False

    def is_hidden_path(p: str) -> bool:
        parts = os.path.relpath(p, root).split(os.sep)
        return any(part.startswith(".") for part in parts if part not in (".", ".."))

    if cfg.recursive:
        for dirpath, dirnames, filenames in os.walk(root):
            if not cfg.include_hidden:
                dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for name in filenames:
                path = os.path.join(dirpath, name)
                if not cfg.include_hidden and is_hidden_path(path):
                    continue

                rel = os.path.relpath(path, root).replace(os.sep, "/")
                if matches_any(rel, cfg.exclude_globs):
                    continue
                if not matches_any(rel, cfg.include_globs):
                    continue

                if os.path.isfile(path):
                    yield path
    else:
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isfile(path):
                rel = os.path.relpath(path, root).replace(os.sep, "/")
                if matches_any(rel, cfg.exclude_globs):
                    continue
                if not matches_any(rel, cfg.include_globs):
                    continue
                yield path


def _build_chunk_metadata(
    *,
    chunk: Chunk,
    file_path: str,
    file_sha256: str,
    rel_path: str,
    chunk_kind: str = "code",
) -> dict[str, Any]:
    def scope_to_dict(scope: Any) -> dict[str, Any]:
        return {
            "kind": getattr(scope.kind, "value", str(scope.kind)),
            "name": scope.name,
            "raw_type": scope.raw_type,
            "rel_path": getattr(scope, "rel_path", None),
        }

    scope_path_list = [scope_to_dict(s) for s in chunk.scope_path]
    contained_scopes_list = [scope_to_dict(s) for s in chunk.contained_scopes]
    scope_path_str = " -> ".join(format_scope(s) for s in chunk.scope_path)
    contained_scopes_str = ", ".join(format_scope(s) for s in chunk.contained_scopes)
    symbol_names = [s.name for s in chunk.scope_path if getattr(s, "name", None)]
    scope_signature = " -> ".join(
        f"{getattr(s.kind, 'value', s.kind)} {s.name}" for s in chunk.scope_path
    )

    meta: dict[str, Any] = {
        "path": file_path,
        "relpath": rel_path,
        "sha256": file_sha256,
        "created_at": int(time.time()),
        "chunk_kind": chunk_kind,
        "scope_path": json.dumps(scope_path_list, ensure_ascii=False),
        "contained_scopes": json.dumps(contained_scopes_list, ensure_ascii=False),
        "scope_path_str": scope_path_str,
        "contained_scopes_str": contained_scopes_str,
        "scope_depth": len(chunk.scope_path),
        "symbol_names": json.dumps(symbol_names, ensure_ascii=False),
        "scope_signature": scope_signature,
        "contained_scope_count": len(chunk.contained_scopes),
    }
    if chunk.start is not None:
        meta["start_line"] = int(getattr(chunk.start, "row", 0))
        meta["start_col"] = int(getattr(chunk.start, "column", 0))
    if chunk.end is not None:
        meta["end_line"] = int(getattr(chunk.end, "row", 0))
        meta["end_col"] = int(getattr(chunk.end, "column", 0))
    scope_start = getattr(chunk, "scope_start", None)
    scope_end = getattr(chunk, "scope_end", None)
    if scope_start is not None:
        meta["scope_start_line"] = int(getattr(scope_start, "row", 0))
        meta["scope_start_col"] = int(getattr(scope_start, "column", 0))
    if scope_end is not None:
        meta["scope_end_line"] = int(getattr(scope_end, "row", 0))
        meta["scope_end_col"] = int(getattr(scope_end, "column", 0))
    if getattr(chunk, "group_id", None) is not None:
        meta["group_id"] = chunk.group_id
    if getattr(chunk, "group_index", None) is not None:
        meta["group_index"] = int(chunk.group_index)
    if chunk.language is not None:
        meta["language"] = chunk.language
    return meta


def _expand_chunks(*, chunks: list[Chunk], file_path: str, rel_path: str) -> list[tuple[Chunk, str]]:
    expanded: list[tuple[Chunk, str]] = [(c, "code") for c in chunks]

    def _attach_source(meta_chunk: Chunk, *, source: Chunk | None) -> Chunk:
        meta_chunk.path = file_path
        if source is not None:
            meta_chunk.sha256 = source.sha256
            meta_chunk.language = source.language
            meta_chunk.scope_path = list(source.scope_path)
            meta_chunk.contained_scopes = list(source.contained_scopes)
            meta_chunk.start = source.start
            meta_chunk.end = source.end
        return meta_chunk

    rel_chunk = _attach_source(Chunk(text=f"relpath: {rel_path}"), source=chunks[0] if chunks else None)
    expanded.append((rel_chunk, "relpath"))

    for source in chunks:
        if len(source.scope_path) <= 1:
            continue
        scope_path_str = " -> ".join(format_scope(s) for s in source.scope_path)
        if not scope_path_str:
            continue
        containers_str = ", ".join(format_scope(s) for s in source.contained_scopes)
        suffix = f" | containers: {containers_str}" if containers_str else ""
        scope_chunk = _attach_source(
            Chunk(text=f"scope_path: {scope_path_str}{suffix}"),
            source=source,
        )
        expanded.append((scope_chunk, "scope_path"))

    kind_counts: dict[str, int] = {}
    for _, kind in expanded:
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
    kind_summary = ", ".join(f"{k}={v}" for k, v in sorted(kind_counts.items()))
    logger.info(
        "[EXPAND] file=%s base=%d expanded=%d added=%d types: %s",
        file_path,
        len(chunks),
        len(expanded),
        max(0, len(expanded) - len(chunks)),
        kind_summary,
    )

    return expanded


def _prepare_chunks_for_file_sync(
    *,
    file_path: str,
    rel_path: str,
    file_sha256: str,
    chunk_cfg: ChunkConfig,
) -> list[tuple[Chunk, str]]:
    chunker = TreeSitterChunker(chunk_cfg)
    chunks: List[Chunk] = list(chunker.chunk(file_path))
    if not chunks:
        return []

    for c in chunks:
        c.path = file_path
        c.sha256 = file_sha256

    if chunk_cfg.mode in {"type", "function"}:
        def _scope_group_key(c: Chunk) -> Optional[tuple]:
            if not c.scope_path:
                return None
            last = c.scope_path[-1]
            if getattr(last, "kind", None) not in {ScopeKind.TYPE, ScopeKind.FUNCTION}:
                return None
            start = getattr(last, "start", None)
            end = getattr(last, "end", None)
            return (
                getattr(last.kind, "value", str(last.kind)),
                getattr(last, "name", None),
                getattr(last, "raw_type", None),
                getattr(start, "row", None),
                getattr(start, "column", None),
                getattr(end, "row", None),
                getattr(end, "column", None),
            )

        groups: dict[tuple, list[Chunk]] = {}
        for c in chunks:
            key = _scope_group_key(c)
            if key is None:
                continue
            groups.setdefault(key, []).append(c)

        for key, items in groups.items():
            if len(items) <= 1:
                continue
            if all(getattr(c, "group_id", None) is not None for c in items):
                continue
            group_id = uuid.uuid4().hex
            items_sorted = sorted(
                items,
                key=lambda c: (
                    getattr(c.start, "row", 0) if c.start else 0,
                    getattr(c.start, "column", 0) if c.start else 0,
                ),
            )
            for idx, c in enumerate(items_sorted):
                if getattr(c, "group_id", None) is None:
                    c.group_id = group_id
                if getattr(c, "group_index", None) is None:
                    c.group_index = idx

    return _expand_chunks(chunks=chunks, file_path=file_path, rel_path=rel_path)


async def _prepare_chunks_for_file(
    *,
    file_path: str,
    rel_path: str,
    file_sha256: str,
    chunk_cfg: ChunkConfig,
) -> list[tuple[Chunk, str]]:
    return await asyncio.to_thread(
        _prepare_chunks_for_file_sync,
        file_path=file_path,
        rel_path=rel_path,
        file_sha256=file_sha256,
        chunk_cfg=chunk_cfg,
    )


def _build_upsert_payloads(
    *,
    expanded_chunks: list[tuple[Chunk, str]],
    file_path: str,
    file_sha256: str,
    rel_path: str,
) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    texts = [c.text for c, _ in expanded_chunks]
    ids = [_new_id() for _ in expanded_chunks]
    metadatas: list[dict[str, Any]] = []
    for c, kind in expanded_chunks:
        metadatas.append(
            _build_chunk_metadata(
                chunk=c,
                file_path=file_path,
                file_sha256=file_sha256,
                rel_path=rel_path,
                chunk_kind=kind,
            )
        )
    return texts, ids, metadatas


async def index_directory(
    *,
    cfg: IndexConfig,
    chunk_cfg: Optional[ChunkConfig] = None,
    embedder: Optional[Embedder] = None,
    store: Optional[VectorStore] = None,
    force_upsert: bool = False,
    batch_size: int = 16,
    max_concurrency: int = 4,
) -> IndexStats:
    """Index a directory end-to-end (scan -> chunk -> embed -> write).

    Current status: framework only.
    - We implement scan + chunk + embed batching.
    - We only write if cfg.dry_run is False AND store is provided.
    """

    setup_logging()
    stats = IndexStats()
    chunk_cfg = chunk_cfg or ChunkConfig()

    index_start_time = time.time()
    logger.info("=" * 80)
    logger.info(
        "INDEXING START: root=%s | mode=%s | chunk_size=%s | overlap=%s | dry_run=%s",
        cfg.root_dir,
        chunk_cfg.mode,
        chunk_cfg.chunk_size,
        chunk_cfg.overlap_ratio,
        cfg.dry_run,
    )

    if not cfg.dry_run and store is None:
        raise ValueError("store is required when dry_run=False")

    file_paths = list(iter_candidate_files(cfg))
    stats.files_seen = len(file_paths)

    semaphore = asyncio.Semaphore(max_concurrency)
    store_lock = asyncio.Lock()

    async def _process_file(file_path: str) -> tuple[int, int]:
        async with semaphore:
            logger.debug("Scanning file: %s", file_path)

            if not await _is_probably_text_file(file_path, chunk_cfg=chunk_cfg):
                logger.debug("Skipping non-text file: %s", file_path)
                return 0, 0

            try:
                file_sha256 = await _hash_file_sha256(file_path)
            except OSError:
                return 0, 0

            rel_path = os.path.relpath(file_path, cfg.root_dir).replace(os.sep, "/")
            file_start_time = time.time()
            logger.info("---\n[FILE] Processing: %s", file_path)

            if not cfg.dry_run:
                if embedder is None:
                    raise ValueError("embedder is required when dry_run=False")
                assert store is not None

                async with store_lock:
                    existing = await store.get_one_by_path(path=file_path)
                existing_sha = existing.get("sha256") if isinstance(existing, dict) else None

                if not force_upsert and existing_sha == file_sha256 and existing is not None:
                    file_elapsed = time.time() - file_start_time
                    logger.info(
                        "[SKIP] Unchanged (sha256 match). elapsed=%.2fs\n",
                        file_elapsed,
                    )
                    return 0, 0

                if existing is not None:
                    async with store_lock:
                        await store.delete_by_path(path=file_path)
                    if force_upsert and existing_sha == file_sha256:
                        logger.info(
                            "[UPDATE] Force reindex: deleted existing vectors for: %s",
                            file_path,
                        )
                    else:
                        logger.info("[UPDATE] Deleted existing vectors for: %s", file_path)
                else:
                    logger.info("[UPDATE] No existing vectors found for: %s", file_path)

            expanded_chunks = await _prepare_chunks_for_file(
                file_path=file_path,
                rel_path=rel_path,
                file_sha256=file_sha256,
                chunk_cfg=chunk_cfg,
            )
            if not expanded_chunks:
                logger.debug("No chunks emitted for: %s", file_path)
                return 0, 0

            base_chunks = sum(1 for _, kind in expanded_chunks if kind == "code")
            expanded_total = len(expanded_chunks)
            expansion_ratio = (expanded_total / base_chunks) if base_chunks else 0.0
            chunk_lengths = [len(c.text) for c, _ in expanded_chunks]
            total_chars = sum(chunk_lengths)
            min_chars = min(chunk_lengths) if chunk_lengths else 0
            max_chars = max(chunk_lengths) if chunk_lengths else 0
            avg_chars = int(total_chars / expanded_total) if expanded_total else 0
            logger.info(
                "[CHUNKING] base=%d expanded=%d ratio=%.2f chars(min/avg/max)=%d/%d/%d",
                base_chunks,
                expanded_total,
                expansion_ratio,
                min_chars,
                avg_chars,
                max_chars,
            )

            chunk_types_count = {}
            chunk_kind_lengths: dict[str, list[int]] = {}
            for chunk, chunk_kind in expanded_chunks:
                chunk_types_count[chunk_kind] = chunk_types_count.get(chunk_kind, 0) + 1
                chunk_kind_lengths.setdefault(chunk_kind, []).append(len(chunk.text))

            chunk_type_str = ", ".join(
                [f"{k}={v}" for k, v in sorted(chunk_types_count.items())]
            )
            logger.info(
                "[CHUNKING] Chunks emitted: %d total | Types: %s",
                len(expanded_chunks),
                chunk_type_str,
            )
            for kind, lengths in sorted(chunk_kind_lengths.items()):
                if not lengths:
                    continue
                kind_min = min(lengths)
                kind_max = max(lengths)
                kind_avg = int(sum(lengths) / len(lengths))
                logger.info(
                    "[CHUNKING] kind=%s count=%d chars(min/avg/max)=%d/%d/%d",
                    kind,
                    len(lengths),
                    kind_min,
                    kind_avg,
                    kind_max,
                )

            if cfg.dry_run:
                file_elapsed = time.time() - file_start_time
                logger.info(
                    "[DRY_RUN] Skipping embedding and upserting (elapsed: %.2fs)\n",
                    file_elapsed,
                )
                return 1, len(expanded_chunks)

            embed_start_time = time.time()
            upsert_total_time = 0.0
            texts, ids, metadatas = _build_upsert_payloads(
                expanded_chunks=expanded_chunks,
                file_path=file_path,
                file_sha256=file_sha256,
                rel_path=rel_path,
            )
            logger.info("[EMBEDDING] Processing %d chunks...", len(texts))

            batch_count = 0
            for i in range(0, len(texts), batch_size):
                batch_count += 1
                batch_docs = texts[i : i + batch_size]
                batch_ids = ids[i : i + batch_size]
                batch_meta = metadatas[i : i + batch_size]
                batch_start = time.time()

                logger.info(
                    "  [BATCH %d/%d] Embedding and upserting: items [%d-%d] (%d chunks)",
                    batch_count,
                    (len(texts) + batch_size - 1) // batch_size,
                    i,
                    min(i + batch_size, len(texts)) - 1,
                    len(batch_docs),
                )
                embed_batch_start = time.time()
                batch_vecs = await embedder.embed(batch_docs)
                embed_batch_elapsed = time.time() - embed_batch_start
                upsert_batch_start = time.time()
                async with store_lock:
                    await store.upsert(
                        ids=batch_ids,
                        documents=batch_docs,
                        embeddings=batch_vecs,
                        metadatas=batch_meta,
                    )
                upsert_batch_elapsed = time.time() - upsert_batch_start
                upsert_total_time += upsert_batch_elapsed
                batch_elapsed = time.time() - batch_start
                logger.info(
                    "  [BATCH %d] Done (total=%.2fs | embed=%.2fs | upsert=%.2fs)",
                    batch_count,
                    batch_elapsed,
                    embed_batch_elapsed,
                    upsert_batch_elapsed,
                )

            embed_elapsed = time.time() - embed_start_time
            file_elapsed = time.time() - file_start_time
            logger.info(
                "[FILE_SUMMARY] %d chunks processed in %.2fs (embedding: %.2fs | upsert: %.2fs)\n",
                len(texts),
                file_elapsed,
                embed_elapsed,
                upsert_total_time,
            )
            return 1, len(expanded_chunks)

    try:
        results = await asyncio.gather(
            *[asyncio.create_task(_process_file(p)) for p in file_paths]
        )
        for files_indexed_inc, chunks_emitted_inc in results:
            stats.files_indexed += files_indexed_inc
            stats.chunks_emitted += chunks_emitted_inc
    finally:
        if embedder is not None and hasattr(embedder, "close"):
            close_fn = getattr(embedder, "close")
            if asyncio.iscoroutinefunction(close_fn):
                await close_fn()
            else:
                close_fn()

    index_elapsed = time.time() - index_start_time
    logger.info("=" * 80)
    logger.info(
        "INDEXING COMPLETE | files_seen=%d | files_indexed=%d | chunks=%d | elapsed=%.2fs",
        stats.files_seen,
        stats.files_indexed,
        stats.chunks_emitted,
        index_elapsed,
    )
    logger.info("=" * 80)
    return stats
