from __future__ import annotations

from pathlib import Path
import textwrap

import pytest

from mini_code_index.chunking import Config, ScopeKind, TreeSitterChunker


def _require_treesitter() -> None:
    from mini_code_index import chunking as m

    assert m._HAS_TREESITTER, "tree-sitter must be available in this test suite"


def _write(tmp_path: Path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content, encoding="utf8")
    return str(p)


def _fmt_scopes(scopes) -> str:
    return " / ".join(f"{s.kind.value}:{s.name}" for s in scopes) if scopes else "<empty>"


def _print_chunks(title: str, chunks) -> None:
    print(f"\n=== {title} ===")
    for i, c in enumerate(chunks, 1):
        start = (c.start.row, c.start.column) if c.start else None
        end = (c.end.row, c.end.column) if c.end else None
        print(
            f"#{i:02d} start={start} end={end} chars={len(c.text)} "
            f"scope_path={_fmt_scopes(c.scope_path)} contained={_fmt_scopes(c.contained_scopes)}"
        )
        print("----- chunk text -----")
        print(c.text)
        print("----- /chunk text -----")


def test_python_long_file_boundary_file_print(tmp_path: Path):
    """
    Similar to the Java long-file test, but for Python.
    boundary=FILE => pure text chunking by chunk_size/overlap, while contained_scopes
    still reports TYPE/FUNCTION overlapping each chunk.
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os
        import json

        # A long-ish python file with multiple classes, methods, and nested functions.

        def top(a, b):
            \"\"\"top level function\"\"\"
            def inner(x):
                return x + 1
            return inner(a) + b

        class A:
            CONST = 123

            def __init__(self, mode: str):
                self.mode = mode

            def add(self, a: int, b: int) -> int:
                x = a + b
                return x

            def run(self, xs: list[int]) -> int:
                s = 0
                for x in xs:
                    s += self._work_one(x)
                return s

            def _work_one(self, x: int) -> int:
                if self.mode == "fast":
                    return x + 1
                return x + 2

        class B:
            def f(self):
                return os.getcwd()

        async def af():
            return json.dumps({"cwd": os.getcwd()})
        """
    )
    path = _write(tmp_path, "big.py", code)

    print("\n\n\n\n+++++++++FILE BOUNDARY++++++++\n\n\n\n")
    cfg = Config(chunk_size=220, overlap_ratio=0.0, boundary=ScopeKind.FILE)
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks("python long file (boundary=FILE, chunk_size=220)", chunks)

    print("\n\n\n\n+++++++++TYPE BOUNDARY++++++++\n\n\n\n")
    cfg = Config(chunk_size=220, overlap_ratio=0.0, boundary=ScopeKind.TYPE)
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks("python long file (boundary=TYPE, chunk_size=220)", chunks)

    print("\n\n\n\n+++++++++FUNCTION BOUNDARY++++++++\n\n\n\n")
    cfg = Config(chunk_size=220, overlap_ratio=0.0, boundary=ScopeKind.FUNCTION)
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks("python long file (boundary=FUNCTION, chunk_size=220)", chunks)
    assert chunks


def test_python_long_file_boundary_type_print(tmp_path: Path):
    """
    boundary=TYPE => each class is emitted as one chunk if it fits, else split by size/overlap.
    top-level functions remain as plain text chunks.
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os

        class A:
            def m(self):
                return 1

        class B:
            def n(self):
                return 2

        def f():
            return os.getcwd()
        """
    )
    path = _write(tmp_path, "types.py", code)

    cfg = Config(chunk_size=120, overlap_ratio=0.0, boundary=ScopeKind.TYPE)
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks("python (boundary=TYPE, chunk_size=120)", chunks)
    assert chunks


def test_python_two_files_boundary_function_print(tmp_path: Path):
    """
    boundary=FUNCTION => functions/methods are the main unit:
    - small TYPE blocks may be emitted as a single chunk with contained_scopes listing methods
    - large functions are split by size/overlap
    """
    _require_treesitter()

    code_a = textwrap.dedent(
        """\
        class A:
            def m(self):
                return 1

            def n(self):
                return 2
        """
    )
    code_b = textwrap.dedent(
        """\
        def big():
            # make this long enough to require splitting under small chunk_size
            s = 0
            for i in range(100):
                s += i
            return s

        async def af():
            return 1
        """
    )

    path_a = _write(tmp_path, "a.py", code_a)
    path_b = _write(tmp_path, "b.py", code_b)

    cfg = Config(chunk_size=80, overlap_ratio=0.2, boundary=ScopeKind.FUNCTION)
    chunker = TreeSitterChunker(cfg)

    chunks_a = list(chunker.chunk(path_a))
    _print_chunks("python file1 a.py (boundary=FUNCTION, chunk_size=80, overlap=0.2)", chunks_a)

    chunks_b = list(chunker.chunk(path_b))
    _print_chunks("python file2 b.py (boundary=FUNCTION, chunk_size=80, overlap=0.2)", chunks_b)

    assert chunks_a and chunks_b


def test_python_chunk_filters_file_boundary_masks_lines_print(tmp_path: Path):
    """
    Demonstrate FILE-boundary line masking for chunk_filters:
    - lines that match (after lstrip) are replaced with spaces, preserving positions
    - useful code in the same chunk remains visible
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os
        import json

        def f():
            return 1
        """
    )
    path = _write(tmp_path, "filter_file.py", code)

    cfg = Config(
        chunk_size=25,
        overlap_ratio=0.0,
        boundary=ScopeKind.FILE,
        chunk_filters={"python": [r"import"]},
    )
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks("python FILE-boundary filter masking (chunk_size=25, filter=import)", chunks)
    assert chunks


