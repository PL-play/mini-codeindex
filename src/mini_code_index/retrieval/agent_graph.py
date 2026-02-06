from __future__ import annotations

import sys
import os

from .util.interface import OpenAICompatibleChatConfig, LLMRequest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))


"""LangGraph-based retrieval agent workflow (skeleton).

This module defines the overall graph structure, roles, and state
for the retrieval agent. Node implementations are intentionally
left as placeholders (docstrings only) per requirement.
"""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph
from langgraph.types import Command

from mini_code_index.retrieval.prompts import planner_system_prompt
from mini_code_index.retrieval.state import RetrievalPlan, RetrievalAgentState, SubtaskState
from .util.llm_factory import OpenAICompatibleChatLLMService
from .util.llm_utils import log_llm_json_result

logger = logging.getLogger(__name__)


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _load_planner_config() -> OpenAICompatibleChatConfig:
    return OpenAICompatibleChatConfig(
        base_url=_require_env("PLANNER_BASE_URL"),
        api_key=_require_env("PLANNER_API_KEY"),
        model=_require_env("PLANNER_MODEL"),
    )


async def planner_node(state: RetrievalAgentState) -> Command:
    """Planner/Supervisor node.

    Responsibilities:
    - Analyze the user query.
    - Produce a high-level plan and sub-task list.
    """
    root_dir = str(state.get("root_dir", "") or "").strip()
    if not root_dir:
        raise ValueError("Missing required field: root_dir")

    query = str(state.get("query", "") or "").strip()
    if not query:
        return Command(update={"plan": None, "sub_tasks": [], "notes": "empty_query"})

    cfg = _load_planner_config()
    client = OpenAICompatibleChatLLMService(cfg)

    req = LLMRequest.from_prompt(
        prompt=query,
        system_prompt=planner_system_prompt,
        parse_json=True,
        temperature=0.0,
        max_tokens=2000,
    )
    resp = await client.complete(req)
    # log_llm_json_result(logger, resp, prefix="[planner]")

    if resp.parse_error or not resp.json_data:
        raise ValueError(f"planner_json_parse_failed: {resp.parse_error or 'empty_json'}")

    plan_model = RetrievalPlan.model_validate(resp.json_data)
    plan_dict = plan_model.model_dump()
    sub_tasks = [task.model_dump() for task in plan_model.sub_tasks]

    logger.info(f"[planner] plan={plan_dict}")

    return Command(goto="run_subtasks",update={"plan": plan_dict, "sub_tasks": sub_tasks, "notes": "planner_ok"})


async def retrieval_node(state: SubtaskState) -> Command:
    """Retrieval Specialist node (subtask graph).

    Responsibilities (to be implemented):
    - Execute tools based on sub_task.
    - Collect candidate evidence chunks.
    - Store normalized evidence in state.
    """
    raise NotImplementedError


async def synthesize_node(state: SubtaskState) -> Command:
    """Synthesizer/Analyst node (subtask graph).

    Responsibilities (to be implemented):
    - Deduplicate and merge evidence.
    - Produce a subtask-level result with citations.
    """
    raise NotImplementedError


async def verify_node(state: SubtaskState) -> Command:
    """Verifier/Critic node (subtask graph).

    Responsibilities (to be implemented):
    - Check if evidence is sufficient and consistent.
    - Decide whether to iterate retrieval.
    - Set needs_more flag.
    """
    raise NotImplementedError

async def summarize_node(state: RetrievalAgentState) -> Command:
    """Summarize all subtask results.

    Responsibilities (to be implemented):
    - Merge sub_results into a final answer.
    - Resolve conflicts and ensure coverage.
    """
    raise NotImplementedError


def _route_after_verify(state: SubtaskState) -> str:
    """Routing logic after verification.

    If needs_more is True and iteration < max_iterations -> retrieval.
    Otherwise, end the workflow.
    """
    needs_more = bool(state.get("needs_more"))
    iteration = int(state.get("iteration", 0))
    max_iterations = int(state.get("max_iterations", 2))
    if needs_more and iteration < max_iterations:
        return "retrieval"
    return END


def build_subtask_graph() -> Any:
    """Build the subtask graph: retrieval -> synthesize -> verify -> (loop)."""
    graph = StateGraph(SubtaskState)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("synthesize", synthesize_node)
    graph.add_node("verify", verify_node)

    graph.set_entry_point("retrieval")
    graph.add_edge("retrieval", "synthesize")
    graph.add_edge("synthesize", "verify")
    graph.add_conditional_edges(
        "verify",
        _route_after_verify,
        {
            "retrieval": "retrieval",
            END: END,
        },
    )
    return graph.compile()

subtask_graph = build_subtask_graph()

async def run_subtasks_node(state: RetrievalAgentState) -> Command:
    """Execute subtask sub-graphs in parallel.

    Responsibilities (to be implemented):
    - Fan out sub_tasks to the subtask graph (parallel execution).
    - Collect sub_results.

    Note:
        This node is reserved for a future implementation. In the current
        graph skeleton, the subtask graph is used directly as a node.
    """
    root_dir = str(state.get("root_dir", "") or "").strip()
    if not root_dir:
        raise ValueError("Missing required field: root_dir")

    sub_tasks = list(state.get("sub_tasks") or [])
    if not sub_tasks:
        return Command(update={"sub_results": [], "notes": "no_subtasks"})

    max_iterations = int(state.get("max_iterations", 2))

    async def _run_one(task: Dict[str, Any]) -> Dict[str, Any]:
        return await subtask_graph.ainvoke(
            {
                "sub_task": task,
                "iteration": 0,
                "max_iterations": max_iterations,
                "root_dir": root_dir,
            }
        )

    results = await asyncio.gather(*[_run_one(task) for task in sub_tasks])
    return Command(update={"sub_results": results, "notes": "subtasks_done"})

def build_retrieval_agent_graph() -> Any:
    """Build a complete retrieval agent graph (skeleton).

        Main flow:
            planner -> run_subtasks(parallel) -> summarize -> END
    """
    graph = StateGraph(RetrievalAgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("run_subtasks", run_subtasks_node)
    graph.add_node("summarize", summarize_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "run_subtasks")
    graph.add_edge("run_subtasks", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()


def main() -> None:
    """Visualize the retrieval agent graph.

    This outputs a PNG diagram when supported; otherwise falls back to Mermaid markdown.
    """
    compiled = build_retrieval_agent_graph()
    subtask_compiled = build_subtask_graph()
    try:
        graph = compiled.get_graph()
        png_bytes = graph.draw_mermaid_png()
        output_path = "retrieval_agent_graph.png"
        with open(output_path, "wb") as f:
            f.write(png_bytes)
        print(f"Wrote graph visualization to {output_path}")

        sub_graph = subtask_compiled.get_graph()
        sub_png = sub_graph.draw_mermaid_png()
        sub_output_path = "retrieval_subtask_graph.png"
        with open(sub_output_path, "wb") as f:
            f.write(sub_png)
        print(f"Wrote subtask graph visualization to {sub_output_path}")
        return
    except Exception:
        mermaid = (
            "graph LR\n"
            "  planner --> run_subtasks --> summarize --> END\n"
            "  subgraph subtask_graph\n"
            "    retrieval --> synthesize --> verify\n"
            "    verify --> retrieval\n"
            "  end\n"
        )

        sub_mermaid = (
            "graph LR\n"
            "  retrieval --> synthesize --> verify\n"
            "  verify --> retrieval\n"
        )

    output_path = "retrieval_agent_graph.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("```mermaid\n")
        f.write(mermaid)
        f.write("\n```")

    print(f"Wrote graph visualization to {output_path}")

    sub_output_path = "retrieval_subtask_graph.md"
    with open(sub_output_path, "w", encoding="utf-8") as f:
        f.write("```mermaid\n")
        f.write(sub_mermaid)
        f.write("\n```")

    print(f"Wrote subtask graph visualization to {sub_output_path}")


if __name__ == "__main__":
    main()
