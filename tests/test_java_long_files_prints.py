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


def test_java_long_file_boundary_file_print(tmp_path: Path):
    """
    Single long Java file, boundary=FILE (coarsest).
    Expectation: chunks may mix multiple types/methods, only constrained by chunk_size.
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        package com.example.big;

        import java.util.*;
        import java.util.concurrent.*;

        // A long-ish file with multiple types and methods.
        interface IWorker {
            int work(int x);
        }

        enum Mode { FAST, SAFE }

        record Pair(int a, int b) {}

        public class MainApp {
            private final Mode mode;

            public MainApp(Mode mode) {
                this.mode = mode;
            }

            public static int add(int a, int b) {
                int x = a + b;
                return x;
            }

            public static int mul(int a, int b) {
                int x = a * b;
                return x;
            }

            public int run(List<Integer> xs) {
                int sum = 0;
                for (int x : xs) {
                    sum += workOne(x);
                }
                return sum;
            }

            private int workOne(int x) {
                if (mode == Mode.FAST) {
                    return x + 1;
                }
                return x + 2;
            }

            public static void main(String[] args) {
                MainApp app = new MainApp(Mode.SAFE);
                System.out.println(app.run(Arrays.asList(1, 2, 3)));
                System.out.println(add(10, 20));
                System.out.println(mul(3, 4));
            }

            static class Nested {
                static int id(int x) { return x; }
            }
        }
        """
    )
    path = _write(tmp_path, "MainApp.java", code)
    print("+++++++++FILE BOUNDARY++++++++\n\n\n\n")
    cfg = Config(
        chunk_size=220,
        overlap_ratio=0.2,
        boundary=ScopeKind.FILE,
        filetype_map={"java": [r"^java$"]},
    )
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks("java long file (boundary=FILE, chunk_size=220)", chunks)


    print("\n\n\n\n+++++++++TYPE BOUNDARY++++++++\n\n\n\n")
    cfg = Config(
        chunk_size=220,
        overlap_ratio=0.2,
        boundary=ScopeKind.TYPE,
        filetype_map={"java": [r"^java$"]},
    )
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks("java long file (boundary=TYPE, chunk_size=220)", chunks)

    print("\n\n\n\n+++++++++FUNCTION BOUNDARY++++++++\n\n\n\n")
    cfg = Config(
        chunk_size=220,
        overlap_ratio=0.2,
        boundary=ScopeKind.FUNCTION,
        filetype_map={"java": [r"^java$"]},
    )
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks("java long file (boundary=FUNCTION, chunk_size=220)", chunks)

    assert chunks


def test_java_long_file_boundary_type_print(tmp_path: Path):
    """
    Same long file, boundary=TYPE.
    Expectation: top-level TYPE declarations won't be mixed into the same chunk.
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        package com.example.big;

        interface IWorker {
            int work(int x);
        }

        enum Mode { FAST, SAFE }

        record Pair(int a, int b) {}

        public class A {
            public int f(int x) { return x + 1; }
        }

        class B {
            public int g(int x) { return x + 2; }
        }
        """
    )
    path = _write(tmp_path, "Types.java", code)

    cfg = Config(
        chunk_size=120,
        overlap_ratio=0.0,
        boundary=ScopeKind.TYPE,
        filetype_map={"java": [r"^java$"]},
    )
    chunks = list(TreeSitterChunker(cfg).chunk(path))
    _print_chunks("java long file (boundary=TYPE, chunk_size=120)", chunks)

    assert chunks
    joined = "".join(c.text for c in chunks)
    assert "interface IWorker" in joined and "class B" in joined


def test_java_two_files_boundary_function_print(tmp_path: Path):
    """
    Two separate Java files, boundary=FUNCTION (finest).
    Expectation: each method/constructor will tend to form its own chunk(s) under small chunk_size.
    """
    _require_treesitter()

    code_a = textwrap.dedent(
        """\
        package com.example.multi;

        public class MathUtil {
            public MathUtil() {}

            public static int add(int a, int b) {
                int x = a + b;
                int y = x + 0;
                return y;
            }

            public static int mul(int a, int b) {
                int x = a * b;
                return x;
            }
        }
        """
    )
    code_b = textwrap.dedent(
        """\
        package com.example.multi;

        public class App {
            public static void main(String[] args) {
                System.out.println(MathUtil.add(1, 2));
                System.out.println(MathUtil.mul(3, 4));
            }

            static int local(int x) {
                return x + 1;
            }
        }
        """
    )

    path_a = _write(tmp_path, "MathUtil.java", code_a)
    path_b = _write(tmp_path, "App.java", code_b)

    cfg = Config(
        chunk_size=80,
        overlap_ratio=0.0,
        boundary=ScopeKind.FUNCTION,
        filetype_map={"java": [r"^java$"]},
    )
    chunker = TreeSitterChunker(cfg)

    chunks_a = list(chunker.chunk(path_a))
    _print_chunks("java file1 MathUtil.java (boundary=FUNCTION, chunk_size=80)", chunks_a)

    chunks_b = list(chunker.chunk(path_b))
    _print_chunks("java file2 App.java (boundary=FUNCTION, chunk_size=80)", chunks_b)

    assert chunks_a and chunks_b


def test_java_many_blank_lines_gap_trim_effect_print(tmp_path: Path):
    """
    Show effect of trim_gap_blank_lines in Java (prints chunk text so you can see gaps).
    """
    _require_treesitter()

    code = textwrap.dedent(
        """\
        package com.example.gaps;

        public class Gaps {



            public static int f() {


                return 1;
            }



            public static int g() {
                return 2;
            }
        }
        """
    )
    path = _write(tmp_path, "Gaps.java", code)

    cfg_no_trim = Config(
        chunk_size=200,
        overlap_ratio=0.0,
        boundary=ScopeKind.FUNCTION,
        trim_gap_blank_lines=False,
        filetype_map={"java": [r"^java$"]},
    )
    chunks_no_trim = list(TreeSitterChunker(cfg_no_trim).chunk(path))
    _print_chunks("java gaps (trim_gap_blank_lines=False)", chunks_no_trim)

    cfg_trim = Config(
        chunk_size=200,
        overlap_ratio=0.0,
        boundary=ScopeKind.FUNCTION,
        trim_gap_blank_lines=True,
        filetype_map={"java": [r"^java$"]},
    )
    chunks_trim = list(TreeSitterChunker(cfg_trim).chunk(path))
    _print_chunks("java gaps (trim_gap_blank_lines=True)", chunks_trim)

    assert chunks_no_trim and chunks_trim


