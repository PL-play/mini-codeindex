from __future__ import annotations

import asyncio
import os

import pytest

from mini_code_index.retrieval_graph import build_retrieval_graph
from dotenv import load_dotenv
load_dotenv()

_RUN_INTEGRATION = os.environ.get("MINI_CODE_INDEX_RUN_INTEGRATION") == "1"


@pytest.mark.skipif(
    not _RUN_INTEGRATION,
    reason="Set MINI_CODE_INDEX_RUN_INTEGRATION=1 and REWRITE_* env vars to run",
)
def test_rewrite_graph_with_llm_integration() -> None:
    """Integration test: requires REWRITE_* env vars + paid network call."""
    graph = build_retrieval_graph()
    out = asyncio.run(
        graph.ainvoke(
            {
                "query": "vector store 查询、过滤 path、限制结果数",
                "rewrite": {},
                "rewritten_queries": [],
                "notes": "",
            }
        )
    )
    print("rewrite=", out.get("rewrite"))
    print("rewritten_queries=", out.get("rewritten_queries"))
    assert out["query"]
    assert isinstance(out.get("rewritten_queries"), list)
    assert 1 <= len(out["rewritten_queries"]) <= 5
    assert all(isinstance(q, str) and q.strip() for q in out["rewritten_queries"])
