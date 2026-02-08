from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .retrieval.agent_graph import build_retrieval_agent_graph


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mini-code-index")
    p.add_argument("root_dir", help="Root directory to retrieve from")
    p.add_argument("query", help="User query")
    p.add_argument("--max-iterations", type=int, default=2, help="Max retrieval rounds (default: %(default)s)")
    p.add_argument(
        "--max-tool-call-iterations",
        type=int,
        default=8,
        help="Max tool loop iterations (default: %(default)s)",
    )
    p.add_argument(
        "--recursion-limit",
        type=int,
        default=80,
        help="LangGraph recursion limit (default: %(default)s)",
    )
    p.add_argument(
        "--output",
        type=str,
        default="",
        help="Optional output markdown file path",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    graph = build_retrieval_agent_graph()

    async def _run() -> dict:
        return await graph.ainvoke(
            {
                "query": args.query,
                "root_dir": str(Path(args.root_dir).resolve()),
                "max_iterations": args.max_iterations,
                "max_tool_call_iterations": args.max_tool_call_iterations,
            },
            {"recursion_limit": args.recursion_limit},
        )

    result = asyncio.run(_run())
    answer = ""
    if isinstance(result, dict):
        answer = str(result.get("answer") or result.get("final_answer") or "")
    if args.output:
        Path(args.output).write_text(answer, encoding="utf-8")
    else:
        print(answer)
    return 0
