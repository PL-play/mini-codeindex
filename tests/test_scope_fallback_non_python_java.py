from __future__ import annotations

from pathlib import Path
import textwrap

from mini_code_index.chunking import Config, ScopeKind, TreeSitterChunker


def _require_treesitter() -> None:
    from mini_code_index import chunking as m

    assert m._HAS_TREESITTER, "tree-sitter must be available in this test suite"


def _write(tmp_path: Path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content, encoding="utf8")
    return str(p)


def test_scope_fallback_javascript_file_mode_has_contained_scopes(tmp_path: Path):
    """
    For non-python/java languages, _scope_of_node should still produce TYPE/FUNCTION scopes
    via generic heuristics.
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        function top(x) { return x + 1; }

        class A {
          m(y) { return y + 2; }
        }
        """
    )
    path = _write(tmp_path, "a.js", code)

    cfg = Config(chunk_size=40, overlap_ratio=0.0, mode="file")
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    # Debug-friendly prints
    print("\n=== js file mode chunks ===")
    for i, c in enumerate(chunks, 1):
        print(f"#{i:02d} scopes={[(s.kind.value, s.name) for s in c.contained_scopes]}")

    assert chunks
    # At least somewhere we should see the class/function names surfaced.
    assert any(any(s.kind == ScopeKind.FUNCTION and s.name == "top" for s in c.contained_scopes) for c in chunks)
    assert any(any(s.kind == ScopeKind.TYPE and s.name == "A" for s in c.contained_scopes) for c in chunks)


