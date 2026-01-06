import os
import re
from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from functools import cache
from io import TextIOWrapper
from typing import Generator, Optional, Protocol

from pygments.lexer import Lexer
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

try:  # tree-sitter is optional at runtime for learning/debugging
    from tree_sitter import Node, Point  # type: ignore
    from tree_sitter_language_pack import SupportedLanguage, get_parser  # type: ignore

    _HAS_TREESITTER = True
except Exception:  # pragma: nocover
    Node = object  # type: ignore
    Point = object  # type: ignore
    SupportedLanguage = object  # type: ignore

    _HAS_TREESITTER = False


# Common extension -> tree-sitter language mapping.
# Keys must be supported by `tree_sitter_language_pack.get_parser()`.
# Patterns are regexes applied via `re.search(pattern, ext)` where `ext` has no leading dot.
DEFAULT_FILETYPE_MAP: dict[str, list[str]] = {
    "python": [r"^(py|pyi)$"],
    "lua": [r"^lua$"],
    "javascript": [r"^(js|mjs|cjs)$"],
    "typescript": [r"^(ts|tsx)$"],
    "java": [r"^java$"],
    "go": [r"^go$"],
    "rust": [r"^rs$"],
    "c": [r"^c$"],
    "cpp": [r"^(cc|cpp|cxx|hpp|hh|hxx)$"],
    "html": [r"^(html|htm)$"],
    "css": [r"^css$"],
    "sql": [r"^sql$"],
    "php": [r"^(php|phtml)$"],
    "ruby": [r"^rb$"],
    "json": [r"^json$"],
    "toml": [r"^toml$"],
    "yaml": [r"^(yml|yaml)$"],
    "bash": [r"^(sh|bash)$"],
    "markdown": [r"^(md|markdown)$"],
}


@dataclass
class Chunk:
    """
    Represents a piece of source text.

    Conventions (matching VectorCode):
    - rows are 1-indexed
    - columns are 0-indexed
    """

    text: str
    start: "Point | None" = None
    end: "Point | None" = None


@dataclass
class Config:
    chunk_size: int = 2500
    overlap_ratio: float = 0.2
    encoding: str = "utf8"  # use "_auto" to auto-detect with charset-normalizer
    chunk_filters: dict[str, list[str]] = None  # language -> patterns, "*" for default
    filetype_map: dict[str, list[str]] = None  # language -> [regex over extension]
    trim_gap_blank_lines: bool = True

    def __post_init__(self) -> None:
        if self.chunk_filters is None:
            self.chunk_filters = {}
        if self.filetype_map is None:
            # Default to a common mapping, while avoiding shared mutable defaults.
            self.filetype_map = {k: v.copy() for k, v in DEFAULT_FILETYPE_MAP.items()}
        if not (0 <= self.overlap_ratio < 1):
            raise ValueError("overlap_ratio must be in [0, 1).")


class Chunker(Protocol):
    def chunk(self, data: str) -> Generator[Chunk, None, None]: ...


class StringChunker:
    """
    Fallback chunker: fixed-size sliding window over a string.
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or Config()

    def chunk(self, data: str, *, start_pos: "Point | None" = None):
        if start_pos is None:
            start_pos = Point(row=1, column=0)  # type: ignore

        if self.config.chunk_size < 0:
            yield Chunk(
                text=data,
                start=start_pos,
                end=Point(  # type: ignore
                    row=data.count("\n") + start_pos.row,
                    column=len(data.split("\n")[-1]) - 1,
                ),
            )
            return

        # Pre-compute line offsets within `data` (like VectorCode's FileChunker),
        # so we can map absolute indices -> (row, col) efficiently.
        # Note: `start_pos.column` only affects the first line.
        lines = data.splitlines(True)
        line_offsets = [0]
        for line in lines:
            line_offsets.append(line_offsets[-1] + len(line))

        step_size = max(1, int(self.config.chunk_size * (1 - self.config.overlap_ratio)))
        i = 0
        while i < len(data):
            chunk_text = data[i : i + self.config.chunk_size]

            start_line_idx = bisect_right(line_offsets, i) - 1
            start_col_in_line = i - line_offsets[start_line_idx]
            chunk_start_row = start_pos.row + start_line_idx
            chunk_start_column = (
                start_pos.column + start_col_in_line if start_line_idx == 0 else start_col_in_line
            )

            end_pos = i + len(chunk_text)
            # Preserve the legacy end-point convention used by VectorCode's StringChunker:
            # - end.row advances by the number of newlines in the chunk
            # - if the chunk ends exactly at a line boundary (right after a '\n'),
            #   end.column is -1 on the next row.
            if end_pos > 0 and end_pos <= len(data) and data[end_pos - 1] == "\n":
                end_col_in_line = -1
                end_line_idx = bisect_right(line_offsets, end_pos) - 1
            else:
                end_line_idx = bisect_right(line_offsets, end_pos) - 1
                end_col_in_line = end_pos - line_offsets[end_line_idx] - 1

            chunk_end_row = start_pos.row + end_line_idx
            chunk_end_column = (
                start_pos.column + end_col_in_line if end_line_idx == 0 else end_col_in_line
            )

            yield Chunk(
                text=chunk_text,
                start=Point(row=chunk_start_row, column=chunk_start_column),  # type: ignore
                end=Point(row=chunk_end_row, column=chunk_end_column),  # type: ignore
            )

            if i + self.config.chunk_size >= len(data):
                break
            i += step_size


class TreeSitterChunker:
    """
    Minimal Tree-sitter chunker (learning-first):
    - input is a file path
    - try select parser by config.filetype_map or pygments guess
    - chunk by concatenating AST children until chunk_size
    - fallback to StringChunker when no parser is available

    Notes:
    - start/end rows follow the same convention as VectorCode (1-indexed rows).
    - chunk_filters are applied with re.match (prefix match), same as VectorCode.
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or Config()
        self._fallback = StringChunker(self.config)

    def _load_file_text(self, path: str) -> str:
        if self.config.encoding == "_auto":
            from charset_normalizer import from_path

            match = from_path(path).best()
            if match is None:
                raise UnicodeError(f"Failed to detect encoding for {path}")
            encoding = match.encoding
        else:
            encoding = self.config.encoding
        with open(path, encoding=encoding) as f:
            return f.read()

    @cache
    def _guess_lexer(self, path: str, content: str) -> Optional[Lexer]:
        try:
            return get_lexer_for_filename(path, content)
        except ClassNotFound:
            return None

    @cache
    def _build_filter_pattern(self, language: Optional[str]) -> str:
        patterns: list[str] = []
        if language and language in self.config.chunk_filters:
            patterns.extend(self.config.chunk_filters[language])
        else:
            patterns.extend(self.config.chunk_filters.get("*", []))
        if not patterns:
            return ""
        patterns = [f"(?:{p})" for p in patterns]
        return f"(?:{'|'.join(patterns)})"

    def _get_parser_from_config(self, file_path: str):
        if not _HAS_TREESITTER:
            return None, None
        if not self.config.filetype_map:
            return None, None

        ext = os.path.splitext(file_path)[1]
        if ext.startswith("."):
            ext = ext[1:]
        for _language, patterns in self.config.filetype_map.items():
            language = _language.lower()
            for pat in patterns:
                if re.search(pat, ext):
                    return get_parser(language), language  # type: ignore[arg-type]
        return None, None

    def _get_parser_by_guess(self, file_path: str, content: str):
        if not _HAS_TREESITTER:
            return None, None

        lexer = self._guess_lexer(file_path, content)
        if lexer is None:
            return None, None

        lang_names = [lexer.name, *lexer.aliases]
        for name in lang_names:
            try:
                parser = get_parser(name.lower())  # type: ignore[arg-type]
                return parser, name.lower()
            except LookupError:
                continue
        return None, None

    def _chunk_node(self, node: "Node", text_bytes: bytes) -> Generator[Chunk, None, None]:
        current_chunk = ""
        current_start: "Point | None" = None
        current_end: "Point | None" = None
        prev_node: "Node | None" = None

        def _normalize_gap_text(gap: str) -> str:
            if not self.config.trim_gap_blank_lines:
                return gap
            if not gap:
                return ""

            lines = gap.splitlines(keepends=True)
            kept = [ln for ln in lines if ln.strip() != ""]
            if kept:
                return "".join(kept)

            if "\n" in gap:
                return "\n"
            return " "

        # Leaf node: fallback to string chunking.
        if len(node.children) == 0 and getattr(node, "text", None):
            # Important: VectorCode passes node.start_point directly (potential 0/1-base mismatch).
            # For this learning wheel we normalize rows to 1-indexed.
            sp = node.start_point  # type: ignore[attr-defined]
            start_pos = Point(row=sp.row + 1, column=sp.column)  # type: ignore
            yield from self._fallback.chunk(node.text.decode(), start_pos=start_pos)  # type: ignore[attr-defined]
            return

        for child in node.children:
            child_bytes = text_bytes[child.start_byte : child.end_byte]
            child_text = child_bytes.decode()
            if self.config.chunk_size >= 0 and len(child_text) > self.config.chunk_size:
                if current_chunk:
                    assert current_start is not None
                    assert current_end is not None
                    yield Chunk(
                        text=current_chunk,
                        start=current_start,
                        end=current_end,
                    )
                    current_chunk = ""
                    current_start = None
                    current_end = None
                    prev_node = None

                yield from self._chunk_node(child, text_bytes)
                continue

            if not current_chunk:
                current_chunk = child_text
                sp = child.start_point
                current_start = Point(row=sp.row + 1, column=sp.column)  # type: ignore
                ep = child.end_point
                current_end = Point(row=ep.row + 1, column=ep.column)  # type: ignore
                prev_node = child
                continue

            # Preserve the exact whitespace/comments between sibling nodes by
            # appending the raw "gap" from the source.
            gap_text = ""
            if prev_node is not None:
                gap_bytes = text_bytes[prev_node.end_byte : child.start_byte]
                gap_text = _normalize_gap_text(gap_bytes.decode())

            # try append if fits (including the gap)
            if self.config.chunk_size < 0 or (
                len(current_chunk) + len(gap_text) + len(child_text) <= self.config.chunk_size
            ):
                current_chunk += gap_text + child_text
                prev_node = child
                ep = child.end_point
                current_end = Point(row=ep.row + 1, column=ep.column)  # type: ignore
                continue

            # otherwise flush and start new
            assert current_start is not None
            assert current_end is not None
            yield Chunk(
                text=current_chunk,
                start=current_start,
                end=current_end,
            )
            current_chunk = child_text
            sp = child.start_point
            current_start = Point(row=sp.row + 1, column=sp.column)  # type: ignore
            ep = child.end_point
            current_end = Point(row=ep.row + 1, column=ep.column)  # type: ignore
            prev_node = child

        if current_chunk:
            assert current_start is not None
            assert current_end is not None
            yield Chunk(
                text=current_chunk,
                start=current_start,
                end=current_end,
            )

    def chunk(self, path: str) -> Generator[Chunk, None, None]:
        if not os.path.isfile(path):
            raise FileNotFoundError(path)

        content = self._load_file_text(path)
        if self.config.chunk_size < 0 and content:
            lines = content.splitlines(True)
            end_col = len(lines[-1]) - 1 if lines else 0
            yield Chunk(
                text=content,
                start=Point(row=1, column=0),  # type: ignore
                end=Point(row=len(lines) if lines else 1, column=end_col),  # type: ignore
            )
            return

        parser, language = self._get_parser_from_config(path)
        if parser is None:
            parser, language = self._get_parser_by_guess(path, content)

        # No tree-sitter parser -> fallback to naive string chunking of whole file.
        if parser is None:
            yield from self._fallback.chunk(content, start_pos=Point(row=1, column=0))  # type: ignore
            return

        pattern_str = self._build_filter_pattern(language)
        content_bytes = content.encode()
        tree = parser.parse(content_bytes)
        chunks = self._chunk_node(tree.root_node, content_bytes)

        if pattern_str:
            rx = re.compile(pattern_str)
            for c in chunks:
                if rx.match(c.text) is None:
                    yield c
        else:
            yield from chunks


