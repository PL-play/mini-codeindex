from __future__ import annotations

import os
import sys

# Allow running this file both as a module (`python -m mini_code_index...`) and as
# a direct script (`python path/to/agent_graph.py`).
# When executed as a script, `mini_code_index` isn't on sys.path by default.
_SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from mini_code_index.retrieval.util.interface import OpenAICompatibleChatConfig, LLMRequest, LLMResponse


"""LangGraph-based retrieval agent workflow (skeleton).

This module defines the overall graph structure, roles, and state
for the retrieval agent. Node implementations are intentionally
left as placeholders (docstrings only) per requirement.
"""

import asyncio
import json
import logging
import re
import time
from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph
from langgraph.types import Command

from mini_code_index.retrieval.prompts import planner_system_prompt, task_agent_system_prompt
from mini_code_index.retrieval.state import RetrievalPlan, RetrievalAgentState, RetrievalComplete, SubtaskState
from mini_code_index.retrieval.util.llm_factory import OpenAICompatibleChatLLMService
from mini_code_index.retrieval.util.llm_utils import log_llm_json_result
from mini_code_index.retrieval.util.llm_tooling import (
    ToolRegistry,
    bind_tools,
    execute_tool_safely,
    extract_tool_calls,
    tool_messages_from_observations,
)
from mini_code_index.retrieval.util.common_tools import think_tool
from mini_code_index.retrieval.util.local_search import (
    file_metadata_tool,
    find_references_tool,
    language_stats_tool,
    path_glob_tool,
    read_file_range_tool,
    symbol_index_tool,
    text_search_tool,
    tree_summary_tool,
)
from mini_code_index.retrieval.util.vector_search import code_vector_search_tool

logger = logging.getLogger(__name__)


def _truncate(s: str, max_len: int = 80) -> str:
    s = str(s)
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


def _tool_args_summary(args: Any) -> str:
    if not isinstance(args, dict):
        return f"<{type(args).__name__}>"
    parts: List[str] = []
    for k in sorted(args.keys(), key=lambda x: str(x)):
        v = args.get(k)
        if isinstance(v, str):
            parts.append(f"{k}={_truncate(v.replace(chr(10), ' '), 80)!r}")
        elif isinstance(v, (int, float, bool)) or v is None:
            parts.append(f"{k}={v!r}")
        else:
            parts.append(f"{k}=<{type(v).__name__}>")
    return ", ".join(parts)


def _result_summary(result: Any) -> str:
    if result is None:
        return "None"
    if isinstance(result, str):
        return _truncate(result.replace("\n", " "), 200)
    if isinstance(result, bytes):
        return f"<bytes len={len(result)}>"
    if isinstance(result, list):
        return f"<list len={len(result)}>"
    if isinstance(result, dict):
        keys = list(result.keys())
        keys_preview = ",".join([str(k) for k in keys[:8]])
        suffix = "..." if len(keys) > 8 else ""
        if "error" in result:
            return f"<dict keys={keys_preview}{suffix} error={_truncate(str(result.get('error')), 120)!r}>"
        return f"<dict keys={keys_preview}{suffix}>"
    return f"<{type(result).__name__}>"


def _tool_call_note(name: str, args: Any, result: Any, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "tool": name,
        "args": args,
        "result": result,
    }
    if meta:
        payload.update(meta)
    return payload


def _normalize_note_payload(note: Any) -> Any:
    if isinstance(note, dict):
        return note
    if not isinstance(note, str):
        return note
    s = note.strip()
    try:
        first = json.loads(s)
    except Exception:
        return note
    if isinstance(first, str):
        inner = first.strip()
        if inner.startswith("{") or inner.startswith("["):
            try:
                return json.loads(inner)
            except Exception:
                return first
    return first


def _normalize_result_payload(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    s = value.strip()
    if not s:
        return value
    if not (s.startswith("{") or s.startswith("[") or s.startswith('"')):
        return value
    try:
        first = json.loads(s)
    except Exception:
        return value
    if isinstance(first, str):
        inner = first.strip()
        if inner.startswith("{") or inner.startswith("["):
            try:
                return json.loads(inner)
            except Exception:
                return first
    return first


def _safe_filename(value: str, *, prefix: str = "subtask", max_len: int = 60) -> str:
    base = re.sub(r"[^A-Za-z0-9_-]+", "_", (value or "").strip()).strip("_").lower()
    if not base:
        base = "untitled"
    base = base[:max_len]
    return f"{prefix}_{base}.md"


def _tool_calls_brief(tool_calls: Any) -> str:
    if not isinstance(tool_calls, list):
        return f"<{type(tool_calls).__name__}>"
    parts: List[str] = []
    for tc in tool_calls:
        if not isinstance(tc, dict):
            parts.append(f"<{type(tc).__name__}>"
            )
            continue
        name = str(tc.get("name") or "")
        args = tc.get("args") or {}
        parts.append(f"{name}({ _tool_args_summary(args) })")
    return "; ".join(parts)


def _log_prefix(node: str, state: Dict[str, Any]) -> str:
    task = asyncio.current_task()
    atask = "no-task"
    if task is not None:
        try:
            atask = task.get_name()
        except Exception:
            atask = f"task@{id(task)}"

    iteration = int(state.get("iteration", 0) or 0)
    tool_iter = int(state.get("tool_call_iterations", 0) or 0)

    sub_task = state.get("sub_task") or {}
    sub_name = _truncate(str(sub_task.get("name", "") or "").strip(), 60)

    return f"[{node} atask={atask} iter={iteration} tool_iter={tool_iter} subtask={sub_name!r}]"


def _messages_summary(messages: List[Any], max_len: int = 600) -> str:
    if not messages:
        return "<empty>"
    parts: List[str] = []
    for msg in messages:
        if not isinstance(msg, dict):
            parts.append(f"<{type(msg).__name__}>")
            continue
        role = msg.get("role") or "unknown"
        content = msg.get("content")
        tool_call_id = msg.get("tool_call_id")
        tool_calls = msg.get("tool_calls")
        content_preview = ""
        if isinstance(content, str):
            content_preview = _truncate(content.replace("\n", " "), 120)
        elif content is not None:
            content_preview = f"<{type(content).__name__}>"
        tool_calls_count = len(tool_calls) if isinstance(tool_calls, list) else (1 if tool_calls else 0)
        extra = []
        if tool_call_id:
            extra.append(f"tool_call_id={tool_call_id}")
        if tool_calls_count:
            extra.append(f"tool_calls={tool_calls_count}")
        suffix = f" ({', '.join(extra)})" if extra else ""
        parts.append(f"{role}:{content_preview}{suffix}")
    return _truncate(" | ".join(parts), max_len)


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


def _load_task_agent_config() -> OpenAICompatibleChatConfig:
    return OpenAICompatibleChatConfig(
        base_url=_require_env("TASK_AGENT_BASE_URL"),
        api_key=_require_env("TASK_AGENT_API_KEY"),
        model=_require_env("TASK_AGENT_MODEL"),
    )


def _task_tools() -> List[Any]:
    return [
        text_search_tool,
        path_glob_tool,
        tree_summary_tool,
        read_file_range_tool,
        symbol_index_tool,
        find_references_tool,
        file_metadata_tool,
        language_stats_tool,
        code_vector_search_tool,
        think_tool,
        RetrievalComplete,
    ]


async def planner_node(state: RetrievalAgentState) -> Command:
    """Planner/Supervisor node.

    Responsibilities:
    - Analyze the user query.
    - Produce a high-level plan and sub-task list.
    """
    logger.info("++++++++++ planner node start ++++++++++")
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
        max_tokens=4000,
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
    root_dir = str(state.get("root_dir", "") or "").strip()
    if not root_dir:
        raise ValueError("Missing required field: root_dir")

    sub_task = state.get("sub_task") or {}
    name = str(sub_task.get("name", "") or "").strip()
    instruction = str(sub_task.get("instruction", "") or "").strip()
    if not name and not instruction:
        return Command(update={"notes": ["empty_subtask"], "last_step_had_tool_calls": False})

    prefix = _log_prefix("task_agent", dict(state))
    logger.info("++++++++++ task_agent node start ++++++++++ %s", prefix)

    cfg = _load_task_agent_config()
    client = OpenAICompatibleChatLLMService(cfg)
    bound = bind_tools(client, _task_tools())

    messages = list(state.get("messages") or [])
    new_messages: List[Dict[str, Any]] = []
    if not messages:
        task_text = f"Subtask: {name}\nInstruction: {instruction}\nRoot directory: {root_dir}"
        user_message = {"role": "user", "content": task_text}
        messages.append(user_message)
        new_messages.append(user_message)

    logger.info("%s llm_messages %s", prefix, _messages_summary(messages))
    logger.debug("%s llm_messages_full %s", prefix, messages)

    req = LLMRequest(
        messages=messages,
        system_prompt=task_agent_system_prompt,
        temperature=0.0,
        max_tokens=8000,
    )
    resp = await bound.complete(req)
    tool_calls = resp.get_tool_calls()

    logger.info("%s llm_done tool_calls=%d", prefix, len(tool_calls))
    if tool_calls:
        logger.info("%s tool_calls %s", prefix, _tool_calls_brief(tool_calls))
    logger.debug("%s llm_text=%r", prefix, _truncate(resp.raw_text or resp.content_text or "", 200))
    assistant_message = {
        "role": "assistant",
        "content": (resp.raw_text or resp.content_text or ""),
        "tool_calls": tool_calls,
    }

    return Command(
        update={
            "messages": [*new_messages, assistant_message],
            "last_step_had_tool_calls": bool(tool_calls),
        }
    )

task_tool_reg = ToolRegistry(_task_tools())

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
    prefix = _log_prefix("task_tools", dict(state))
    logger.info("++++++++++ task_tools node start ++++++++++ %s", prefix)

    messages = list(state.get("messages") or [])
    if not messages:
        return Command(update={"last_step_had_tool_calls": False})

    last_msg = messages[-1]
    tool_calls_raw = last_msg.get("tool_calls") if isinstance(last_msg, dict) else None
    if not tool_calls_raw:
        return Command(update={"last_step_had_tool_calls": False})

    tool_calls = extract_tool_calls(
        LLMResponse(raw_text="", tool_calls=list(tool_calls_raw) if isinstance(tool_calls_raw, list) else [])
    )
    if not tool_calls:
        return Command(update={"last_step_had_tool_calls": False})

    logger.info("%s start tool_calls=%d", prefix, len(tool_calls))

    completion_tool_names = {"RetrievalComplete", "ResearchComplete", "ResearchCompleted"}
    has_completion = any(tc.get("name") in completion_tool_names for tc in tool_calls)

    observations: List[Any] = []
    executed_calls: List[Dict[str, Any]] = []
    notes: List[str] = []

    root_dir = str(state.get("root_dir", "") or "").strip()

    if has_completion:
        logger.info("%s completion_requested", prefix)
        for idx, tc in enumerate(tool_calls, start=1):
            if tc.get("name") in completion_tool_names:
                obs = "Retrieval marked complete"
                observations.append(obs)
                executed_calls.append(tc)
                notes.append(
                    _tool_call_note(
                        str(tc.get("name") or ""),
                        tc.get("args") or {},
                        obs,
                        {"tool_iter": int(state.get("tool_call_iterations", 0)), "call_index": idx},
                    )
                )
        tool_messages = tool_messages_from_observations(
            tool_calls=executed_calls,
            observations=observations,
        )
        return Command(
            update={
                "messages": tool_messages,
                "notes": notes,
                "last_step_had_tool_calls": False,
                "tool_call_iterations": int(state.get("tool_call_iterations", 0)) + 1,
            }
        )

    if any(str(tc.get("name") or "") == "think_tool" for tc in tool_calls) and len(tool_calls) > 1:
        notes.append("think_tool_parallel_violation")
        logger.warning("%s think_tool_parallel_violation", prefix)

    tool_iter = int(state.get("tool_call_iterations", 0))
    non_think_tool_called = False
    extra_messages: List[Dict[str, Any]] = []
    tool_iter = int(state.get("tool_call_iterations", 0))
    for idx, tc in enumerate(tool_calls, start=1):
        name = str(tc.get("name") or "").strip()
        args = tc.get("args") or {}
        if name == "think_tool" and "reflection" not in args and "tool_input" in args:
            args = dict(args)
            args["reflection"] = args.get("tool_input")
        if name in {
            "text_search_tool",
            "path_glob_tool",
            "tree_summary_tool",
            "symbol_index_tool",
            "find_references_tool",
            "language_stats_tool",
            "code_vector_search_tool",
        }:
            if root_dir and not args.get("root_dir"):
                args = dict(args)
                args["root_dir"] = root_dir
        if name in {"read_file_range_tool", "file_metadata_tool"}:
            path = str(args.get("path") or "").strip()
            if path and not os.path.isabs(path) and root_dir:
                args = dict(args)
                args["path"] = os.path.join(root_dir, path)
        logger.info("%s tool_execute name=%s args=%s", prefix, name, _tool_args_summary(args))
        spec = task_tool_reg.get(name)
        if spec is None:
            logger.warning("%s tool_unknown name=%s", prefix, name)
            obs = {"error": f"unknown_tool:{name}"}
            observations.append(obs)
            executed_calls.append(tc)
            notes.append(_tool_call_note(name, args, obs, {"tool_iter": tool_iter, "call_index": idx}))
            continue

        t0 = time.perf_counter()
        obs = await execute_tool_safely(spec, args)
        dt_ms = (time.perf_counter() - t0) * 1000.0

        summary = _result_summary(obs)
        logger.info("%s tool_result name=%s dt_ms=%.1f result=%s", prefix, name, dt_ms, summary)
        logger.info("%s tool_result_value name=%s value=%s", prefix, name, _truncate(str(obs), 500))
        if isinstance(obs, dict) and obs.get("error"):
            logger.warning("%s tool_result_error name=%s error=%r", prefix, name, _truncate(str(obs.get("error")), 200))

        observations.append(obs)
        executed_calls.append(tc)

        if name == "think_tool":
            reflection_text = obs if isinstance(obs, str) else str(obs)
            extra_messages.append(
                {
                    "role": "user",
                    "content": f"[Think Reflection]\n{reflection_text}",
                }
            )
            notes.append(
                _tool_call_note(
                    "think_tool_reflection",
                    {"reflection": args.get("reflection")},
                    reflection_text,
                    {"tool_iter": tool_iter, "call_index": idx},
                )
            )
        else:
            notes.append(_tool_call_note(name, args, obs, {"tool_iter": tool_iter, "call_index": idx}))
            non_think_tool_called = True

    tool_messages = tool_messages_from_observations(
        tool_calls=executed_calls,
        observations=observations,
    )

    return Command(
        update={
            "messages": [*tool_messages, *extra_messages],
            "notes": notes,
            "last_step_had_tool_calls": True,
            "tool_call_iterations": int(state.get("tool_call_iterations", 0)) + (1 if non_think_tool_called else 0),
        }
    )


async def synthesize_node(state: SubtaskState) -> Command:
    """Synthesizer/Analyst node (subtask graph).

    Responsibilities (to be implemented):
    - Deduplicate and merge evidence.
    - Produce a subtask-level result with citations.
    """
    prefix = _log_prefix("synthesize", dict(state))
    logger.info("++++++++++ synthesize node start ++++++++++ %s", prefix)

    sub_task = state.get("sub_task") or {}
    name = str(sub_task.get("name", "") or "").strip()
    instruction = str(sub_task.get("instruction", "") or "").strip()
    notes = list(state.get("notes") or [])

    rendered_items: List[str] = []
    tool_count = 0
    for note in notes:
        payload = _normalize_note_payload(note)

        if isinstance(payload, dict):
            if payload.get("note") == "retrieval_complete_requested":
                continue
            if payload.get("tool") in {"think_tool", "think_tool_reflection"}:
                reflection = payload.get("result")
                rendered_items.append("### Think Reflection")
                rendered_items.append(str(reflection or ""))
                rendered_items.append("")
                continue
            if "result" in payload:
                payload = dict(payload)
                payload["result"] = _normalize_result_payload(payload.get("result"))
            tool_count += 1
            rendered_items.append(f"### Call {tool_count}")
            rendered_items.append("```json")
            rendered_items.append(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
            rendered_items.append("```")
            rendered_items.append("")
            continue

        rendered_items.append(f"### Call {tool_count + 1}")
        rendered_items.append("```json")
        rendered_items.append(json.dumps({"note": payload}, ensure_ascii=False, indent=2, default=str))
        rendered_items.append("```")
        rendered_items.append("")
        tool_count += 1

    lines: List[str] = [
        "# Subtask Debug Report",
        "",
        f"**Title**: {name or '(empty)'}",
        f"**Instruction**: {instruction or '(empty)'}",
        "",
        "## Tool Calls",
    ]
    if rendered_items:
        lines.extend(rendered_items)
    else:
        lines.append("- (none)")

    report = "\n".join(lines).rstrip()
    logger.info("%s synthesize_report\n%s", prefix, report)

    report_path = _safe_filename(name or instruction or "subtask")
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info("%s synthesize_report_written path=%s", prefix, report_path)
    except Exception as e:
        logger.warning("%s synthesize_report_write_failed error=%s", prefix, e)

    return Command(update={"notes": [report], "last_step_had_tool_calls": False})


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
    prefix = _log_prefix("verify", dict(state))
    logger.info("++++++++++ verify node start ++++++++++ %s", prefix)
    return Command(update={"needs_more": False})

async def summarize_node(state: RetrievalAgentState) -> Command:
    """Summarize all subtask results.

    Responsibilities (to be implemented):
    - Merge sub_results into a final answer.
    - Resolve conflicts and ensure coverage.
    """
    logger.info("++++++++++ summarize node start ++++++++++")
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
    logger.info("++++++++++ run_subtasks node start ++++++++++")
    root_dir = str(state.get("root_dir", "") or "").strip()
    if not root_dir:
        raise ValueError("Missing required field: root_dir")

    sub_tasks = list(state.get("sub_tasks") or [])
    if not sub_tasks:
        return Command(update={"sub_results": [], "notes": "no_subtasks"})

    max_iterations = int(state.get("max_iterations", 2))
    max_tool_call_iterations = int(state.get("max_tool_call_iterations", 10))

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
