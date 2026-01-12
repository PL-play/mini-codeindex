import hashlib
import os
import re
from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
from enum import Enum
from functools import cache
from io import TextIOWrapper
from typing import Generator, Optional, Protocol, Union

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


class ScopeKind(str, Enum):
    FILE = "file"

    # Unified "type container" across languages (class/interface/enum/record/struct/trait...).
    TYPE = "type"

    FUNCTION = "function"


@dataclass
class Scope:
    kind: ScopeKind
    name: str


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

    # Optional metadata
    path: Optional[str] = None
    sha256: Optional[str] = None
    language: Optional[str] = None

    # Full scope path from outermost -> innermost.
    scope_path: list[Scope] = field(default_factory=list)

    # If a chunk contains multiple inner scopes (e.g. class A method m + method n
    # when boundary is at class), keep scope_path truncated to the configured
    # boundary prefix and record the distinct inner scopes here.
    contained_scopes: list[Scope] = field(default_factory=list)


@dataclass
class Config:
    chunk_size: int = 2500
    overlap_ratio: float = 0.2
    encoding: str = "utf8"  # use "_auto" to auto-detect with charset-normalizer
    chunk_filters: dict[str, list[str]] = None  # language -> patterns, "*" for default
    filetype_map: dict[str, list[str]] = None  # language -> [regex over extension]
    trim_gap_blank_lines: bool = True
    # Boundary controls BOTH:
    # - how scope_path is truncated (outer containers retained up to the boundary)
    # - whether chunks are allowed to mix across different scopes at that boundary
    #
    # Must be one of: FILE, TYPE, FUNCTION.
    boundary: Optional[Union[ScopeKind, str]] = None

    def __post_init__(self) -> None:
        if self.chunk_filters is None:
            self.chunk_filters = {}
        if self.filetype_map is None:
            # Default to a common mapping, while avoiding shared mutable defaults.
            self.filetype_map = {k: v.copy() for k, v in DEFAULT_FILETYPE_MAP.items()}
        # Normalize/validate boundary; invalid -> default to FILE.
        try:
            if self.boundary is None:
                self.boundary = ScopeKind.FILE
            elif isinstance(self.boundary, str):
                self.boundary = ScopeKind(self.boundary)
        except Exception:
            self.boundary = ScopeKind.FILE
        if self.boundary not in {ScopeKind.FILE, ScopeKind.TYPE, ScopeKind.FUNCTION}:
            self.boundary = ScopeKind.FILE
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

    def _load_file(self, path: str) -> tuple[str, bytes]:
        raw = open(path, "rb").read()
        if self.config.encoding == "_auto":
            from charset_normalizer import from_bytes

            match = from_bytes(raw).best()
            if match is None or match.encoding is None:
                raise UnicodeError(f"Failed to detect encoding for {path}")
            encoding = match.encoding
        else:
            encoding = self.config.encoding
        return raw.decode(encoding), raw

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

    def _scope_of_node(
        self,
        node: "Node",
        *,
        language: Optional[str],
        text_bytes: bytes,
        scope_stack: list[Scope],
    ) -> Optional[Scope]:
        if language is None or not _HAS_TREESITTER:
            return None
        lang = language.lower()
        t = getattr(node, "type", None)

        def _name_from_field() -> Optional[str]:
            name_node = node.child_by_field_name("name")  # type: ignore[attr-defined]
            if name_node is None:
                return None
            try:
                return text_bytes[name_node.start_byte : name_node.end_byte].decode()
            except Exception:
                return None

        if lang == "python":
            if t == "class_definition":
                n = _name_from_field()
                return Scope(kind=ScopeKind.TYPE, name=n) if n else None
            if t in {"function_definition", "async_function_definition"}:
                n = _name_from_field()
                if not n:
                    return None
                # Methods are also functions for our boundary purposes.
                return Scope(kind=ScopeKind.FUNCTION, name=n)

        if lang == "java":
            if t in {
                "class_declaration",
                "interface_declaration",
                "enum_declaration",
                "record_declaration",
            }:
                n = _name_from_field()
                return Scope(kind=ScopeKind.TYPE, name=n) if n else None
            if t in {"method_declaration", "constructor_declaration"}:
                n = _name_from_field()
                return Scope(kind=ScopeKind.FUNCTION, name=n) if n else None

        return None

    def _boundary_prefix(self, scope_path: list[Scope]) -> list[Scope]:
        """Return the scope prefix up to the configured boundary.

        Ordering is conceptually: FILE -> TYPE -> FUNCTION.
        For example:
        - boundary=FILE keeps only FILE (if present)
        - boundary=TYPE keeps FILE/TYPE up to TYPE (if present), else falls back to FILE
        - boundary=FUNCTION keeps FILE/TYPE/FUNCTION up to FUNCTION (if present), else falls back to TYPE/FILE
        """
        b = self.config.boundary
        if b == ScopeKind.FILE:
            allowed = {ScopeKind.FILE}
        elif b == ScopeKind.TYPE:
            allowed = {ScopeKind.FILE, ScopeKind.TYPE}
        else:  # FUNCTION
            allowed = {ScopeKind.FILE, ScopeKind.TYPE, ScopeKind.FUNCTION}

        last_idx = -1
        for i, s in enumerate(scope_path):
            if s.kind in allowed:
                last_idx = i
        if last_idx < 0:
            return []
        # If our boundary kind wasn't present, fall back to the innermost available allowed scope.
        # This makes boundary=FUNCTION still produce FILE-only prefixes for top-level statements.
        return scope_path[: last_idx + 1]

    def _inner_scopes_for_chunk(self, *, full_scope_path: list[Scope], boundary_prefix: list[Scope]) -> list[Scope]:
        """Return a best-effort list of inner scopes beyond the boundary prefix.

        We record the first scope immediately under the boundary (e.g., method/function),
        which is typically what callers care about when a chunk mixes siblings.
        """

        if len(full_scope_path) <= len(boundary_prefix):
            return []
        return [full_scope_path[len(boundary_prefix)]]

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

    def _chunk_node(
        self,
        node: "Node",
        text_bytes: bytes,
        *,
        language: Optional[str],
        scope_stack: list[Scope],
    ) -> Generator[Chunk, None, None]:
        current_chunk = ""
        current_start: "Point | None" = None
        current_end: "Point | None" = None
        current_scope_path: list[Scope] = []
        current_contained: list[Scope] = []
        prev_node: "Node | None" = None

        local_scope = self._scope_of_node(node, language=language, text_bytes=text_bytes, scope_stack=scope_stack)
        if local_scope is not None:
            scope_stack = [*scope_stack, local_scope]

        def _emit_node_as_text_chunks(
            *,
            target_node: "Node",
            boundary_prefix: list[Scope],
            contained_scopes: list[Scope],
        ) -> Generator[Chunk, None, None]:
            """
            Emit target_node.text as:
            - a single chunk if it fits chunk_size
            - otherwise, fallback StringChunker with overlap
            """
            if getattr(target_node, "text", None) is None:
                return
            sp = target_node.start_point
            start_pos = Point(row=sp.row + 1, column=sp.column)  # type: ignore
            node_text = target_node.text.decode()
            if self.config.chunk_size < 0 or len(node_text) <= self.config.chunk_size:
                ep = target_node.end_point
                yield Chunk(
                    text=node_text,
                    start=start_pos,
                    end=Point(row=ep.row + 1, column=ep.column),  # type: ignore
                    scope_path=boundary_prefix,
                    contained_scopes=contained_scopes,
                )
                return
            for c in self._fallback.chunk(node_text, start_pos=start_pos):
                yield Chunk(
                    text=c.text,
                    start=c.start,
                    end=c.end,
                    scope_path=boundary_prefix,
                    contained_scopes=contained_scopes,
                )

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
            full_scope_path = scope_stack.copy()
            boundary_prefix = self._boundary_prefix(full_scope_path)
            contained_scopes: list[Scope] = []
            for s in self._inner_scopes_for_chunk(full_scope_path=full_scope_path, boundary_prefix=boundary_prefix):
                if (s.kind, s.name) not in {(x.kind, x.name) for x in contained_scopes}:
                    contained_scopes.append(s)
            for c in self._fallback.chunk(node.text.decode(), start_pos=start_pos):  # type: ignore[attr-defined]
                yield Chunk(
                    text=c.text,
                    start=c.start,
                    end=c.end,
                    scope_path=boundary_prefix,
                    contained_scopes=contained_scopes,
                )
            return

        for child in node.children:
            child_bytes = text_bytes[child.start_byte : child.end_byte]
            child_text = child_bytes.decode()
            child_type = getattr(child, "type", None)

            child_scope = self._scope_of_node(
                child, language=language, text_bytes=text_bytes, scope_stack=scope_stack
            )

            # boundary=FUNCTION: if a TYPE node is small enough, emit it as ONE chunk.
            # This avoids fragmentation like:
            #   interface I {  (chunk)
            #   {              (chunk)
            #   int x();       (chunk)
            #   }              (chunk)
            # while still preserving function-level information via contained_scopes.
            if (
                child_scope is not None
                and child_scope.kind == ScopeKind.TYPE
                and self.config.boundary == ScopeKind.FUNCTION
                and getattr(child, "text", None) is not None
                and (self.config.chunk_size < 0 or len(child.text.decode()) <= self.config.chunk_size)  # type: ignore[attr-defined]
            ):
                # Flush any pending non-scope text in the current node.
                if current_chunk:
                    assert current_start is not None
                    assert current_end is not None
                    yield Chunk(
                        text=current_chunk,
                        start=current_start,
                        end=current_end,
                        scope_path=current_scope_path,
                        contained_scopes=current_contained,
                    )
                    current_chunk = ""
                    current_start = None
                    current_end = None
                    current_scope_path = []
                    current_contained = []
                    prev_node = None

                # Collect inner FUNCTION scopes for contained_scopes (one-level precision is fine).
                contained: list[Scope] = []

                def _collect_functions(n: "Node", stack: list[Scope]) -> None:
                    sc = self._scope_of_node(
                        n, language=language, text_bytes=text_bytes, scope_stack=stack
                    )
                    if sc is not None:
                        if sc.kind == ScopeKind.FUNCTION and (sc.kind, sc.name) not in {
                            (x.kind, x.name) for x in contained
                        }:
                            contained.append(sc)
                        stack = [*stack, sc]
                    for ch in getattr(n, "children", []):
                        _collect_functions(ch, stack)

                _collect_functions(child, [*scope_stack, child_scope])

                full_scope_path = [*scope_stack, child_scope]
                boundary_prefix = self._boundary_prefix(full_scope_path)
                yield from _emit_node_as_text_chunks(
                    target_node=child,
                    boundary_prefix=boundary_prefix,
                    contained_scopes=contained,
                )
                prev_node = child
                continue

            # boundary=TYPE: emit each TYPE node as a whole chunk (or string-chunked if too large).
            if child_scope is not None and child_scope.kind == ScopeKind.TYPE and self.config.boundary == ScopeKind.TYPE:
                if current_chunk:
                    assert current_start is not None
                    assert current_end is not None
                    yield Chunk(
                        text=current_chunk,
                        start=current_start,
                        end=current_end,
                        scope_path=current_scope_path,
                        contained_scopes=current_contained,
                    )
                    current_chunk = ""
                    current_start = None
                    current_end = None
                    current_scope_path = []
                    current_contained = []
                    prev_node = None

                full_scope_path = [*scope_stack, child_scope]
                boundary_prefix = self._boundary_prefix(full_scope_path)
                yield from _emit_node_as_text_chunks(
                    target_node=child,
                    boundary_prefix=boundary_prefix,
                    contained_scopes=[],
                )
                prev_node = child
                continue

            # Boundary-driven recursion:
            # - boundary=FILE: do NOT recurse solely because we saw a scope node; allow mixing.
            # - boundary=TYPE: recurse into TYPE nodes so each type is chunked independently.
            # - boundary=FUNCTION: recurse into TYPE and FUNCTION nodes so each function/method is chunked independently.
            should_recurse_for_boundary = False
            if child_scope is not None:
                if child_scope.kind == ScopeKind.TYPE and self.config.boundary == ScopeKind.FUNCTION:
                    # For FUNCTION boundary we traverse into TYPE containers to discover functions.
                    should_recurse_for_boundary = True
                if child_scope.kind == ScopeKind.FUNCTION and self.config.boundary == ScopeKind.FUNCTION:
                    # boundary=FUNCTION: emit each FUNCTION node as a whole chunk (or string-chunked if too large),
                    # and do NOT recurse into it.
                    if current_chunk:
                        assert current_start is not None
                        assert current_end is not None
                        yield Chunk(
                            text=current_chunk,
                            start=current_start,
                            end=current_end,
                            scope_path=current_scope_path,
                            contained_scopes=current_contained,
                        )
                        current_chunk = ""
                        current_start = None
                        current_end = None
                        current_scope_path = []
                        current_contained = []
                        prev_node = None

                    full_scope_path = [*scope_stack, child_scope]
                    boundary_prefix = self._boundary_prefix(full_scope_path)
                    yield from _emit_node_as_text_chunks(
                        target_node=child,
                        boundary_prefix=boundary_prefix,
                        contained_scopes=[],
                    )
                    prev_node = child
                    continue

            if should_recurse_for_boundary:
                if current_chunk:
                    assert current_start is not None
                    assert current_end is not None
                    yield Chunk(
                        text=current_chunk,
                        start=current_start,
                        end=current_end,
                        scope_path=current_scope_path,
                        contained_scopes=current_contained,
                    )
                    current_chunk = ""
                    current_start = None
                    current_end = None
                    current_scope_path = []
                    current_contained = []

                yield from self._chunk_node(child, text_bytes, language=language, scope_stack=scope_stack)
                prev_node = child
                continue

            # Recurse into structural container nodes that may contain scoped declarations.
            if language is not None:
                # Only recurse into containers when boundary is at least TYPE.
                if self.config.boundary != ScopeKind.FILE:
                    lang_lower = language.lower()
                    java_containers = {"class_body", "interface_body", "enum_body", "record_body"}
                    python_containers = {"block"}
                    if (lang_lower == "java" and child_type in java_containers) or (
                        lang_lower == "python" and child_type in python_containers
                    ):
                        if current_chunk:
                            assert current_start is not None
                            assert current_end is not None
                            yield Chunk(
                                text=current_chunk,
                                start=current_start,
                                end=current_end,
                                scope_path=current_scope_path,
                                contained_scopes=current_contained,
                            )
                            current_chunk = ""
                            current_start = None
                            current_end = None
                            current_scope_path = []
                            current_contained = []

                        yield from self._chunk_node(
                            child, text_bytes, language=language, scope_stack=scope_stack
                        )
                        prev_node = child
                        continue

            if self.config.chunk_size >= 0 and len(child_text) > self.config.chunk_size:
                if current_chunk:
                    assert current_start is not None
                    assert current_end is not None
                    yield Chunk(
                        text=current_chunk,
                        start=current_start,
                        end=current_end,
                        scope_path=current_scope_path,
                        contained_scopes=current_contained,
                    )
                    current_chunk = ""
                    current_start = None
                    current_end = None
                    current_scope_path = []
                    current_contained = []
                    prev_node = None

                yield from self._chunk_node(child, text_bytes, language=language, scope_stack=scope_stack)
                continue
            child_scope_path = scope_stack.copy()
            if child_scope is not None:
                child_scope_path.append(child_scope)

            child_boundary = self._boundary_prefix(child_scope_path)
            child_inner = self._inner_scopes_for_chunk(full_scope_path=child_scope_path, boundary_prefix=child_boundary)

            if not current_chunk:
                current_chunk = child_text
                sp = child.start_point
                current_start = Point(row=sp.row + 1, column=sp.column)  # type: ignore
                ep = child.end_point
                current_end = Point(row=ep.row + 1, column=ep.column)  # type: ignore
                current_scope_path = child_boundary
                current_contained = []
                for s in child_inner:
                    if (s.kind, s.name) not in {(x.kind, x.name) for x in current_contained}:
                        current_contained.append(s)
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
                # If the next child is under a different *boundary*, flush first.
                if current_scope_path != child_boundary and current_chunk:
                    assert current_start is not None
                    assert current_end is not None
                    yield Chunk(
                        text=current_chunk,
                        start=current_start,
                        end=current_end,
                        scope_path=current_scope_path,
                        contained_scopes=current_contained,
                    )
                    current_chunk = ""
                    current_start = None
                    current_end = None
                    prev_node = None

                    current_chunk = child_text
                    sp = child.start_point
                    current_start = Point(row=sp.row + 1, column=sp.column)  # type: ignore
                    ep = child.end_point
                    current_end = Point(row=ep.row + 1, column=ep.column)  # type: ignore
                    current_scope_path = child_boundary
                    current_contained = []
                    for s in child_inner:
                        if (s.kind, s.name) not in {(x.kind, x.name) for x in current_contained}:
                            current_contained.append(s)
                    prev_node = child
                    continue

                # Same boundary: allow mixing. Record inner scope(s).
                for s in child_inner:
                    if (s.kind, s.name) not in {(x.kind, x.name) for x in current_contained}:
                        current_contained.append(s)

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
                scope_path=current_scope_path,
                contained_scopes=current_contained,
            )
            current_chunk = child_text
            sp = child.start_point
            current_start = Point(row=sp.row + 1, column=sp.column)  # type: ignore
            ep = child.end_point
            current_end = Point(row=ep.row + 1, column=ep.column)  # type: ignore
            current_scope_path = child_boundary
            current_contained = []
            for s in child_inner:
                if (s.kind, s.name) not in {(x.kind, x.name) for x in current_contained}:
                    current_contained.append(s)
            prev_node = child

        if current_chunk:
            assert current_start is not None
            assert current_end is not None
            yield Chunk(
                text=current_chunk,
                start=current_start,
                end=current_end,
                scope_path=current_scope_path,
                contained_scopes=current_contained,
            )

    def chunk_str(
        self,
        content: str,
        *,
        path: Optional[str] = None,
        language: Optional[str] = None,
        start_pos: Optional["Point"] = None,
        content_bytes: Optional[bytes] = None,
    ) -> Generator[Chunk, None, None]:
        """Chunk a raw string.

        Parser selection priority:
        1) If `path` is provided, try config.filetype_map then pygments guessing.
        2) Else if `language` is provided, try `tree_sitter_language_pack.get_parser(language)`.
        3) Else fall back to `StringChunker`.

        `start_pos` controls the start Point for the fallback StringChunker only.
        """

        if start_pos is None:
            start_pos = Point(row=1, column=0)  # type: ignore

        if content_bytes is None:
            content_bytes = content.encode()

        sha256_value = hashlib.sha256(content_bytes).hexdigest() if path is not None else None

        module_value: Optional[str] = None
        if path is not None:
            base = os.path.basename(path)
            module_value = os.path.splitext(base)[0]

        # Resolve language as early as possible so even the whole-file fast-path
        # can still report `language`.
        parser = None
        lang = None
        if path is not None:
            parser, lang = self._get_parser_from_config(path)
            if parser is None:
                parser, lang = self._get_parser_by_guess(path, content)
        elif language is not None:
            lang = language.lower()

        if self.config.chunk_size < 0 and content:
            # Yield the whole content as one chunk.
            lines = content.splitlines(True)
            end_col = len(lines[-1]) - 1 if lines else 0
            end_row = start_pos.row + (len(lines) - 1 if lines else 0)
            end_column = start_pos.column + end_col if len(lines) <= 1 else end_col
            yield Chunk(
                text=content,
                start=start_pos,
                end=Point(row=end_row, column=end_column),  # type: ignore
                path=path,
                sha256=sha256_value,
                language=lang,
                scope_path=[
                    *( [Scope(kind=ScopeKind.FILE, name=module_value)] if module_value else [] ),
                ],
                contained_scopes=[],
            )
            return

        if parser is None and lang is not None and _HAS_TREESITTER:
            try:
                parser = get_parser(lang)  # type: ignore[arg-type]
            except LookupError:
                parser = None
                lang = None

        # No tree-sitter parser -> fallback to naive string chunking.
        if parser is None:
            for c in self._fallback.chunk(content, start_pos=start_pos):
                yield Chunk(
                    text=c.text,
                    start=c.start,
                    end=c.end,
                    path=path,
                    sha256=sha256_value,
                    language=lang,
                    scope_path=[
                        *( [Scope(kind=ScopeKind.FILE, name=module_value)] if module_value else [] ),
                    ],
                    contained_scopes=[],
                )
            return

        pattern_str = self._build_filter_pattern(lang)

        # boundary=FILE => pure text chunking.
        #
        # Requirements:
        # - do NOT scope-split the file
        # - chunk_filters should not delete useful code (line-level masking instead)
        # - each chunk still needs contained_scopes (TYPE/FUNCTION) at good precision
        if self.config.boundary == ScopeKind.FILE:
            tree = parser.parse(content_bytes)

            # (1) Prepare line-level masking regex list
            patterns: list[str] = []
            if lang and lang in self.config.chunk_filters:
                patterns = self.config.chunk_filters.get(lang, [])
            else:
                patterns = self.config.chunk_filters.get("*", [])

            line_rx = re.compile(f"(?:{'|'.join(f'(?:{p})' for p in patterns)})") if patterns else None

            def _mask_line(line: str) -> str:
                # Preserve length and newline to keep (row,col) stable.
                if not line:
                    return line
                if line.endswith("\n"):
                    body, nl = line[:-1], "\n"
                else:
                    body, nl = line, ""
                return (" " * len(body)) + nl

            file_text = content
            if line_rx is not None:
                masked_lines: list[str] = []
                for ln in content.splitlines(keepends=True):
                    if line_rx.match(ln.lstrip()) is not None:
                        masked_lines.append(_mask_line(ln))
                    else:
                        masked_lines.append(ln)
                file_text = "".join(masked_lines)

            # NOTE: We intentionally do NOT apply trim_gap_blank_lines in FILE mode,
            # because FILE mode is defined as "pure text" and we also want positions
            # to remain aligned with the original file for contained_scopes mapping.

            # (2) Collect scope ranges (TYPE/FUNCTION) from the parsed tree.
            scope_ranges: list[tuple[Scope, "Point", "Point"]] = []

            def _dfs(n: "Node", stack: list[Scope]) -> None:
                sc = self._scope_of_node(
                    n, language=lang, text_bytes=content_bytes, scope_stack=stack
                )
                if sc is not None:
                    sp = n.start_point
                    ep = n.end_point
                    scope_ranges.append(
                        (
                            sc,
                            Point(row=sp.row + 1, column=sp.column),  # type: ignore
                            Point(row=ep.row + 1, column=ep.column),  # type: ignore
                        )
                    )
                    stack = [*stack, sc]
                for ch in getattr(n, "children", []):
                    _dfs(ch, stack)

            _dfs(tree.root_node, [])

            def _pt_key(p: "Point") -> tuple[int, int]:
                return int(p.row), int(p.column)

            def _ranges_overlap(a0: "Point", a1: "Point", b0: "Point", b1: "Point") -> bool:
                return not (_pt_key(a1) < _pt_key(b0) or _pt_key(b1) < _pt_key(a0))

            for c in self._fallback.chunk(file_text, start_pos=start_pos):
                contained: list[Scope] = []
                for sc, s0, s1 in scope_ranges:
                    if _ranges_overlap(c.start, c.end, s0, s1):  # type: ignore[arg-type]
                        if (sc.kind, sc.name) not in {(x.kind, x.name) for x in contained}:
                            contained.append(sc)
                yield Chunk(
                    text=c.text,
                    start=c.start,
                    end=c.end,
                    path=path,
                    sha256=sha256_value,
                    language=lang,
                    scope_path=[
                        *( [Scope(kind=ScopeKind.FILE, name=module_value)] if module_value else [] ),
                    ],
                    contained_scopes=contained,
                )
            return

        tree = parser.parse(content_bytes)

        base_scopes: list[Scope] = []
        if module_value:
            # Keep name as file-stem for stability across extensions.
            base_scopes.append(Scope(kind=ScopeKind.FILE, name=module_value))

        chunks = self._chunk_node(tree.root_node, content_bytes, language=lang, scope_stack=base_scopes)

        if pattern_str:
            rx = re.compile(pattern_str)
            for c in chunks:
                if rx.match(c.text) is None:
                    yield Chunk(
                        text=c.text,
                        start=c.start,
                        end=c.end,
                        path=path,
                        sha256=sha256_value,
                        language=lang,
                        scope_path=c.scope_path,
                        contained_scopes=c.contained_scopes,
                    )
        else:
            for c in chunks:
                yield Chunk(
                    text=c.text,
                    start=c.start,
                    end=c.end,
                    path=path,
                    sha256=sha256_value,
                    language=lang,
                    scope_path=c.scope_path,
                    contained_scopes=c.contained_scopes,
                )

    def chunk(self, path: str) -> Generator[Chunk, None, None]:
        if not os.path.isfile(path):
            raise FileNotFoundError(path)

        content, raw = self._load_file(path)
        yield from self.chunk_str(
            content,
            path=path,
            start_pos=Point(row=1, column=0),  # type: ignore
            content_bytes=raw,
        )


