from __future__ import annotations

import asyncio
import unittest

from dotenv import load_dotenv

load_dotenv()
from mini_code_index.retrieval.agent_graph import build_retrieval_agent_graph


class TestRetrievalAgentGraph(unittest.TestCase):
    def test_build_graph(self) -> None:
        graph = build_retrieval_agent_graph()
        print("build_retrieval_agent_graph ok:", graph)
        try:
            g = graph.get_graph()
            # print("graph nodes:", g.nodes)
            # print("graph edges:", g.edges)
        except Exception as exc:
            print("graph visualization info unavailable:", exc)
        query = "这个项目是做什么的？"
        root_dir = "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
        try:
            result = asyncio.run(
                graph.ainvoke({"query": query, "root_dir": root_dir, "max_iterations": 2})
            )
            print("graph run result:", result)
        except Exception as exc:
            print("graph run failed (expected if subgraph nodes not implemented):", exc)


if __name__ == "__main__":
    unittest.main()
