from __future__ import annotations

from pathlib import Path
import textwrap

import pytest

from mini_code_index.chunking import Config, TreeSitterChunker


def _write(p: Path, content: str) -> str:
    p.write_text(content, encoding="utf8")
    return str(p)


def test_chunk_path_python_file_smoke(tmp_path: Path):
    """
    Debug-friendly smoke test:
    - create a small python file
    - run TreeSitterChunker.chunk(path)
    - print chunk boundaries and previews
    """
    # NOTE: use REAL newlines here (not the two-character sequence "\\n"),
    # otherwise chunk row/col calculation will think everything is on row=1.
    code = textwrap.dedent(
        """\
        import os

        # this is a comment


        def add(a, b):
            '''
            this is add function doc string
            '''
            return a + b
        
        class A:
            def m(self):
                x = add(1, 2)
                return x
        """
    )
    path = _write(tmp_path / "sample.py", code)

    cfg = Config(chunk_size=115, overlap_ratio=0.0)

    chunks = list(TreeSitterChunker(cfg).chunk(path))

    print("\n--- produced chunks ---")  # visible under `pytest -s`
    for i, c in enumerate(chunks, 1):
        start = (c.start.row, c.start.column) if c.start else None
        end = (c.end.row, c.end.column) if c.end else None
        preview = " ".join(c.text.strip().split())[:120]
        print(f"#{i:02d} start={start} end={end} chars={len(c.text)} preview={preview}")

    # light sanity: we should get at least one chunk and it should contain some code
    assert len(chunks) >= 1
    assert any("def add" in c.text for c in chunks)


def test_chunk_path_fallback_when_no_treesitter(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """
    Force fallback mode (simulates missing tree-sitter) and ensure we still get chunks.
    """
    from mini_code_index import chunking as m

    monkeypatch.setattr(m, "_HAS_TREESITTER", False, raising=False)

    text = "a\n" * 50
    path = _write(tmp_path / "plain.txt", text)

    cfg = Config(chunk_size=20, overlap_ratio=0.0)
    chunks = list(m.TreeSitterChunker(cfg).chunk(path))

    print("\n--- fallback chunks ---")
    for i, c in enumerate(chunks, 1):
        start = (c.start.row, c.start.column) if c.start else None
        end = (c.end.row, c.end.column) if c.end else None
        print(f"#{i:02d} start={start} end={end} chars={len(c.text)}")

    assert len(chunks) >= 2


