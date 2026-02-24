from __future__ import annotations

import ast
import fnmatch
import json
import math
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple, TypedDict


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


DEFAULT_TREE_EXCLUDE_GLOBS = [
    "**/.git/**",
    "**/.venv/**",
    "**/node_modules/**",
    "**/__pycache__/**",
    "**/.pytest_cache/**",
    "**/.mypy_cache/**",
    "**/.ruff_cache/**",
    "**/.tox/**",
    "**/.idea/**",
    "**/.vscode/**",
    "**/dist/**",
    "**/build/**",
    "**/target/**",
    "**/out/**",
    "**/.next/**",
    "**/.nuxt/**",
    "**/coverage/**",
    "**/bin/**",
    "**/obj/**",
]

DEFAULT_TREE_EXCLUDE_DIR_NAMES: Set[str] = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "target",
    "out",
    ".next",
    ".nuxt",
    "coverage",
    "bin",
    "obj",
}


def _iter_files(
    root_dir: str,
    *,
    include_glob: Optional[str] = None,
    exclude_glob: Optional[str] = None,
) -> Iterable[Tuple[Path, str]]:
    root = Path(root_dir).resolve()
    if not root.exists() or not root.is_dir():
        return

    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        pruned_dirnames: List[str] = []
        for dirname in dirnames:
            if dirname in DEFAULT_TREE_EXCLUDE_DIR_NAMES:
                continue
            full_dir = current / dirname
            rel_dir = full_dir.relative_to(root).as_posix()
            if _matches_any(rel_dir, DEFAULT_TREE_EXCLUDE_GLOBS):
                continue
            if exclude_glob and fnmatch.fnmatch(rel_dir, exclude_glob):
                continue
            pruned_dirnames.append(dirname)
        dirnames[:] = pruned_dirnames

        for filename in filenames:
            path = current / filename
            rel = path.relative_to(root).as_posix()
            if _matches_any(rel, DEFAULT_TREE_EXCLUDE_GLOBS):
                continue
            if include_glob and not fnmatch.fnmatch(rel, include_glob):
                continue
            if exclude_glob and fnmatch.fnmatch(rel, exclude_glob):
                continue
            yield path, rel


def _matches_any(rel: str, patterns: Optional[Iterable[str]]) -> bool:
    if not patterns:
        return False
    for pattern in patterns:
        if fnmatch.fnmatch(rel, pattern):
            return True
    return False


def _is_default_excluded_rel(rel: str) -> bool:
    parts = [part for part in rel.split("/") if part]
    if any(part in DEFAULT_TREE_EXCLUDE_DIR_NAMES for part in parts):
        return True
    return _matches_any(rel, DEFAULT_TREE_EXCLUDE_GLOBS)


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


def text_search_file_summary(
    root_dir: str,
    query: str,
    *,
    is_regex: bool = False,
    include_glob: Optional[str] = None,
    exclude_glob: Optional[str] = None,
    max_files: int = 300,
    max_total_hits: int = 10000,
) -> Dict[str, object]:
    pattern = query if is_regex else re.escape(query)
    regex = re.compile(pattern)
    per_file: List[Dict[str, object]] = []
    total_hits = 0
    matched_files = 0
    truncated = False
    scanned_files = 0
    safe_max_files = max(1, int(max_files))
    safe_total_hits = max(1, int(max_total_hits))

    for path, rel in _iter_files(root_dir, include_glob=include_glob, exclude_glob=exclude_glob):
        scanned_files += 1
        lines = _read_text_lines(path)
        count = 0
        first_line = 0
        last_line = 0
        for idx, line in enumerate(lines, start=1):
            hit_count = len(regex.findall(line))
            if hit_count <= 0:
                continue
            if first_line == 0:
                first_line = idx
            last_line = idx
            count += hit_count
            total_hits += hit_count
            if total_hits >= safe_total_hits:
                truncated = True
                break
        if count > 0:
            matched_files += 1
            per_file.append(
                {
                    "path": rel,
                    "match_count": count,
                    "first_line": first_line,
                    "last_line": last_line,
                }
            )
            if len(per_file) >= safe_max_files:
                truncated = True
                break
        if truncated:
            break

    per_file.sort(key=lambda item: (-int(item["match_count"]), str(item["path"])))
    return {
        "items": per_file,
        "meta": {
            "query": query,
            "mode": "file_summary",
            "scanned_files": scanned_files,
            "matched_files": matched_files,
            "total_hits": total_hits,
            "truncated": truncated,
            "max_files": safe_max_files,
            "max_total_hits": safe_total_hits,
        },
    }


def text_search_hits(
    root_dir: str,
    query: str,
    *,
    is_regex: bool = False,
    include_glob: Optional[str] = None,
    exclude_glob: Optional[str] = None,
    file_paths: Optional[List[str]] = None,
    per_file_hit_cap: int = 3,
    max_results: int = 60,
    context_lines: int = 0,
) -> Dict[str, object]:
    root = Path(root_dir).resolve()
    pattern = query if is_regex else re.escape(query)
    regex = re.compile(pattern)
    safe_file_cap = max(1, int(per_file_hit_cap))
    safe_max_results = max(1, int(max_results))
    safe_context_lines = max(0, int(context_lines))
    hits: List[TextSearchResult] = []
    omitted_hits = 0
    truncated = False

    candidates: List[Tuple[Path, str]] = []
    if file_paths:
        for raw in file_paths:
            rel_input = str(raw or "").strip()
            if not rel_input:
                continue
            candidate = Path(rel_input)
            path = candidate if candidate.is_absolute() else (root / rel_input)
            path = path.resolve()
            if not path.exists() or not path.is_file():
                continue
            try:
                rel = path.relative_to(root).as_posix()
            except ValueError:
                rel = path.as_posix()
            if _is_default_excluded_rel(rel):
                continue
            if include_glob and not fnmatch.fnmatch(rel, include_glob):
                continue
            if exclude_glob and fnmatch.fnmatch(rel, exclude_glob):
                continue
            candidates.append((path, rel))
    else:
        candidates = list(_iter_files(root_dir, include_glob=include_glob, exclude_glob=exclude_glob))

    for path, rel in candidates:
        lines = _read_text_lines(path)
        file_hits = 0
        for idx, line in enumerate(lines, start=1):
            for match in regex.finditer(line):
                if file_hits >= safe_file_cap:
                    omitted_hits += 1
                    continue
                if len(hits) >= safe_max_results:
                    truncated = True
                    break
                before_start = max(0, idx - 1 - safe_context_lines)
                after_end = min(len(lines), idx - 1 + safe_context_lines + 1)
                context_before = "\n".join(lines[before_start : idx - 1])
                context_after = "\n".join(lines[idx:after_end])
                hits.append(
                    {
                        "path": rel,
                        "line": idx,
                        "col": match.start() + 1,
                        "snippet": line.strip(),
                        "context_before": context_before,
                        "context_after": context_after,
                    }
                )
                file_hits += 1
            if truncated:
                break
        if truncated:
            break

    return {
        "items": hits,
        "meta": {
            "query": query,
            "mode": "hits",
            "candidate_files": len(candidates),
            "returned_hits": len(hits),
            "omitted_hits": omitted_hits,
            "per_file_hit_cap": safe_file_cap,
            "truncated": truncated,
            "context_lines": safe_context_lines,
        },
    }


def path_glob(root_dir: str, pattern: str, *, max_results: int = 500) -> List[PathResult]:
    matches: List[PathResult] = []
    for _path, rel in _iter_files(root_dir):
        if not fnmatch.fnmatch(rel, pattern):
            continue
        matches.append({"path": rel})
        if len(matches) >= max_results:
            break
    return matches


def tree_summary(
    root_dir: str,
    *,
    max_depth: int = 1,
    include_files: bool = True,
    exclude_globs: Optional[Iterable[str]] = None,
    max_entries_per_dir: int = 60,
    max_total_entries: int = 300,
) -> str:
    root = Path(root_dir).resolve()
    if not root.exists():
        return f"(error) path_not_found: {root.as_posix()}"
    if not root.is_dir():
        return f"(error) not_a_directory: {root.as_posix()}"

    safe_depth = max(0, int(max_depth))
    safe_per_dir = max(1, int(max_entries_per_dir))
    safe_total = max(20, int(max_total_entries))

    lines: List[str] = []
    emitted = 0
    truncated_global = False
    shown_dirs = 0
    shown_files = 0
    omitted_entries = 0

    def _should_skip(entry: Path) -> bool:
        if entry.is_dir() and entry.name in DEFAULT_TREE_EXCLUDE_DIR_NAMES:
            return True
        rel = entry.relative_to(root).as_posix()
        return _matches_any(rel, exclude_globs)

    def _visible_entries(current: Path) -> Tuple[List[Path], int, bool]:
        try:
            entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except (PermissionError, OSError):
            return [], 0, True

        visible: List[Path] = []
        for entry in entries:
            if _should_skip(entry):
                continue
            if entry.is_file() and not include_files:
                continue
            visible.append(entry)
        shown = visible[:safe_per_dir]
        hidden_count = max(0, len(visible) - len(shown))
        return shown, hidden_count, False

    def _flat_list(current: Path) -> None:
        nonlocal emitted, truncated_global, shown_dirs, shown_files, omitted_entries
        shown, hidden_count, denied = _visible_entries(current)
        if denied:
            lines.append("(permission denied)")
            return
        for entry in shown:
            if emitted >= safe_total:
                truncated_global = True
                return
            suffix = "/" if entry.is_dir() else ""
            lines.append(f"{entry.name}{suffix}")
            emitted += 1
            if entry.is_dir():
                shown_dirs += 1
            else:
                shown_files += 1
        if hidden_count > 0 and emitted < safe_total:
            lines.append(f"... ({hidden_count} more entries omitted)")
            omitted_entries += hidden_count

    def _tree_walk(current: Path, depth: int, prefix: str) -> None:
        nonlocal emitted, truncated_global, shown_dirs, shown_files, omitted_entries
        if emitted >= safe_total:
            truncated_global = True
            return
        shown, hidden_count, denied = _visible_entries(current)
        if denied:
            lines.append(f"{prefix}(permission denied)")
            return

        for idx, entry in enumerate(shown):
            if emitted >= safe_total:
                truncated_global = True
                return
            is_last = idx == len(shown) - 1 and hidden_count == 0
            branch = "└── " if is_last else "├── "
            suffix = "/" if entry.is_dir() else ""
            lines.append(f"{prefix}{branch}{entry.name}{suffix}")
            emitted += 1
            if entry.is_dir():
                shown_dirs += 1
            else:
                shown_files += 1
            if entry.is_dir() and depth < safe_depth:
                child_prefix = prefix + ("    " if is_last else "│   ")
                _tree_walk(entry, depth + 1, child_prefix)
            if truncated_global:
                return

        if hidden_count > 0 and emitted < safe_total:
            lines.append(f"{prefix}└── ... ({hidden_count} more entries omitted)")
            omitted_entries += hidden_count

    mode = "flat" if safe_depth <= 1 else "tree"
    lines.append("./")
    if mode == "flat":
        _flat_list(root)
    else:
        _tree_walk(root, 1, "")

    if truncated_global:
        lines.append(f"... (truncated at {safe_total} entries; narrow scope or reduce depth)")
    header = (
        f"root_dir={root.as_posix()} | mode={mode} | max_depth={safe_depth} | "
        f"include_files={include_files} | shown={emitted} (dirs={shown_dirs}, files={shown_files}) | "
        f"omitted={omitted_entries} | truncated={truncated_global}"
    )
    lines.insert(0, header)
    return "\n".join(lines)


def read_file_range(path: str, start_line: int, end_line: int) -> Dict[str, str]:
    file_path = Path(path)
    if not file_path.exists():
        return {"content": f"(error) file_not_found: {file_path.as_posix()}"}
    if not file_path.is_file():
        return {"content": f"(error) not_a_file: {file_path.as_posix()}"}

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
    if not file_path.exists():
        return {
            "size": 0,
            "mtime": "",
            "encoding": f"(error) file_not_found: {file_path.as_posix()}",
        }
    if not file_path.is_file():
        return {
            "size": 0,
            "mtime": "",
            "encoding": f"(error) not_a_file: {file_path.as_posix()}",
        }

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
    mode: str = "file_summary",
    file_paths: Optional[List[str]] = None,
    per_file_hit_cap: int = 3,
    max_files: int = 300,
    max_total_hits: int = 10000,
    context_lines: int = 2,
    max_results: int = 0,
    page: int = 1,
    page_size: int = 50,
) -> str:
    """LLM Tool: Search text with multi-stage modes and return JSON as a string.

    Args:
        root_dir: Root directory to scan.
        query: Search text or regex pattern.
        is_regex: If True, treat query as regex; otherwise escape as literal text.
        include_glob: Optional glob to include files (relative to root_dir).
        exclude_glob: Optional glob to exclude files (relative to root_dir).
        mode: Search mode: "file_summary" (default), "hits", or "full".
        file_paths: Optional target file list for mode="hits"/"full".
        per_file_hit_cap: Max returned hits per file for mode="hits".
        max_files: Max matched files returned for mode="file_summary".
        max_total_hits: Max hits to scan for mode="file_summary".
        context_lines: Number of context lines before/after the matched line.
        max_results: Backward-compatible cap for returned hit records (hits/full modes).
        page: Backward-compatible argument, currently ignored in output.
        page_size: Backward-compatible argument, currently ignored in output.

    Returns:
        JSON string with:
            {
              "mode": "file_summary" | "hits" | "full",
              "items": [...],
              "meta": {...}
            }
        Notes:
            - page/page_size are accepted for backward compatibility but ignored in output.
            - max_results controls the return cap for "hits"/"full" modes.
              If max_results <= 0, the default cap is 200.

    Usage:
        await text_search_tool("/repo", "diagnosis", mode="file_summary", include_glob="**/*.py")
        await text_search_tool("/repo", "diagnosis", mode="hits", file_paths=["app/services.py"], per_file_hit_cap=3)
        await text_search_tool("/repo", "diagnosis", mode="full", include_glob="**/*.py", context_lines=2)
    """
    _ = page
    _ = page_size
    safe_mode = str(mode or "file_summary").strip().lower()

    if safe_mode == "file_summary":
        summary = text_search_file_summary(
            root_dir,
            query,
            is_regex=is_regex,
            include_glob=include_glob,
            exclude_glob=exclude_glob,
            max_files=max_files,
            max_total_hits=max_total_hits,
        )
        return _to_json_str(
            {
                "mode": safe_mode,
                "items": list(summary["items"]),
                "meta": summary["meta"],
            }
        )

    if safe_mode == "hits":
        fetch_limit = max(30, int(max_results) if int(max_results) > 0 else 200)
        hit_data = text_search_hits(
            root_dir,
            query,
            is_regex=is_regex,
            include_glob=include_glob,
            exclude_glob=exclude_glob,
            file_paths=file_paths,
            per_file_hit_cap=per_file_hit_cap,
            max_results=fetch_limit,
            context_lines=0,
        )
        return _to_json_str(
            {
                "mode": safe_mode,
                "items": list(hit_data["items"]),
                "meta": hit_data["meta"],
            }
        )

    if safe_mode == "full":
        fetch_limit = max(30, int(max_results) if int(max_results) > 0 else 200)
        safe_context = max(0, int(context_lines))
        if file_paths:
            hit_data = text_search_hits(
                root_dir,
                query,
                is_regex=is_regex,
                include_glob=include_glob,
                exclude_glob=exclude_glob,
                file_paths=file_paths,
                per_file_hit_cap=max(1, fetch_limit),
                max_results=fetch_limit,
                context_lines=safe_context,
            )
            return _to_json_str(
                {
                    "mode": safe_mode,
                    "items": list(hit_data["items"]),
                    "meta": hit_data["meta"],
                }
            )

        results = text_search(
            root_dir,
            query,
            is_regex=is_regex,
            include_glob=include_glob,
            exclude_glob=exclude_glob,
            max_results=fetch_limit,
            context_lines=safe_context,
        )
        return _to_json_str(
            {
                "mode": safe_mode,
                "items": results,
                "meta": {
                    "query": query,
                    "mode": "full",
                    "returned_hits": len(results),
                    "context_lines": safe_context,
                    "truncated": len(results) >= fetch_limit,
                },
            }
        )

    return _to_json_str(
        {
            "error": f"invalid_mode:{safe_mode}",
            "supported_modes": ["file_summary", "hits", "full"],
        }
    )


async def path_glob_tool(
    root_dir: str,
    pattern: str,
    *,
    page: int = 1,
    page_size: int = 200,
) -> str:
    """LLM Tool: Match file paths by glob pattern and return JSON as a string.

    Args:
        root_dir: Root directory to scan.
        pattern: Glob pattern (relative to root_dir), e.g. "**/*.py".
        page: 1-based page index.
        page_size: Number of records per page.

    Returns:
        JSON string encoding a page object with items: [{"path": ...}].

    Usage:
        await path_glob_tool("/repo", "src/**/*.ts", page=1, page_size=200)
    """
    safe_page = max(1, int(page))
    safe_page_size = max(1, int(page_size))
    fetch_limit = max(500, safe_page * safe_page_size)

    results = path_glob(root_dir, pattern, max_results=fetch_limit)
    return _to_json_str(_paged_response(results, page=safe_page, page_size=safe_page_size))


async def tree_summary_tool(
    root_dir: str,
    *,
    max_depth: int = 1,
    include_files: bool = True,
    exclude_glob: Optional[str] = None,
) -> str:
    """LLM Tool: Build a concise directory summary as plain text.

    Args:
        root_dir: Root directory to summarize.
        max_depth: When <=1, returns flat one-level listing; when >1, returns a tree.
        include_files: If True, include files; otherwise show directories only.
        exclude_glob: Optional glob to exclude entries (relative to root_dir).
            If omitted, defaults exclude: .git, .venv, node_modules.

    Returns:
        Plain text listing (flat by default) with per-directory and global truncation.

    Usage:
        await tree_summary_tool("/repo", max_depth=3, exclude_glob="**/node_modules/**")
    """
    exclude_globs = list(DEFAULT_TREE_EXCLUDE_GLOBS)
    if exclude_glob is not None:
        exclude_globs.append(exclude_glob)

    return tree_summary(
        root_dir,
        max_depth=max_depth,
        include_files=include_files,
        exclude_globs=exclude_globs,
    )


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
    page: int = 1,
    page_size: int = 100,
) -> str:
    """LLM Tool: Find textual references to a symbol and return JSON as a string.

    Args:
        root_dir: Root directory to scan.
        symbol: Symbol name or regex pattern.
        is_regex: If True, interpret symbol as regex; otherwise use word-boundary match.
        include_glob: Optional glob to include files.
        page: 1-based page index.
        page_size: Number of records per page.

    Returns:
        JSON string encoding a page object with items:
            path, line, snippet.

    Usage:
        await find_references_tool("/repo", "VectorStore", include_glob="**/*.py", page=1, page_size=100)
    """
    safe_page = max(1, int(page))
    safe_page_size = max(1, int(page_size))
    fetch_limit = max(200, safe_page * safe_page_size)

    results = find_references(
        root_dir,
        symbol,
        is_regex=is_regex,
        include_glob=include_glob,
        max_results=fetch_limit,
    )
    return _to_json_str(_paged_response(results, page=safe_page, page_size=safe_page_size))


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
