from __future__ import annotations

import fnmatch
import hashlib
import logging
import os
import uuid
from dataclasses import dataclass, field
from typing import Any, Iterable, Iterator, List, Optional, Sequence

from .chunking import Chunk, Config as ChunkConfig, TreeSitterChunker
from .db import VectorStore
from .embedding import Embedder

logger = logging.getLogger(__name__)


def _hash_file_sha256(path: str) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            hasher.update(block)
    return hasher.hexdigest()


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


def _is_probably_text_file(path: str, *, chunk_cfg: ChunkConfig, sample_size: int = 8192) -> bool:
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


def index_directory(
    *,
    cfg: IndexConfig,
    chunk_cfg: Optional[ChunkConfig] = None,
    embedder: Optional[Embedder] = None,
    store: Optional[VectorStore] = None,
    batch_size: int = 128,
) -> IndexStats:
    """Index a directory end-to-end (scan -> chunk -> embed -> write).

    Current status: framework only.
    - We implement scan + chunk + embed batching.
    - We only write if cfg.dry_run is False AND store is provided.
    """

    stats = IndexStats()
    chunk_cfg = chunk_cfg or ChunkConfig()
    chunker = TreeSitterChunker(chunk_cfg)

    if not cfg.dry_run and store is None:
        raise ValueError("store is required when dry_run=False")

    # We allow embedder=None for a pure chunking dry-run.
    
    for file_path in iter_candidate_files(cfg):
        stats.files_seen += 1

        # Default behaviour: skip non-text/binary files (images, archives, etc).
        if not _is_probably_text_file(file_path, chunk_cfg=chunk_cfg):
            logger.info("Skipping non-text file: %s", file_path)
            continue

        try:
            file_sha256 = _hash_file_sha256(file_path)
        except OSError:
            continue

        chunks: List[Chunk] = list(chunker.chunk(file_path))
        if not chunks:
            continue

        # Attach minimal metadata (VectorCode-style) for downstream store.
        for c in chunks:
            c.path = file_path
            c.sha256 = file_sha256

        stats.files_indexed += 1
        stats.chunks_emitted += len(chunks)

        if cfg.dry_run:
            continue

        if embedder is None:
            raise ValueError("embedder is required when dry_run=False")

        assert store is not None

        # VectorCode-style update strategy: delete all existing chunks for the file,
        # then re-insert. This keeps the implementation simple even when chunk IDs
        # are not stable across runs.
        store.delete_by_path(path=file_path)

        # Batch embed + upsert. This is the main shape; we will refine metadata
        # and update strategy (delete-by-path vs stable IDs) later.
        texts = [c.text for c in chunks]
        ids = [_new_id() for _ in chunks]
        metadatas: list[dict[str, Any]] = []
        for c in chunks:
            meta: dict[str, Any] = {
                "path": c.path,
                "sha256": c.sha256,
            }
            if c.start is not None:
                meta["start_line"] = int(getattr(c.start, "row", 0))
            if c.end is not None:
                meta["end_line"] = int(getattr(c.end, "row", 0))
            if c.language is not None:
                meta["language"] = c.language
            metadatas.append(meta)

        for i in range(0, len(texts), batch_size):
            batch_docs = texts[i : i + batch_size]
            batch_ids = ids[i : i + batch_size]
            batch_meta = metadatas[i : i + batch_size]
            batch_vecs = embedder.embed(batch_docs)
            store.upsert(
                ids=batch_ids,
                documents=batch_docs,
                embeddings=batch_vecs,
                metadatas=batch_meta,
            )

    return stats
