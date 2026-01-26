import os

import pytest

from mini_code_index.chunking import Config as ChunkConfig
from mini_code_index.db import ChromaStore
from mini_code_index.embedding import OpenAICompatibleEmbedder
from mini_code_index.indexing import IndexConfig, index_directory


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
    root_dir = tmp_path / "repo"
    root_dir.mkdir()

    # Text file (should be processed)
    (root_dir / "a.py").write_text("print('hello')\n", encoding="utf-8")

    # Binary file (should be skipped)
    (root_dir / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\x0dIHDR")

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
        chunk_size=800,
        overlap_ratio=0.2,
        encoding="utf8",
        mode="auto_ast",
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
