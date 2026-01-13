from __future__ import annotations

from pathlib import Path
import textwrap

from mini_code_index.chunking import Config, ScopeKind, TreeSitterChunker, print_chunks


def _require_treesitter() -> None:
    from mini_code_index import chunking as m

    assert m._HAS_TREESITTER, "tree-sitter must be available in this test suite"


def _write(tmp_path: Path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content, encoding="utf8")
    return str(p)


def test_js_mode_function_discovers_methods_in_class_body_print(tmp_path: Path):
    """
    Regression/coverage: non-java/python languages (e.g. JS) often nest methods under "class_body".
    mode="function" should recurse into such container nodes so methods are emitted as FUNCTION chunks.
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        function top(x) { return x + 1; }

        class A {
          m(y) { return y + 2; }
          n(z) { return z + 3; }
        }
        """
    )
    path = _write(tmp_path, "a.js", code)

    cfg = Config(chunk_size=40, overlap_ratio=0.0, mode="function")
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    print_chunks('js (mode="function")', chunks, include_text=True)

    assert chunks
    # We expect at least one chunk to carry a FUNCTION scope in scope_path (method/function unit).
    assert any(any(s.kind == ScopeKind.FUNCTION for s in c.scope_path) for c in chunks)
    # And we should see method names.
    joined = "\n".join(c.text for c in chunks)
    assert "m(y)" in joined and "n(z)" in joined


