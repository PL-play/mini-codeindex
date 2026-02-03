import asyncio
import os
import random
from typing import Sequence, Mapping, Any, Optional
from urllib.parse import urlparse
from urllib.parse import urlparse

import pytest

from mini_code_index.chunking import Config as ChunkConfig, TreeSitterChunker, format_scope
from mini_code_index.db import ChromaStore, VectorStore, _collection_name_for_root
from mini_code_index.embedding import OpenAICompatibleEmbedder, Embedder
from mini_code_index.indexing import IndexConfig, index_directory, iter_candidate_files

from dotenv import load_dotenv

load_dotenv()


def _load_dotenv(path: str) -> None:
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


class DummyEmbedder(Embedder):
    async def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [[0.0] for _ in texts]


class CaptureStore(VectorStore):
    def __init__(self) -> None:
        self.deleted_paths: list[str] = []
        self.upserts: list[dict[str, Any]] = []
        self.saved_outputs: list[str] = []

    async def ping(self) -> bool:  # pragma: nocover - not used in tests
        return True

    async def get_one_by_path(self, *, path: str) -> Optional[Mapping[str, Any]]:
        return None

    async def delete_by_path(self, *, path: str) -> None:
        self.deleted_paths.append(path)

    def get_upserts(self, path: str) -> list[dict[str, Any]]:
        return self.upserts

    def dump_chunks_to_file(self, path: str) -> str:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            i = 0
            for batch in self.upserts:
                for doc, meta in zip(batch.get("documents", []), batch.get("metadatas", [])):
                    f.write(f"+++++++ chunk-{i} ++++++\n")
                    if isinstance(meta, dict):
                        f.write(
                            f"path={meta.get('path')} relpath={meta.get('relpath')} "
                            f"lang={meta.get('language')} kind={meta.get('chunk_kind')} "
                            f"mode={meta.get('mode')}\n"
                        )
                        f.write(
                            f"start={meta.get('start_line')}:{meta.get('start_col')} "
                            f"end={meta.get('end_line')}:{meta.get('end_col')}\n"
                        )
                        f.write(f"scope_path={meta.get('scope_path_str')}\n")
                        f.write(f"contained={meta.get('contained_scopes_str')}\n")
                        f.write(f"language={meta.get('language')} mode={meta.get('mode')}\n")
                        f.write(
                            f"contained_scope_count={meta.get('contained_scope_count')} "
                            f"scope_depth={meta.get('scope_depth')}\n"
                        )
                        f.write(f"symbol_names={meta.get('symbol_names')}\n")
                        f.write(
                            f"group_id={meta.get('group_id')} group_index={meta.get('group_index')}\n"
                        )
                        f.write(
                            f"scope_range="
                            f"{meta.get('scope_start_line')}:{meta.get('scope_start_col')}"
                            f"->"
                            f"{meta.get('scope_end_line')}:{meta.get('scope_end_col')}\n"
                        )
                        f.write(
                            f"is_trivia={meta.get('is_trivia')} "
                            f"is_comment={meta.get('is_comment')}\n"
                        )
                    f.write("----- text -----\n")
                    f.write(doc)
                    if not doc.endswith("\n"):
                        f.write("\n")
                    f.write("----- /text -----\n")
                    f.write(f"--------- chunk-{i} ---------\n\n")
                    i += 1
        self.saved_outputs.append(path)
        return path

    async def upsert(
            self,
            *,
            ids: Sequence[str],
            documents: Sequence[str],
            embeddings: Sequence[Sequence[float]],
            metadatas: Sequence[Mapping[str, Any]],
    ) -> None:
        self.upserts.append(
            {
                "ids": list(ids),
                "documents": list(documents),
                "embeddings": [list(v) for v in embeddings],
                "metadatas": [dict(m) for m in metadatas],
            }
        )


@pytest.mark.integration
def test_index_directory_smoke(tmp_path) -> None:
    """Smoke test for the indexing pipeline.

    No asserts by design: this is a scaffold for you to fill in.

    What it demonstrates:
    - how to construct IndexConfig + ChunkConfig
    - how to wire an embedder + ChromaStore (optional)
    - how binary/non-text files are skipped by default
    """

    # --- prepare a tiny directory ---
    root_dir = "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"

    # --- configs you can tweak ---
    cfg = IndexConfig(
        root_dir=str(root_dir),
        dry_run=True,  # set to False when you want to write
        recursive=True,
        include_hidden=False,
        include_globs=["**/*"],
        exclude_globs=[
            "**/.git/**",
            "**/.venv/**",
            "**/__pycache__/**",
            "**/.pytest_cache/**",
            "**.lst"
        ],
    )

    chunk_cfg = ChunkConfig(
        chunk_size=1200,
        overlap_ratio=0.1,
        encoding="utf8",
        mode="function",
    )

    # --- optional wiring for actual writes ---
    chroma_url = os.environ.get("CHROMA_URL", "http://127.0.0.1:8010")
    store = ChromaStore(base_url=chroma_url, root_dir=str(root_dir))

    # For dry-run, embedder and store are unused.
    embedder = None

    # For real writes, uncomment and set cfg.dry_run=False:
    # embedder = OpenAICompatibleEmbedder.from_env()

    stats = asyncio.run(
        index_directory(cfg=cfg, chunk_cfg=chunk_cfg, embedder=embedder, store=store)
    )
    print(stats)


@pytest.mark.integration
def test_chunk_directory_with_complex_code(tmp_path) -> None:
    """Test chunking functionality with complex code directory.

    This test chunks the complex Java/Python test project we created
    and randomly prints some chunk results to verify chunking works.
    """

    # Use the complex test project directory we created
    test_project_dir = "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
    # Configure chunking
    chunk_cfg = ChunkConfig(
        chunk_size=1200,
        overlap_ratio=0.1,
        encoding="utf8",
        mode="function",
    )

    # Create chunker
    chunker = TreeSitterChunker(chunk_cfg)

    # Collect all chunks from the directory
    all_chunks = []
    try:
        for file_path in iter_candidate_files(IndexConfig(
                root_dir=str(test_project_dir),
                dry_run=True,
                recursive=True,
                include_hidden=False,
                include_globs=["**/*"],
                exclude_globs=[
                    "**/.git/**",
                    "**/.venv/**",
                    "**/__pycache__/**",
                    "**/.pytest_cache/**",
                    "**.class"
                ],
        )):
            try:
                chunks = list(chunker.chunk(file_path))
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"Warning: Failed to chunk {file_path}: {e}")
                continue

        # Print some statistics
        print(f"Successfully chunked directory: {test_project_dir}")
        print(f"Total chunks created: {len(all_chunks)}")

        # Randomly select and print some chunks
        if all_chunks:
            num_to_print = min(10, len(all_chunks))
            selected_chunks = random.sample(all_chunks, num_to_print)

            for i, chunk in enumerate(selected_chunks, 1):
                print(f"\n--- Chunk {i} ---")
                print(f"File: {chunk.path}")
                print(f"Language: {getattr(chunk, 'language', 'unknown')}")

                # Print position information
                if chunk.start and chunk.end:
                    print(f"Start: Line {chunk.start.row + 1}, Column {chunk.start.column}")
                    print(f"End: Line {chunk.end.row + 1}, Column {chunk.end.column}")
                else:
                    print("Position: Not available")

                # Print scope information
                if chunk.scope_path:
                    print(f"Scope Path: {' -> '.join(format_scope(s) for s in chunk.scope_path)}")
                else:
                    print("Scope Path: None")

                # Print contained scopes
                if chunk.contained_scopes:
                    print(f"Contained Scopes: {', '.join(format_scope(s) for s in chunk.contained_scopes)}")
                else:
                    print("Contained Scopes: None")

                print(f"Content length: {len(chunk.text)} characters")
                print(f"Content preview: {chunk.text[:1000]}")
                if len(chunk.text) > 1000:
                    print("... (truncated)")

        # If we get here without exceptions, the test passes
        assert True, "Chunking completed successfully"

    except Exception as e:
        pytest.fail(f"Chunking failed with exception: {e}")


@pytest.mark.integration
def test_index_directory_no_error() -> None:
    """Run index_directory on the complex test project and ensure no error."""

    test_project_dir = "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
    cfg = IndexConfig(
        root_dir=str(test_project_dir),
        dry_run=False,
        recursive=True,
        include_hidden=False,
        include_globs=["**/*"],
        exclude_globs=[
            "**/.git/**",
            "**/.venv/**",
            "**/__pycache__/**",
            "**/.pytest_cache/**",
            "**.class",
        ],
    )

    chunk_cfg = ChunkConfig(
        chunk_size=1200,
        overlap_ratio=0.1,
        encoding="utf8",
        mode="function",
    )
    store = CaptureStore()
    embedder = DummyEmbedder()

    stats = asyncio.run(
        index_directory(cfg=cfg, chunk_cfg=chunk_cfg, embedder=embedder, store=store)
    )
    print(stats)


@pytest.mark.integration
def test_index_directory_capture_chunks_to_file(tmp_path) -> None:
    """Index a project and dump collected chunks into a text file."""
    test_project_dir = "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
    cfg = IndexConfig(
        root_dir=str(test_project_dir),
        dry_run=False,
        recursive=True,
        include_hidden=False,
        include_globs=["**/*"],
        exclude_globs=[
            "**/.git/**",
            "**/.venv/**",
            "**/__pycache__/**",
            "**/.pytest_cache/**",
            "**.class",
            "**.lst"
        ],
    )
    chunk_cfg = ChunkConfig(
        chunk_size=1200,
        overlap_ratio=0.1,
        encoding="utf8",
        mode="function",
    )
    store = CaptureStore()
    embedder = DummyEmbedder()

    stats = asyncio.run(
        index_directory(cfg=cfg, chunk_cfg=chunk_cfg, embedder=embedder, store=store)
    )
    print(stats)

    output_path = os.path.join("./", "captured_chunks.txt")
    store.dump_chunks_to_file(output_path)
    print(f"wrote chunks to: {output_path}")


@pytest.mark.integration
def test_full_pipeline_with_real_services() -> None:
    """Run end-to-end indexing using real embeddings + ChromaDB."""

    _load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

    chroma_host = os.environ.get("CHROMADB_HOST")
    if not chroma_host:
        pytest.skip("CHROMADB_HOST not set")

    try:
        embedder = OpenAICompatibleEmbedder.from_env()
    except Exception as e:
        pytest.skip(f"Embedder config missing: {e}")

    test_project_dir = "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
    cfg = IndexConfig(
        root_dir=str(test_project_dir),
        dry_run=False,
        recursive=True,
        include_hidden=False,
        include_globs=["**/*"],
        exclude_globs=[
            "**/.git/**",
            "**/.venv/**",
            "**/__pycache__/**",
            "**/.pytest_cache/**",
            "**.class",
        ],
    )
    chunk_cfg = ChunkConfig(
        chunk_size=1200,
        overlap_ratio=0.1,
        encoding="utf8",
        mode="function",
    )

    store = ChromaStore(base_url=chroma_host, root_dir=str(test_project_dir))
    stats = asyncio.run(
        index_directory(
            cfg=cfg,
            chunk_cfg=chunk_cfg,
            embedder=embedder,
            store=store,
            force_upsert=True,
            batch_size=128,
        )
    )
    print(stats)


@pytest.mark.integration
def test_chromadb_query_smoke() -> None:
    """Smoke test for querying ChromaDB using real embeddings."""
    chroma_host = os.environ.get("CHROMADB_HOST")
    if not chroma_host:
        pytest.skip("CHROMADB_HOST not set")

    try:
        import chromadb
    except Exception as e:
        pytest.skip(f"chromadb not available: {e}")

    try:
        embedder = OpenAICompatibleEmbedder.from_env()
    except Exception as e:
        pytest.skip(f"Embedder config missing: {e}")

    parsed = urlparse(chroma_host)
    client = chromadb.HttpClient(host=parsed.hostname, port=parsed.port)

    root_dir = "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
    collection_name = _collection_name_for_root(root_dir)
    try:
        collection = client.get_collection(collection_name)
    except Exception as e:
        pytest.skip(f"Collection not found: {e}")

    async def _run_query() -> Any:
        query = "decorate"
        async with embedder:
            embedding = (await embedder.embed([query]))[0]
            results = collection.query(
                query_embeddings=[embedding],
                n_results=25,
                # where={"$and": [{"chunk_kind": "code"}, {"is_trivia": False}]},
                where={"$and": [{"is_comment": False}, {"is_trivia": False}]},
            )
            return results

    results = asyncio.run(_run_query())
    print(results)
    assert results is not None
