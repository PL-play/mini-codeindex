from __future__ import annotations

import asyncio
import unittest
from pathlib import Path

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
                graph.ainvoke(
                    {"query": query, "root_dir": root_dir, "max_iterations": 2, "max_tool_call_iterations": 10})
            )
            # print("graph run result:", result)
        except Exception as exc:
            print("graph run failed (expected if subgraph nodes not implemented):", exc)

    def test_batch_questions_write_md(self) -> None:
        graph = build_retrieval_agent_graph()
        root_dir = "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
        questions = [
            "这个项目的主要目的是什么？它的核心功能有哪些？",
            "项目里有哪些主要模块（Java 和 Python 各自有哪些关键文件/目录）？",
            "Java 侧的用户管理功能涉及哪些核心类，它们之间是什么关系？",
            "Python 侧的数据处理流程是什么，入口脚本和关键依赖文件有哪些？",
            "项目中有哪些设计模式示例？各自对应的类或文件在哪里？",
        ]

        out_lines = ["# Retrieval Agent Batch Results", ""]

        async def _run_all() -> None:
            for idx, query in enumerate(questions, start=1):
                try:
                    result = await graph.ainvoke(
                        {
                            "query": query,
                            "root_dir": root_dir,
                            "max_iterations": 2,
                            "max_tool_call_iterations": 8,
                        },
                        {"recursion_limit": 80},
                    )
                    answer = ""
                    if isinstance(result, dict):
                        answer = str(result.get("answer") or result.get("final_answer") or "")
                    content = [
                        f"# Q{idx}",
                        "",
                        f"**Question**: {query}",
                        "",
                        "**Answer**:",
                        "",
                        answer or "(empty)",
                        "",
                    ]
                    out_lines.extend(
                        [
                            f"## Q{idx}",
                            "",
                            f"**Question**: {query}",
                            "",
                            "**Answer**:",
                            "",
                            answer or "(empty)",
                            "",
                        ]
                    )
                    file_path = Path(__file__).parent / f"batch_retrieval_q{idx}.md"
                    file_path.write_text("\n".join(content), encoding="utf-8")
                except Exception as exc:
                    content = [
                        f"# Q{idx}",
                        "",
                        f"**Question**: {query}",
                        "",
                        "**Answer**:",
                        "",
                        f"(error) {exc}",
                        "",
                    ]
                    out_lines.extend(
                        [
                            f"## Q{idx}",
                            "",
                            f"**Question**: {query}",
                            "",
                            "**Answer**:",
                            "",
                            f"(error) {exc}",
                            "",
                        ]
                    )
                    file_path = Path(__file__).parent / f"batch_retrieval_q{idx}.md"
                    file_path.write_text("\n".join(content), encoding="utf-8")

        asyncio.run(_run_all())

        output_path = Path(__file__).parent / "batch_retrieval_results.md"
        output_path.write_text("\n".join(out_lines), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
