from __future__ import annotations

from pathlib import Path
import textwrap

import pytest

from mini_code_index.chunking import Config, ScopeKind, TreeSitterChunker, print_chunks


def _require_treesitter() -> None:
    from mini_code_index import chunking as m

    assert m._HAS_TREESITTER, "tree-sitter must be available in this test suite"


def _write(tmp_path: Path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content, encoding="utf8")
    return str(p)


def _print_chunks(title: str, chunks) -> None:
    print_chunks(title, list(chunks), include_text=True)


@pytest.mark.parametrize(
    "mode",
    [
        "file",
        "type",
        "function",
        "auto_ast",
    ],
)
@pytest.mark.parametrize("chunk_size", [50, 120, 10_000])
def test_python_boundaries_and_chunk_size_matrix_print(tmp_path: Path, mode: str, chunk_size: int):
    """
    Print-first matrix test for Python:
    - different modes (file/type/function/auto_ast)
    - different chunk sizes (tiny/medium/huge)
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os

        def top(a, b):
            # comment
            return a + b

        class A:
            def m(self, x):
                def inner(y):
                    return y + 1
                return inner(x)

        async def af():
            return os.getcwd()
        """
    )
    path = _write(tmp_path, "matrix.py", code)

    cfg = Config(chunk_size=chunk_size, overlap_ratio=0.0, mode=mode)
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks(f"python mode={mode} chunk_size={chunk_size}", chunks)

    # very light sanity so the test is stable
    assert chunks
    joined = "".join(c.text for c in chunks)
    assert "class A" in joined
    assert "def top" in joined


@pytest.mark.parametrize(
    "mode",
    [
        "file",
        "type",
        "function",
        "auto_ast",
    ],
)
@pytest.mark.parametrize("chunk_size", [60, 140, 10_000])
def test_java_boundaries_and_chunk_size_matrix_print(tmp_path: Path, mode: str, chunk_size: int):
    """
    Print-first matrix test for Java:
    - package/imports + multiple types + methods + constructor
    - different modes (file/type/function/auto_ast)
    - different chunk sizes
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        package com.example;

        import java.util.*;

        interface I { void x(); }
        enum E { A, B }
        record R(int x) {}

        public class A {
            public A() {}

            public static int add(int a, int b) {
                int x = a + b;
                return x;
            }

            public static int mul(int a, int b) {
                return a * b;
            }
        }
        """
    )
    path = _write(tmp_path, "A.java", code)

    cfg = Config(
        chunk_size=chunk_size,
        overlap_ratio=0.0,
        mode=mode,
        filetype_map={"java": [r"^java$"]},
    )
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks(f"java mode={mode} chunk_size={chunk_size}", chunks)

    assert chunks
    joined = "".join(c.text for c in chunks)
    assert "class A" in joined
    assert "return a * b" in joined


def test_boundary_effect_demo_python_print(tmp_path: Path):
    """
    A single demo showing how mode changes scope_path/contained_scopes with a small chunk_size.
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        class A:
            def m(self):
                return 1

            def n(self):
                return 2
        """
    )
    path = _write(tmp_path, "boundary_demo.py", code)

    cfg_type = Config(
        chunk_size=80,
        overlap_ratio=0.0,
        mode="type",
    )
    chunks_type = list(TreeSitterChunker(cfg_type).chunk(path))
    _print_chunks('python mode demo (mode="type")', chunks_type)

    cfg_func = Config(
        chunk_size=80,
        overlap_ratio=0.0,
        mode="function",
    )
    chunks_func = list(TreeSitterChunker(cfg_func).chunk(path))
    _print_chunks('python mode demo (mode="function")', chunks_func)

    assert chunks_type and chunks_func


