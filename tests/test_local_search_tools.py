from __future__ import annotations

import asyncio
import json
from pathlib import Path
import unittest

from mini_code_index.retrieval.util import (
    file_metadata_tool,
    find_references_tool,
    language_stats_tool,
    path_glob_tool,
    read_file_range_tool,
    symbol_index_tool,
    text_search_tool,
    tree_summary_tool,
)


def _pretty_json(raw_json: str) -> str:
    try:
        return json.dumps(json.loads(raw_json), ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return raw_json


class TestLocalSearchTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        project_root = Path(__file__).resolve().parents[1]
        cls.test_code_dir = project_root / "test_code_index_project"

    def test_text_search_tool(self) -> None:
        result = asyncio.run(
            text_search_tool(
                str(self.test_code_dir),
                "UserService",
                include_glob="src/**/*.java",
                max_results=5,
            )
        )
        print("text_search_tool result:\n", _pretty_json(result))

    def test_path_glob_tool(self) -> None:
        result = asyncio.run(path_glob_tool(str(self.test_code_dir), "src/**/*.py"))
        print("path_glob_tool result:\n", _pretty_json(result))

    def test_tree_summary_tool(self) -> None:
        result = asyncio.run(tree_summary_tool(str(self.test_code_dir), max_depth=2))
        print("tree_summary_tool result:\n", _pretty_json(result))

    def test_read_file_range_tool(self) -> None:
        target_file = self.test_code_dir / "src" /"main" / "python" / "config.py"
        result = asyncio.run(read_file_range_tool(str(target_file), 1, 5))
        print("read_file_range_tool result:\n", _pretty_json(result))

    def test_symbol_index_tool(self) -> None:
        result = asyncio.run(symbol_index_tool(str(self.test_code_dir), languages=["java"]))
        print("symbol_index_tool result:\n", _pretty_json(result))

    def test_find_references_tool(self) -> None:
        result = asyncio.run(
            find_references_tool(
                str(self.test_code_dir),
                "UserService",
                include_glob="src/**/*.java",
                max_results=10,
            )
        )
        print("find_references_tool result:\n", _pretty_json(result))

    def test_file_metadata_tool(self) -> None:
        target_file = self.test_code_dir / "README.md"
        result = asyncio.run(file_metadata_tool(str(target_file)))
        print("file_metadata_tool result:\n", _pretty_json(result))

    def test_language_stats_tool(self) -> None:
        result = asyncio.run(language_stats_tool(str(self.test_code_dir)))
        print("language_stats_tool result:\n", _pretty_json(result))


if __name__ == "__main__":
    unittest.main()
