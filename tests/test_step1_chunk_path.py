from __future__ import annotations

from pathlib import Path
import textwrap

import pytest

from mini_code_index.chunking import Config, TreeSitterChunker


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


def test_gap_trim_blank_lines_option_python(tmp_path: Path):
    _require_treesitter()

    code = textwrap.dedent(
        """\
        a = 1




        b = 2
        """
    )
    path = _write(tmp_path / "gap.py", code)

    cfg_no_trim = Config(chunk_size=10_000, overlap_ratio=0.0, trim_gap_blank_lines=False)
    chunks_no_trim = list(TreeSitterChunker(cfg_no_trim).chunk(path))
    text_no_trim = "".join(c.text for c in chunks_no_trim)

    cfg_trim = Config(chunk_size=10_000, overlap_ratio=0.0, trim_gap_blank_lines=True)
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





