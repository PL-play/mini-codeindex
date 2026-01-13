from __future__ import annotations

import hashlib
from pathlib import Path
import textwrap

import pytest

from mini_code_index.chunking import Config, ScopeKind, TreeSitterChunker


def _assert_python_parser(parser) -> None:
    tree = parser.parse(b"def f(x):\n    return x + 1\n")
    root = tree.root_node
    assert root.type == "module"
    assert not getattr(root, "has_error", False)


def _assert_java_parser(parser) -> None:
    tree = parser.parse(
        b"public class A { public static int add(int a, int b) { return a + b; } }\n"
    )
    root = tree.root_node
    assert root.type == "program"
    assert not getattr(root, "has_error", False)


def _require_treesitter() -> None:
    from mini_code_index import chunking as m

    assert m._HAS_TREESITTER, "tree-sitter must be available in this test suite"


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

    _require_treesitter()

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


def test_config_overlap_ratio_validation():
    with pytest.raises(ValueError):
        Config(overlap_ratio=-0.01)
    with pytest.raises(ValueError):
        Config(overlap_ratio=1.0)

def test_default_scope_boundaries_are_file_type_function():
    cfg = Config()
    assert cfg.mode == "auto_ast"


def test_gap_trim_blank_lines_option_python(tmp_path: Path):
    _require_treesitter()

    code = textwrap.dedent(
        """\
        a = 1




        b = 2
        """
    )
    path = _write(tmp_path / "gap.py", code)

    # Gap trimming is an AST-mode feature (mode != "file"). Under mode="file" we do pure text chunking.
    cfg_no_trim = Config(chunk_size=10_000, overlap_ratio=0.0, trim_gap_blank_lines=False, mode="type")
    chunks_no_trim = list(TreeSitterChunker(cfg_no_trim).chunk(path))
    text_no_trim = "".join(c.text for c in chunks_no_trim)

    cfg_trim = Config(chunk_size=10_000, overlap_ratio=0.0, trim_gap_blank_lines=True, mode="type")
    chunks_trim = list(TreeSitterChunker(cfg_trim).chunk(path))
    text_trim = "".join(c.text for c in chunks_trim)

    assert "a = 1" in text_no_trim and "b = 2" in text_no_trim
    assert "a = 1" in text_trim and "b = 2" in text_trim
    # With trimming enabled, we should not preserve long runs of blank lines in gaps.
    assert "\n\n\n" in text_no_trim
    assert "\n\n\n" not in text_trim


def test_chunk_filters_excludes_matching_prefix_chunks(tmp_path: Path):
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os

        def f():
            return 1
        """
    )
    path = _write(tmp_path / "filter.py", code)

    # Choose a chunk size that will likely flush after the import and start a new chunk at `def f`.
    cfg = Config(chunk_size=25, overlap_ratio=0.0, chunk_filters={"python": [r"import"]})
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    assert any("def f" in c.text for c in chunks)
    assert not any(c.text.lstrip().startswith("import") for c in chunks)


def test_chunk_filters_is_prefix_match_not_search(tmp_path: Path):
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os

        def f():
            return os.getcwd()
        """
    )
    path = _write(tmp_path / "prefix_only.py", code)

    # Because chunk_filters uses re.match (prefix match), pattern "os" should NOT
    # match a chunk that starts with "import os".
    cfg = Config(chunk_size=25, overlap_ratio=0.0, chunk_filters={"python": [r"os"]})
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    assert any(c.text.lstrip().startswith("import") for c in chunks)


def test_chunk_filters_default_star_applies_when_no_language_rule(tmp_path: Path):
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os

        def f():
            return 1
        """
    )
    path = _write(tmp_path / "star_default.py", code)

    # Only provide a default rule; since language is "python" but no "python" key exists,
    # the "*" rule is used.
    cfg = Config(chunk_size=25, overlap_ratio=0.0, chunk_filters={"*": [r"import"]})
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    assert any("def f" in c.text for c in chunks)
    assert not any(c.text.lstrip().startswith("import") for c in chunks)


def test_chunk_filters_language_rule_overrides_star(tmp_path: Path):
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os

        def f():
            return 1
        """
    )
    path = _write(tmp_path / "lang_overrides.py", code)

    # When language-specific rules exist, the implementation uses ONLY those patterns,
    # not the default "*" list.
    cfg = Config(
        chunk_size=25,
        overlap_ratio=0.0,
        chunk_filters={"*": [r"def"], "python": [r"import"]},
    )
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    assert any("def f" in c.text for c in chunks)
    assert not any(c.text.lstrip().startswith("import") for c in chunks)


def test_filetype_map_selects_parser_when_available(tmp_path: Path):
    _require_treesitter()

    # This asserts that _get_parser_from_config can find a parser for a given extension.
    path = _write(tmp_path / "mapped.py", "x = 1\n")
    cfg = Config(filetype_map={"python": [r"^py$"]})
    chunker = TreeSitterChunker(cfg)
    parser, language = chunker._get_parser_from_config(path)
    assert parser is not None
    assert language == "python"
    _assert_python_parser(parser)


def test_filetype_map_prevents_guess_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _require_treesitter()

    code = "x = 1\n" * 10
    path = _write(tmp_path / "mapped_only.py", code)

    cfg = Config(chunk_size=50, overlap_ratio=0.0, filetype_map={"python": [r"^py$"]})
    chunker = TreeSitterChunker(cfg)

    called = {"guess": False}

    def _boom(_file_path: str, _content: str):
        called["guess"] = True
        raise AssertionError("_get_parser_by_guess should not be called when filetype_map matches")

    monkeypatch.setattr(chunker, "_get_parser_by_guess", _boom)

    chunks = list(chunker.chunk(path))
    assert called["guess"] is False
    assert len(chunks) >= 1


def test_chunk_path_java_file_smoke(tmp_path: Path):
    _require_treesitter()

    code = textwrap.dedent(
        """\
        package com.example;

        public class A {
            public static int add(int a, int b) {
                return a + b;
            }
        }
        """
    )
    path = _write(tmp_path / "A.java", code)

    cfg = Config(chunk_size=80, overlap_ratio=0.0)
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    assert len(chunks) >= 1
    assert any("class A" in c.text for c in chunks)
    assert any("return a + b" in c.text for c in chunks)

    parser, language = TreeSitterChunker(Config(filetype_map={"java": [r"^java$"]}))._get_parser_from_config(
        path
    )
    assert language == "java"
    assert parser is not None
    _assert_java_parser(parser)


def test_chunk_path_java_file_multiple_chunks_print(tmp_path: Path):
    _require_treesitter()

    code = textwrap.dedent(
        """\
        package com.example;

        import java.util.*;

        public class A {
        
            public int a;
            
            public static int b;
            
            public static int add(int a, int b) {
                return a + b;
            }

            public static int mul(int a, int b) {
                return a * b;
            }

            public static void main(String[] args) {
                System.out.println(add(1, 2));
                System.out.println(mul(3, 4));
            }
        }
        """
    )
    path = _write(tmp_path / "A.java", code)

    # Small chunk size to force multiple chunks.
    cfg = Config(chunk_size=120, overlap_ratio=0.2)
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    print("\n--- java produced chunks ---")  # visible under `pytest -s`
    for i, c in enumerate(chunks, 1):
        start = (c.start.row, c.start.column) if c.start else None
        end = (c.end.row, c.end.column) if c.end else None
        preview = " ".join(c.text.strip().split())[:160]
        print(f"#{i:02d} start={start} end={end} chars={len(c.text)} preview={preview}")

    assert len(chunks) >= 2
    joined = "".join(c.text for c in chunks)
    assert "class A" in joined
    assert "return a + b" in joined
    assert "return a * b" in joined


def test_chunk_filters_java_can_filter_package_declaration_print(tmp_path: Path):
    _require_treesitter()

    code = textwrap.dedent(
        """\
        package com.example;

        public class A {
        
        
        
            public int a;
            
            public static int b;
            
            public static int add(int a, int b) {
                return a + b;
            }
        }
        """
    )
    path = _write(tmp_path / "Filtered.java", code)

    # Make the chunk size small enough that the package declaration is likely its own chunk.
    cfg = Config(chunk_size=40, overlap_ratio=0.0, chunk_filters={"java": [r"package"]})
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    print("\n--- java filtered chunks ---")  # visible under `pytest -s`
    for i, c in enumerate(chunks, 1):
        preview = " ".join(c.text.strip().split())[:160]
        print(f"#{i:02d} chars={len(c.text)} preview={preview}")

    assert len(chunks) >= 1
    assert any("class A" in c.text for c in chunks)
    assert not any(c.text.lstrip().startswith("package") for c in chunks)


def test_chunk_str_python_by_language_smoke() -> None:
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os

        def add(a, b):
            return a + b
        """
    )

    cfg = Config(chunk_size=80, overlap_ratio=0.0)
    chunker = TreeSitterChunker(cfg)
    chunks = list(chunker.chunk_str(code, language="python"))

    assert len(chunks) >= 1
    assert any("def add" in c.text for c in chunks)


def test_chunk_str_applies_chunk_filters_python() -> None:
    _require_treesitter()

    code = textwrap.dedent(
        """\
        import os

        def f():
            return 1
        """
    )

    # Small chunk size to encourage a separate chunk starting with "import".
    cfg = Config(chunk_size=25, overlap_ratio=0.0, chunk_filters={"python": [r"import"]})
    chunks = list(TreeSitterChunker(cfg).chunk_str(code, language="python"))

    assert any("def f" in c.text for c in chunks)
    assert not any(c.text.lstrip().startswith("import") for c in chunks)


def test_chunk_str_falls_back_to_string_chunker_when_no_parser() -> None:
    # No `path` and no `language` => no parser selection => fallback.
    cfg = Config(chunk_size=2, overlap_ratio=0.0)
    chunks = list(TreeSitterChunker(cfg).chunk_str("abcd"))
    assert [c.text for c in chunks] == ["ab", "cd"]


def test_chunk_delegates_to_chunk_str(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = _write(tmp_path / "x.py", "print('hi')\n")

    cfg = Config(chunk_size=10, overlap_ratio=0.0)
    chunker = TreeSitterChunker(cfg)

    called = {"ok": False}

    def _fake_chunk_str(content: str, *, path=None, **_kwargs):
        called["ok"] = True
        assert path is not None
        assert "print" in content
        yield from []

    monkeypatch.setattr(chunker, "chunk_str", _fake_chunk_str)
    list(chunker.chunk(path))
    assert called["ok"] is True


def test_chunk_sets_path_sha256_language_and_container(tmp_path: Path) -> None:
    _require_treesitter()

    code = textwrap.dedent(
        """\
        class A:
            def m(self):
                return 1

        def f():
            return 2
        """
    )
    path = _write(tmp_path / "meta.py", code)
    expected_sha = hashlib.sha256(Path(path).read_bytes()).hexdigest()

    # Use a small chunk size to force recursion into the class body,
    # so we can observe method-level scope.
    cfg = Config(chunk_size=20, overlap_ratio=0.0, mode="function")
    chunks = list(TreeSitterChunker(cfg).chunk(path))

    assert len(chunks) >= 1
    assert all(c.path == path for c in chunks)
    assert all(c.sha256 == expected_sha for c in chunks)
    assert all(c.language == "python" for c in chunks)

    # Boundary-truncated scope_path + contained_scopes for inner (function/method) info
    assert all(any(s.kind == ScopeKind.FILE and s.name == "meta" for s in c.scope_path) for c in chunks)

    # "A" is a TYPE scope now (unified across class/interface/enum/record/...).
    assert any(any(s.kind == ScopeKind.TYPE and s.name == "A" for s in c.scope_path) for c in chunks)

    # With mode="function", functions/methods are expected to appear in scope_path.
    assert any(
        "def m" in c.text
        and any(s.kind == ScopeKind.TYPE and s.name == "A" for s in c.scope_path)
        and any(s.kind == ScopeKind.FUNCTION and s.name == "m" for s in c.scope_path)
        for c in chunks
    )

    # The top-level function f should be a FUNCTION scope without a TYPE parent.
    assert any(
        "def f" in c.text
        and any(s.kind == ScopeKind.FUNCTION and s.name == "f" for s in c.scope_path)
        and not any(s.kind == ScopeKind.TYPE for s in c.scope_path)
        for c in chunks
    )


def test_chunk_str_sets_language_but_no_path_or_sha256_when_not_given() -> None:
    _require_treesitter()

    code = "def add(a, b):\n    return a + b\n"
    chunks = list(TreeSitterChunker(Config(chunk_size=80, overlap_ratio=0.0)).chunk_str(code, language="python"))

    assert len(chunks) >= 1
    assert all(c.language == "python" for c in chunks)
    assert all(c.path is None for c in chunks)
    assert all(c.sha256 is None for c in chunks)


def test_chunk_java_sets_type_and_function_scopes(tmp_path: Path) -> None:
    _require_treesitter()

    code = textwrap.dedent(
        """\
        package com.example;

        public class A {
            public static int add(int a, int b) {
                int x = a + b;
                int y = x + 1;
                return y;
            }
        }
        """
    )
    path = _write(tmp_path / "A.java", code)
    chunks = list(
        TreeSitterChunker(Config(chunk_size=40, overlap_ratio=0.0, mode="function")).chunk(path)
    )

    assert len(chunks) >= 1
    assert all(c.language == "java" for c in chunks)

    assert any(any(s.kind == ScopeKind.TYPE and s.name == "A" for s in c.scope_path) for c in chunks)
    assert any(any(s.kind == ScopeKind.FUNCTION and s.name == "add" for s in c.scope_path) for c in chunks)


def test_python_async_function_scope_kind(tmp_path: Path) -> None:
    _require_treesitter()

    code = """
async def af():
    return 1
""".lstrip("\n")
    path = _write(tmp_path / "a.py", code)

    chunker = TreeSitterChunker(Config(chunk_size=200, overlap_ratio=0.0, mode="function"))
    chunks = list(chunker.chunk(path))
    assert chunks

    assert any(any(s.kind == ScopeKind.FUNCTION and s.name == "af" for s in c.scope_path) for c in chunks)


def test_java_constructor_and_type_kinds(tmp_path: Path) -> None:
    _require_treesitter()

    code = textwrap.dedent(
        """\
        package com.example;

        interface I { void x(); }
        enum E { A, B }
        record R(int x) {}

        class A {
          A() { }
          void m() { }
        }
        """
    )
    path = _write(tmp_path / "A.java", code)

    chunker = TreeSitterChunker(Config(chunk_size=400, overlap_ratio=0.0, mode="function"))
    chunks = list(chunker.chunk(path))
    assert chunks

    # interface/enum/record/class are all TYPE now.
    assert any(any(s.kind == ScopeKind.TYPE and s.name == "I" for s in c.scope_path) for c in chunks)
    assert any(any(s.kind == ScopeKind.TYPE and s.name == "E" for s in c.scope_path) for c in chunks)
    assert any(any(s.kind == ScopeKind.TYPE and s.name == "R" for s in c.scope_path) for c in chunks)
    assert any(any(s.kind == ScopeKind.TYPE and s.name == "A" for s in c.scope_path) for c in chunks)
    # With the optimized mode="function" behavior, small TYPE nodes may be emitted as a single chunk,
    # and their inner functions are reported via contained_scopes.
    assert any(any(s.kind == ScopeKind.FUNCTION and s.name == "A" for s in c.contained_scopes) for c in chunks)
    assert any(any(s.kind == ScopeKind.FUNCTION and s.name == "m" for s in c.contained_scopes) for c in chunks)





