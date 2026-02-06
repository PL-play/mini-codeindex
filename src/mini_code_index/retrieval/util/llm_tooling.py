from __future__ import annotations

import inspect
import json
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional, Sequence, Type, Union, get_args, get_origin

from .interface import LLMService, LLMRequest, LLMResponse, LLMMessage, LLMTool

try:
    # Optional dependency (already used in other parts of this mono-repo).
    from pydantic import BaseModel  # type: ignore
except Exception:  # pragma: no cover
    BaseModel = None  # type: ignore



ToolFn = Union[
    Callable[[Dict[str, Any]], Any],
    Callable[[Dict[str, Any]], Awaitable[Any]],
]


@dataclass(frozen=True)
class ToolSpec:
    """
    A lightweight tool definition (LangChain-like) that can be converted to OpenAI-compatible tool schema.
    """

    name: str
    description: str
    parameters: Dict[str, Any]
    # Execution callback (optional). Many tools are "signals" (e.g., ResearchComplete) and don't need a function.
    fn: Optional[ToolFn] = None
    # Optional raw callable reference (best-effort). Useful for debugging/introspection.
    raw: Any = None

    def to_llm_tool(self) -> LLMTool:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": dict(self.parameters or {}),
            },
        }

    def __call__(self, args: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        """
        Make ToolSpec callable for ergonomic manual execution:
        - tool({"a":1,"b":2})
        - tool(a=1,b=2)
        """
        if self.fn is None:
            raise TypeError(f"ToolSpec '{self.name}' is not executable (fn is None)")
        merged: Dict[str, Any] = {}
        if args:
            merged.update(args)
        if kwargs:
            merged.update(kwargs)
        return self.fn(merged)

    async def ainvoke(self, args: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        """
        Async-friendly execution helper (mirrors LangChain's ainvoke ergonomics).
        """
        v = self(args=args, **kwargs)
        if hasattr(v, "__await__"):
            return await v
        return v

    def invoke(self, args: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        """
        Sync execution helper.
        """
        return self(args=args, **kwargs)


class ToolRegistry:
    def __init__(self, tools: Sequence[Any], *, existing_names: Optional[Sequence[str]] = None):
        """
        Registry with unique tool names.
        Accepts mixed inputs (ToolSpec / callable / BaseModel subclass).
        """
        existing = set(existing_names or [])
        normalized: List[ToolSpec] = []
        for t in tools:
            spec = tool_spec_from(t)
            if spec.name in existing:
                raise ValueError(f"duplicate tool name: {spec.name}")
            existing.add(spec.name)
            normalized.append(spec)
        self._tools: Dict[str, ToolSpec] = {t.name: t for t in normalized}

    @property
    def tools_by_name(self) -> Dict[str, ToolSpec]:
        return dict(self._tools)

    def register(self, tool: Any) -> None:
        spec = tool_spec_from(tool)
        if spec.name in self._tools:
            raise ValueError(f"duplicate tool name: {spec.name}")
        self._tools[spec.name] = spec

    def to_llm_tools(self) -> List[LLMTool]:
        return [t.to_llm_tool() for t in self._tools.values()]

    def get(self, name: str) -> Optional[ToolSpec]:
        return self._tools.get(name)

    def require(self, name: str) -> ToolSpec:
        t = self.get(name)
        if t is None:
            raise KeyError(f"unknown tool: {name}")
        return t


@dataclass(frozen=True)
class BoundLLMService:
    """
    A lightweight wrapper that mimics `model.bind_tools(tools)`:
    it only binds tool schema + tool_choice defaults.

    NOTE: executing tool calls still requires a "tool loop" (see `run_tool_loop_complete`).
    """

    llm: LLMService
    tools: Sequence[ToolSpec]
    tool_choice: Any = "auto"

    def _bind(self, request: LLMRequest) -> LLMRequest:
        # Do not mutate original request object.
        reg = ToolRegistry(self.tools)
        return LLMRequest(
            messages=list(request.messages or []),
            system_prompt=request.system_prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            parse_json=request.parse_json,
            tools=reg.to_llm_tools(),
            tool_choice=self.tool_choice if request.tool_choice is None else request.tool_choice,
            extra=dict(request.extra or {}),
        )

    async def complete(self, request: LLMRequest) -> LLMResponse:
        return await self.llm.complete(self._bind(request))

    async def stream(self, request: LLMRequest):
        async for ch in self.llm.stream(self._bind(request)):
            yield ch

    async def close(self) -> None:
        await self.llm.close()


def _type_to_schema(tp: Any) -> Dict[str, Any]:
    """
    Best-effort mapping from Python type hints to JSON schema.
    Keep it intentionally small; callers can always pass `parameters=...` explicitly.
    """
    origin = get_origin(tp)
    args = get_args(tp)

    # Optional[T] == Union[T, None]
    if origin is Union and args:
        non_none = [a for a in args if a is not type(None)]  # noqa: E721
        if len(non_none) == 1:
            return _type_to_schema(non_none[0])
        return {"anyOf": [_type_to_schema(a) for a in non_none]}

    # Literal
    if str(origin) == "typing.Literal" and args:
        return {"enum": list(args)}

    if tp in (str,):
        return {"type": "string"}
    if tp in (int,):
        return {"type": "integer"}
    if tp in (float,):
        return {"type": "number"}
    if tp in (bool,):
        return {"type": "boolean"}

    if origin in (list, List) and args:
        return {"type": "array", "items": _type_to_schema(args[0])}
    if origin in (dict, Dict):
        # keep open; providers typically accept object without deep constraints
        return {"type": "object"}

    # fallback
    return {"type": "string"}


def schema_from_callable(fn: Any) -> Dict[str, Any]:
    """
    Build a JSON schema from a callable signature + type hints.
    """
    sig = inspect.signature(fn)
    try:
        hints = getattr(fn, "__annotations__", {}) or {}
    except Exception:
        hints = {}

    properties: Dict[str, Any] = {}
    required: List[str] = []

    for name, p in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        if p.kind in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
            continue

        schema = _type_to_schema(hints.get(name, str))
        properties[name] = schema
        if p.default is inspect._empty:
            # required unless explicitly Optional[...] (best-effort: treat as required anyway)
            required.append(name)

    out: Dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        out["required"] = required
    return out


def tool_spec_from(
    obj: Any,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None,
    fn: Optional[ToolFn] = None,
) -> ToolSpec:
    """
    Convert a callable / ToolSpec / (optional) pydantic BaseModel into ToolSpec.
    """
    if isinstance(obj, ToolSpec):
        return obj

    # pydantic BaseModel subclass as argument schema (signal tools often only need schema)
    if BaseModel is not None:
        try:
            if isinstance(obj, type) and issubclass(obj, BaseModel):  # type: ignore[arg-type]
                schema = obj.model_json_schema()  # type: ignore[union-attr]
                # Merge explicit description + docstring (both matter).
                doc = (inspect.getdoc(obj) or "").strip()
                desc = (description or "").strip()
                merged_desc = "\n\n".join([s for s in [desc, doc] if s])
                return ToolSpec(
                    name=str(name or getattr(obj, "__name__", "Tool")),
                    description=merged_desc or "",
                    parameters=parameters or schema,
                    fn=fn,
                    raw=obj,
                )
        except Exception:
            pass

    # Plain class as a "signal tool" (schema-only), inspired by agent-psychology's BaseModel tools.
    # We only treat it as a tool when it is clearly intended as a declaration:
    # - no explicit parameters provided
    # - no execution fn provided
    # Otherwise, fall through to the callable branch (which will treat it as a constructor).
    if isinstance(obj, type) and parameters is None and fn is None:
        doc = (inspect.getdoc(obj) or "").strip()
        desc = (description or "").strip()
        merged_desc = "\n\n".join([s for s in [desc, doc] if s])
        return ToolSpec(
            name=str(name or getattr(obj, "__name__", "Tool")),
            description=merged_desc or "",
            parameters={"type": "object", "properties": {}},
            fn=None,
            raw=obj,
        )

    # callable (function / instance with __call__)
    if callable(obj):
        target = obj
        spec_name = str(name or getattr(obj, "__name__", obj.__class__.__name__))
        # Merge explicit description + docstring (both matter).
        doc = (inspect.getdoc(obj) or "").strip()
        desc = (description or "").strip()
        merged_desc = "\n\n".join([s for s in [desc, doc] if s])
        params = parameters or schema_from_callable(target)

        def _wrapped(args: Dict[str, Any]) -> Any:
            # Prefer kwargs call (common tool signature). Fallback to single-arg call for "dict tools".
            try:
                return target(**(args or {}))
            except TypeError:
                return target(args or {})

        return ToolSpec(
            name=spec_name,
            description=merged_desc or "",
            parameters=params,
            fn=fn or _wrapped,
            raw=target,
        )

    raise TypeError(f"Unsupported tool spec type: {type(obj)}")


def tool(
    _fn: Optional[Callable[..., Any]] = None,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Decorator to define a tool quickly (LangChain-like), without LangChain dependency.

    Example:
    @tool(description="Add two numbers")
    def add(a: float, b: float) -> float:
        return a + b
    """

    def _wrap(fn: Callable[..., Any]) -> ToolSpec:
        return tool_spec_from(
            fn,
            name=name,
            description=description,
            parameters=parameters,
            # Let `tool_spec_from` wrap the callable so it can be executed with `args: dict`.
            fn=None,
        )

    if _fn is not None:
        return _wrap(_fn)
    return _wrap


def bind_tools(
    llm: LLMService,
    tools: Sequence[Any],
    *,
    tool_choice: Any = "auto",
) -> BoundLLMService:
    """
    Convenience: accept mixed tool declarations (ToolSpec / decorated function / callable / BaseModel subclass),
    normalize them, then bind onto the LLMService.
    """
    reg = ToolRegistry(tools)
    normalized: List[ToolSpec] = list(reg.tools_by_name.values())
    return BoundLLMService(llm=llm, tools=normalized, tool_choice=tool_choice)


def _best_effort_json_loads(s: str) -> Optional[Dict[str, Any]]:
    s = (s or "").strip()
    if not s:
        return None
    try:
        obj = json.loads(s)
        if isinstance(obj, dict):
            return obj
        # tool args are expected to be an object; keep best-effort
        return {"_": obj}
    except Exception:
        return None


def extract_tool_calls(
    resp: LLMResponse,
) -> List[Dict[str, Any]]:
    """
    Normalize tool calls from `LLMResponse` into a simple, execution-friendly shape.

    Output:
    - [{"id": "...", "name": "...", "args": {...}, "args_raw": "..."}]
    This is intentionally similar to how `agent-psychology` prepares tool execution.
    """
    out: List[Dict[str, Any]] = []
    for tc in resp.get_tool_calls():
        if not isinstance(tc, dict):
            continue
        fn = tc.get("function") or {}
        if not isinstance(fn, dict):
            # best-effort: tool_calls might be pydantic objects already dumped upstream
            try:
                fn = dict(getattr(fn, "__dict__", {}) or {})
            except Exception:
                fn = {}
        name = fn.get("name") or ""
        args_raw = fn.get("arguments", "") or ""
        args = _best_effort_json_loads(str(args_raw)) or {}
        out.append(
            {
                "id": str(tc.get("id") or ""),
                "name": str(name),
                "args": args,
                "args_raw": str(args_raw),
            }
        )
    return out


def tool_message(
    *,
    tool_call_id: str,
    content: Any,
) -> LLMMessage:
    """
    Create a `role="tool"` message for feeding tool execution results back into the LLM.
    """
    if isinstance(content, str):
        payload = content
    else:
        try:
            payload = json.dumps(content, ensure_ascii=False)
        except Exception:
            payload = str(content)
    return {"role": "tool", "tool_call_id": str(tool_call_id or ""), "content": payload}


def tool_messages_from_observations(
    *,
    tool_calls: Sequence[Dict[str, Any]],
    observations: Sequence[Any],
) -> List[LLMMessage]:
    """
    Build tool messages from executed observations.

    Typical usage:
    - tool_calls = extract_tool_calls(resp)
    - observations = await asyncio.gather(...)
    - messages += tool_messages_from_observations(tool_calls=tool_calls, observations=observations)
    """
    msgs: List[LLMMessage] = []
    for tc, obs in zip(tool_calls, observations):
        msgs.append(tool_message(tool_call_id=str(tc.get("id") or ""), content=obs))
    return msgs


async def execute_tool_safely(tool: ToolSpec, args: Dict[str, Any]) -> Any:
    """
    Safely execute a tool with error handling.
    Mirrors the spirit of agent-psychology's execute_tool_safely, without LangChain dependency.
    """
    try:
        return await tool.ainvoke(args)
    except Exception as e:
        return {"error": f"tool_error:{tool.name}: {e}"}


