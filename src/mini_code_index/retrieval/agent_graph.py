from __future__ import annotations

import os
import sys

# Allow running this file both as a module (`python -m mini_code_index...`) and as
# a direct script (`python path/to/agent_graph.py`).
# When executed as a script, `mini_code_index` isn't on sys.path by default.
_SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from mini_code_index.retrieval.util.interface import OpenAICompatibleChatConfig, LLMRequest


"""LangGraph-based retrieval agent workflow (skeleton).

This module defines the overall graph structure, roles, and state
for the retrieval agent. Node implementations are intentionally
left as placeholders (docstrings only) per requirement.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph
from langgraph.types import Command

from mini_code_index.retrieval.prompts import planner_system_prompt
from mini_code_index.retrieval.state import RetrievalPlan, RetrievalAgentState, SubtaskState
from mini_code_index.retrieval.util.llm_factory import OpenAICompatibleChatLLMService
from mini_code_index.retrieval.util.llm_utils import log_llm_json_result

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


async def task_agent_node(state: SubtaskState) -> Command:
    """Subtask agent node ("supervisor-like") for ONE subtask.

    Input example (state['sub_task']):
        {"name": "Identify entry points and core logic",
         "instruction": "Locate the main entry files ..."}

    Design intent:
    - Organize context (root_dir + sub_task + prior evidence + prior notes).
    - Bind *action tools* (vector search, local search, file read, etc.).
    - Ask the LLM to decide the next action (often a tool call).
    - Do NOT execute tools here; execution happens in `task_tools_node`.

    Expected state updates (conceptually):
    - Append an AIMessage to state['messages'].
    - Set state['last_step_had_tool_calls'] based on the AIMessage tool_calls.
    """
    raise NotImplementedError


async def task_tools_node(state: SubtaskState) -> Command:
    """Tool execution node for the subtask agent.

    Design intent:
    - If the last AIMessage requested tool calls, execute them safely.
    - Append ToolMessage(s) to state['messages'].
    - Increment `tool_call_iterations`.
    - Normalize any results into `evidence` / `notes`.

    Exit behavior:
        - Control returns to routing (`_route_after_task_tools`) which either:
            - loops back to `task_agent` (continue tool-calling), or
      - proceeds to `synthesize` (no tool calls / hit tool loop limit).
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
    - Decide whether to iterate another round.
    - Set needs_more flag.

    If another round is needed, this node should ALSO prepare the next round state
    (so we can keep the graph short):
    - If state['next_sub_task'] is set, overwrite state['sub_task'].
    - Increment `iteration` (round counter).
    - Reset tool-loop counters for the next round:
        - tool_call_iterations = 0
        - last_step_had_tool_calls = False
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

    If needs_more is True and iteration < max_iterations -> next round.
    Otherwise, end the workflow.
    """
    needs_more = bool(state.get("needs_more"))
    iteration = int(state.get("iteration", 0))
    max_iterations = int(state.get("max_iterations", 2))
    if needs_more and iteration < max_iterations:
        return "task_agent"
    return END


def _route_after_task_tools(state: SubtaskState) -> str:
    """Routing logic after tool execution.

    Continue the retrieval tool-calling loop if:
    - the last retrieval step had tool calls AND
    - tool_call_iterations < max_tool_call_iterations

    Otherwise proceed to synthesis.
    """
    had_tool_calls = bool(state.get("last_step_had_tool_calls"))
    tool_iters = int(state.get("tool_call_iterations", 0))
    max_tool_iters = int(state.get("max_tool_call_iterations", 5))
    if had_tool_calls and tool_iters < max_tool_iters:
        return "task_agent"
    return "synthesize"


def build_subtask_graph() -> Any:
    """Build the subtask graph (re-planned).

    Subtask flow (two loops):
    1) Retrieval tool-calling loop (supervisor-like):
        task_agent -> task_tools -> (task_agent | synthesize)
    2) Verify-driven retrieval-round loop:
        synthesize -> verify -> (task_agent | END)

    Note:
        To keep the graph short, state preparation for the next round (refining
        sub_task, incrementing iteration, resetting tool counters) is handled
        inside `verify_node`.
    """
    graph = StateGraph(SubtaskState)
    graph.add_node("task_agent", task_agent_node)
    graph.add_node("task_tools", task_tools_node)
    graph.add_node("synthesize", synthesize_node)
    graph.add_node("verify", verify_node)

    graph.set_entry_point("task_agent")

    # Retrieval tool loop
    graph.add_edge("task_agent", "task_tools")
    graph.add_conditional_edges(
        "task_tools",
        _route_after_task_tools,
        {
            "task_agent": "task_agent",
            "synthesize": "synthesize",
        },
    )

    # Synthesize + verify
    graph.add_edge("synthesize", "verify")
    graph.add_conditional_edges(
        "verify",
        _route_after_verify,
        {
            "task_agent": "task_agent",
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
    max_tool_call_iterations = int(state.get("max_tool_call_iterations", 5))

    async def _run_one(task: Dict[str, Any]) -> Dict[str, Any]:
        return await subtask_graph.ainvoke(
            {
                "sub_task": task,
                "iteration": 0,
                "max_iterations": max_iterations,
                "tool_call_iterations": 0,
                "max_tool_call_iterations": max_tool_call_iterations,
                "last_step_had_tool_calls": False,
                "next_sub_task": None,
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
            "    task_agent --> task_tools\n"
            "    task_tools --> task_agent\n"
            "    task_tools --> synthesize\n"
            "    synthesize --> verify\n"
            "    verify --> task_agent\n"
            "  end\n"
        )

        sub_mermaid = (
            "graph LR\n"
            "  task_agent --> task_tools\n"
            "  task_tools --> task_agent\n"
            "  task_tools --> synthesize\n"
            "  synthesize --> verify\n"
            "  verify --> task_agent\n"
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
