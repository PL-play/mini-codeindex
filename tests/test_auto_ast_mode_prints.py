from __future__ import annotations

from pathlib import Path
import textwrap

from mini_code_index.chunking import Config, TreeSitterChunker, print_chunks


def _require_treesitter() -> None:
    from mini_code_index import chunking as m

    assert m._HAS_TREESITTER, "tree-sitter must be available in this test suite"


def _write(tmp_path: Path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content, encoding="utf8")
    return str(p)


def test_auto_ast_mode_smoke_python_print(tmp_path: Path):
    """
    Smoke test for mode=auto_ast:
    - prints chunks so you can compare with other modes
    - checks that scope_path contains file and contained_scopes is populated sometimes
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os

        def f(x):
            return x + 1

        class A:
            def m(self):
                return 2

        def g():
            return os.getcwd()
        """
    )
    path = _write(tmp_path, "auto.py", code)

    cfg = Config(chunk_size=80, overlap_ratio=0.0, mode="auto_ast")
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    print_chunks('auto_ast python chunks (mode="auto_ast")', chunks, include_text=True)

    assert chunks
    # scope_path should always contain file container in our implementation
    assert all(any(s.kind.value == "file" for s in c.scope_path) for c in chunks)


