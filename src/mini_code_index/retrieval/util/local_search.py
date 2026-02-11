from __future__ import annotations

import ast
import fnmatch
import json
import math
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, TypedDict


class TextSearchResult(TypedDict):
    path: str
    line: int
    col: int
    snippet: str
    context_before: str
    context_after: str


class PathResult(TypedDict):
    path: str


class SymbolResult(TypedDict):
    symbol: str
    kind: str
    path: str
    line: int


class ReferenceResult(TypedDict):
    path: str
    line: int
    snippet: str


class FileMetadata(TypedDict):
    size: int
    mtime: str
    encoding: str


class LanguageStatsResult(TypedDict):
    ext: str
    files: int
    lines: int


def _iter_files(
    root_dir: str,
    *,
    include_glob: Optional[str] = None,
    exclude_glob: Optional[str] = None,
) -> Iterable[Tuple[Path, str]]:
    root = Path(root_dir).resolve()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if include_glob and not fnmatch.fnmatch(rel, include_glob):
            continue
        if exclude_glob and fnmatch.fnmatch(rel, exclude_glob):
            continue
        yield path, rel


def _read_text_lines(path: Path) -> List[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore").splitlines()


def text_search(
    root_dir: str,
    query: str,
    *,
    is_regex: bool = False,
    include_glob: Optional[str] = None,
    exclude_glob: Optional[str] = None,
    max_results: int = 20,
    context_lines: int = 2,
) -> List[TextSearchResult]:
    pattern = query if is_regex else re.escape(query)
    regex = re.compile(pattern)
    results: List[TextSearchResult] = []

    for path, rel in _iter_files(root_dir, include_glob=include_glob, exclude_glob=exclude_glob):
        lines = _read_text_lines(path)
        for idx, line in enumerate(lines, start=1):
            for match in regex.finditer(line):
                before_start = max(0, idx - 1 - context_lines)
                after_end = min(len(lines), idx - 1 + context_lines + 1)
                context_before = "\n".join(lines[before_start : idx - 1])
                context_after = "\n".join(lines[idx:after_end])
                results.append(
                    {
                        "path": rel,
                        "line": idx,
                        "col": match.start() + 1,
                        "snippet": line.strip(),
                        "context_before": context_before,
                        "context_after": context_after,
                    }
                )
                if len(results) >= max_results:
                    return results
    return results


def path_glob(root_dir: str, pattern: str, *, max_results: int = 500) -> List[PathResult]:
    root = Path(root_dir).resolve()
    matches: List[PathResult] = []
    for path in root.glob(pattern):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        matches.append({"path": rel})
        if len(matches) >= max_results:
            break
    return matches


def tree_summary(
    root_dir: str,
    *,
    max_depth: int = 4,
    include_files: bool = True,
    exclude_glob: Optional[str] = None,
) -> Dict[str, str]:
    root = Path(root_dir).resolve()

    def _walk(current: Path, depth: int) -> Dict[str, object]:
        node: Dict[str, object] = {
            "name": current.name,
            "path": current.relative_to(root).as_posix() if current != root else root.name,
            "type": "dir" if current.is_dir() else "file",
        }
        if not current.is_dir():
            return node
        if depth >= max_depth:
            node["children"] = []
            return node

        children: List[Dict[str, object]] = []
        entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        for entry in entries:
            rel = entry.relative_to(root).as_posix()
            if exclude_glob and fnmatch.fnmatch(rel, exclude_glob):
                continue
            if entry.is_file() and not include_files:
                continue
            children.append(_walk(entry, depth + 1))
        node["children"] = children
        return node

    tree = _walk(root, 0)
    return {"tree": tree}


def read_file_range(path: str, start_line: int, end_line: int) -> Dict[str, str]:
    file_path = Path(path)
    lines = _read_text_lines(file_path)
    start = max(1, start_line)
    end = min(len(lines), end_line)
    content = "\n".join(lines[start - 1 : end])
    return {"content": content}


def symbol_index(
    root_dir: str,
    *,
    languages: Optional[List[str]] = None,
    include_glob: Optional[str] = None,
) -> List[SymbolResult]:
    allowed_languages = set(lang.lower() for lang in languages) if languages else None
    results: List[SymbolResult] = []

    for path, rel in _iter_files(root_dir, include_glob=include_glob):
        ext = path.suffix.lower()
        if allowed_languages is not None:
            if ext == ".py" and "python" not in allowed_languages:
                continue
            if ext in {".js", ".jsx"} and "javascript" not in allowed_languages:
                continue
            if ext in {".ts", ".tsx"} and "typescript" not in allowed_languages:
                continue
            if ext == ".java" and "java" not in allowed_languages:
                continue
        if ext == ".py":
            results.extend(_python_symbols(path, rel))
        elif ext in {".js", ".jsx", ".ts", ".tsx"}:
            results.extend(_js_ts_symbols(path, rel))
        elif ext == ".java":
            results.extend(_java_symbols(path, rel))
    return results


def find_references(
    root_dir: str,
    symbol: str,
    *,
    is_regex: bool = False,
    include_glob: Optional[str] = None,
    max_results: int = 200,
) -> List[ReferenceResult]:
    pattern = symbol if is_regex else rf"\b{re.escape(symbol)}\b"
    regex = re.compile(pattern)
    results: List[ReferenceResult] = []

    for path, rel in _iter_files(root_dir, include_glob=include_glob):
        lines = _read_text_lines(path)
        for idx, line in enumerate(lines, start=1):
            if regex.search(line):
                results.append({"path": rel, "line": idx, "snippet": line.strip()})
                if len(results) >= max_results:
                    return results
    return results


def file_metadata(path: str) -> FileMetadata:
    file_path = Path(path)
    stat = file_path.stat()
    encoding = _detect_encoding(file_path)
    return {
        "size": stat.st_size,
        "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "encoding": encoding,
    }


def language_stats(
    root_dir: str, *, include_glob: Optional[str] = None
) -> List[LanguageStatsResult]:
    stats: Dict[str, LanguageStatsResult] = {}
    for path, _rel in _iter_files(root_dir, include_glob=include_glob):
        ext = path.suffix.lower() or "<no_ext>"
        lines = _read_text_lines(path)
        entry = stats.setdefault(ext, {"ext": ext, "files": 0, "lines": 0})
        entry["files"] += 1
        entry["lines"] += len(lines)
    return sorted(stats.values(), key=lambda item: item["ext"])


def _python_symbols(path: Path, rel: str) -> List[SymbolResult]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    results: List[SymbolResult] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            results.append({"symbol": node.name, "kind": "function", "path": rel, "line": node.lineno})
        elif isinstance(node, ast.AsyncFunctionDef):
            results.append({"symbol": node.name, "kind": "async_function", "path": rel, "line": node.lineno})
        elif isinstance(node, ast.ClassDef):
            results.append({"symbol": node.name, "kind": "class", "path": rel, "line": node.lineno})
    return results


def _js_ts_symbols(path: Path, rel: str) -> List[SymbolResult]:
    results: List[SymbolResult] = []
    lines = _read_text_lines(path)
    function_pattern = re.compile(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(")
    class_pattern = re.compile(r"\bclass\s+([A-Za-z_$][\w$]*)\b")
    arrow_pattern = re.compile(
        r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\(?.*?\)?\s*=>"
    )
    for idx, line in enumerate(lines, start=1):
        for match in function_pattern.finditer(line):
            results.append({"symbol": match.group(1), "kind": "function", "path": rel, "line": idx})
        for match in class_pattern.finditer(line):
            results.append({"symbol": match.group(1), "kind": "class", "path": rel, "line": idx})
        for match in arrow_pattern.finditer(line):
            results.append({"symbol": match.group(1), "kind": "function", "path": rel, "line": idx})
    return results


def _java_symbols(path: Path, rel: str) -> List[SymbolResult]:
    results: List[SymbolResult] = []
    lines = _read_text_lines(path)
    class_pattern = re.compile(r"\b(class|interface|enum)\s+([A-Za-z_][\w]*)")
    for idx, line in enumerate(lines, start=1):
        for match in class_pattern.finditer(line):
            results.append({"symbol": match.group(2), "kind": match.group(1), "path": rel, "line": idx})
    return results


def _detect_encoding(path: Path) -> str:
    try:
        path.read_text(encoding="utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "binary"


def _to_json_str(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _paged_response(items: List[object], *, page: int, page_size: int) -> Dict[str, object]:
    safe_page = max(1, int(page))
    safe_page_size = max(1, int(page_size))
    total_count = len(items)
    total_pages = max(1, math.ceil(total_count / safe_page_size)) if total_count else 1
    start = (safe_page - 1) * safe_page_size
    end = start + safe_page_size
    page_items = items[start:end]
    return {
        "page": safe_page,
        "page_size": safe_page_size,
        "total_count": total_count,
        "total_pages": total_pages,
        "items": page_items,
    }


async def text_search_tool(
    root_dir: str,
    query: str,
    *,
    is_regex: bool = False,
    include_glob: Optional[str] = None,
    exclude_glob: Optional[str] = None,
    max_results: int = 30,
    context_lines: int = 2,
    page: int = 1,
    page_size: int = 50,
) -> str:
    """LLM Tool: Search text within a directory and return JSON as a string.

    Args:
        root_dir: Root directory to scan.
        query: Search text or regex pattern.
        is_regex: If True, treat query as regex; otherwise escape as literal text.
        include_glob: Optional glob to include files (relative to root_dir).
        exclude_glob: Optional glob to exclude files (relative to root_dir).
        max_results: Maximum number of matches to return.
        context_lines: Number of context lines before/after the matched line.

    Returns:
        JSON string encoding a page object:
            {
              "page": int,
              "page_size": int,
              "total_count": int,
              "total_pages": int,
              "items": [ ... ]
            }
        Each item contains: path, line, col, snippet, context_before, context_after.

    Usage:
        await text_search_tool("/repo", "embedding", include_glob="**/*.py", page=1, page_size=50)
    """
    results = text_search(
        root_dir,
        query,
        is_regex=is_regex,
        include_glob=include_glob,
        exclude_glob=exclude_glob,
        max_results=max_results,
        context_lines=context_lines,
    )
    return _to_json_str(_paged_response(results, page=page, page_size=page_size))


async def path_glob_tool(
    root_dir: str,
    pattern: str,
    *,
    max_results: int = 500,
    page: int = 1,
    page_size: int = 200,
) -> str:
    """LLM Tool: Match file paths by glob pattern and return JSON as a string.

    Args:
        root_dir: Root directory to scan.
        pattern: Glob pattern (relative to root_dir), e.g. "**/*.py".
        max_results: Maximum number of paths to return.

    Returns:
        JSON string encoding a page object with items: [{"path": ...}].

    Usage:
        await path_glob_tool("/repo", "src/**/*.ts", page=1, page_size=200)
    """
    results = path_glob(root_dir, pattern, max_results=max_results)
    return _to_json_str(_paged_response(results, page=page, page_size=page_size))


async def tree_summary_tool(
    root_dir: str,
    *,
    max_depth: int = 4,
    include_files: bool = True,
    exclude_glob: Optional[str] = None,
) -> str:
    """LLM Tool: Build a directory tree summary and return JSON as a string.

    Args:
        root_dir: Root directory to summarize.
        max_depth: Maximum depth to traverse.
        include_files: If True, include files; otherwise show directories only.
        exclude_glob: Optional glob to exclude entries (relative to root_dir).

    Returns:
        JSON string encoding an object: {"tree": {...}} with a structured tree.
        Each node contains: name, path, type, and optional children.

    Usage:
        await tree_summary_tool("/repo", max_depth=3, exclude_glob="**/node_modules/**")
    """
    results = tree_summary(
        root_dir,
        max_depth=max_depth,
        include_files=include_files,
        exclude_glob=exclude_glob,
    )
    return _to_json_str(results)


async def read_file_range_tool(path: str, start_line: int, end_line: int) -> str:
    """LLM Tool: Read a file line range and return JSON as a string.

    Args:
        path: Absolute or relative file path.
        start_line: 1-based start line.
        end_line: 1-based end line (inclusive).

    Returns:
        JSON string encoding an object: {"content": "..."}.

    Usage:
        await read_file_range_tool("/repo/src/app.py", 10, 40)
    """
    results = read_file_range(path, start_line, end_line)
    return _to_json_str(results)


async def symbol_index_tool(
    root_dir: str,
    *,
    languages: Optional[List[str]] = None,
    include_glob: Optional[str] = None,
    page: int = 1,
    page_size: int = 200,
) -> str:
    """LLM Tool: Extract symbol index and return JSON as a string.

    Args:
        root_dir: Root directory to scan.
        languages: Optional list of languages (python, javascript, typescript, java).
        include_glob: Optional glob to include files.

    Returns:
        JSON string encoding a page object with items:
            symbol, kind, path, line.

    Usage:
        await symbol_index_tool("/repo", languages=["python", "java"], page=1, page_size=200)
    """
    results = symbol_index(root_dir, languages=languages, include_glob=include_glob)
    return _to_json_str(_paged_response(results, page=page, page_size=page_size))


async def find_references_tool(
    root_dir: str,
    symbol: str,
    *,
    is_regex: bool = False,
    include_glob: Optional[str] = None,
    max_results: int = 200,
    page: int = 1,
    page_size: int = 100,
) -> str:
    """LLM Tool: Find textual references to a symbol and return JSON as a string.

    Args:
        root_dir: Root directory to scan.
        symbol: Symbol name or regex pattern.
        is_regex: If True, interpret symbol as regex; otherwise use word-boundary match.
        include_glob: Optional glob to include files.
        max_results: Maximum number of matches to return.

    Returns:
        JSON string encoding a page object with items:
            path, line, snippet.

    Usage:
        await find_references_tool("/repo", "VectorStore", include_glob="**/*.py", page=1, page_size=100)
    """
    results = find_references(
        root_dir,
        symbol,
        is_regex=is_regex,
        include_glob=include_glob,
        max_results=max_results,
    )
    return _to_json_str(_paged_response(results, page=page, page_size=page_size))


async def file_metadata_tool(path: str) -> str:
    """LLM Tool: Get file metadata and return JSON as a string.

    Args:
        path: Absolute or relative file path.

    Returns:
        JSON string encoding: size (bytes), mtime (ISO 8601), encoding.

    Usage:
        await file_metadata_tool("/repo/README.md")
    """
    results = file_metadata(path)
    return _to_json_str(results)


async def language_stats_tool(
    root_dir: str,
    *,
    include_glob: Optional[str] = None,
    page: int = 1,
    page_size: int = 200,
) -> str:
    """LLM Tool: Collect language/extension statistics and return JSON as a string.

    Args:
        root_dir: Root directory to scan.
        include_glob: Optional glob to include files.

    Returns:
        JSON string encoding a page object with items: ext, files, lines.

    Usage:
        await language_stats_tool("/repo", include_glob="**/*", page=1, page_size=200)
    """
    results = language_stats(root_dir, include_glob=include_glob)
    return _to_json_str(_paged_response(results, page=page, page_size=page_size))
