from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
import unittest

from mini_code_index.retrieval.util import code_vector_search_tool


def _pretty_json(raw_json: str) -> str:
    try:
        return json.dumps(json.loads(raw_json), ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return raw_json


class TestCodeVectorSearchTool(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from dotenv import load_dotenv
        load_dotenv()
        project_root = Path(__file__).resolve().parents[1]
        cls.test_code_dir = project_root / "test_code_index_project"

    def test_code_vector_search_tool(self) -> None:
        chroma_host = os.environ.get("CHROMADB_HOST") or os.environ.get("CHROMA_URL")
        if not chroma_host:
            self.skipTest("CHROMADB_HOST/CHROMA_URL not set")

        try:
            import chromadb  # noqa: F401
        except Exception as e:
            self.skipTest(f"chromadb not available: {e}")

        result = asyncio.run(
            code_vector_search_tool(
                "搜索用户 search user",
                root_dir=str(self.test_code_dir),
                n_results=3,
            )
        )
        print("code_vector_search_tool result:\n", _pretty_json(result))


if __name__ == "__main__":
    unittest.main()
