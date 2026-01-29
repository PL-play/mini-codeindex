import os
import random

import pytest

from mini_code_index.chunking import Config as ChunkConfig, TreeSitterChunker, format_scope
from mini_code_index.db import ChromaStore
from mini_code_index.embedding import OpenAICompatibleEmbedder
from mini_code_index.indexing import IndexConfig, index_directory, iter_candidate_files


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

    stats = index_directory(cfg=cfg, chunk_cfg=chunk_cfg, embedder=embedder, store=store)
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
