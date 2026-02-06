"""
LLM factory utilities for zrag.

This module provides a small, explicit way to build an OpenAI-compatible `LLMService`
from environment / `src.config.settings`, similar in spirit to agent-psychology's
model utilities, but adapted to zrag's `LLMService` Protocol.
"""

from __future__ import annotations

import logging
import asyncio
import random
from typing import cast, Protocol, TypedDict, Literal
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Dict, List, Optional, Sequence, Tuple

from openai import AsyncOpenAI, AsyncStream

from .interface import LLMService, OpenAICompatibleChatConfig, LLMTokenUsage, LLMRequest, LLMResponse, \
    LLMStreamChunk
from .llm_utils import parse_json_from_model_output_detailed

try:
    from openai.types.chat import ChatCompletion, ChatCompletionMessage, \
        ChatCompletionChunk  # type: ignore[import-not-found]
except Exception as e:  # pragma: no cover
    # Runtime will still work because we treat these as typing-only. Keep minimal fallback.
    ChatCompletion = Any  # type: ignore[assignment]
    ChatCompletionMessage = Any  # type: ignore[assignment]

logger = logging.getLogger(__name__)




class OpenAICompatibleChatLLMService(LLMService):
    """
    Minimal OpenAI-compatible chat completion client.

    - Uses `openai.AsyncOpenAI`
    - Records token usage from response.usage (if present)
    - Implements zrag's `LLMService` protocol and an optional `get_last_token_usage()`
    """

    def __init__(self, cfg: OpenAICompatibleChatConfig):
        self._cfg = cfg
        self._client: Any = None
        self._last_usage: Dict[str, int] = {}

        logger.info(
            "GraphExtractor LLM: base_url=%s model=%s timeout_s=%s max_tokens=%s temperature=%s api_key=%s",
            cfg.base_url,
            cfg.model,
            cfg.timeout_s,
            cfg.max_tokens,
            cfg.temperature,
            "set" if bool(cfg.api_key) else "missing",
        )

    def get_last_token_usage(self) -> Dict[str, int]:
        return dict(self._last_usage or {})

    def _ensure_client(self) -> Any:
        if self._client is not None:
            return self._client
        from openai import AsyncOpenAI  # type: ignore

        self._client = AsyncOpenAI(
            base_url=self._cfg.base_url,
            api_key=self._cfg.api_key,
            timeout=self._cfg.timeout_s,
        )
        return self._client

    async def close(self) -> None:
        """
        Close underlying HTTP resources (httpx) to avoid ResourceWarning in tests.
        """
        if self._client is None:
            return
        try:
            # openai.AsyncOpenAI exposes `close()` (async).
            await self._client.close()
        finally:
            self._client = None

    def _record_usage(self, usage: Any, *, method: str) -> None:
        self._last_usage = self._usage_dict_from_any(usage)

        if self._last_usage.get("total_tokens"):
            logger.info(
                "[llm:%s] token_usage prompt=%s completion=%s total=%s",
                method,
                self._last_usage.get("prompt_tokens", 0),
                self._last_usage.get("completion_tokens", 0),
                self._last_usage.get("total_tokens", 0),
            )

    def _usage_dict_from_any(self, usage: Any) -> Dict[str, int]:
        """
        Normalize token usage from various provider shapes.
        Supports:
        - OpenAI usage: prompt_tokens/completion_tokens/total_tokens
        - Some providers: input_tokens/output_tokens/total_tokens
        - Dict payloads (from model_dump / raw json)
        """
        if usage is None:
            return {}

        # dict-like
        if isinstance(usage, dict):
            prompt = usage.get("prompt_tokens", usage.get("input_tokens", 0)) or 0
            completion = usage.get("completion_tokens", usage.get("output_tokens", 0)) or 0
            total = usage.get("total_tokens", 0) or 0
            try:
                prompt_i = int(prompt)
            except Exception:
                prompt_i = 0
            try:
                completion_i = int(completion)
            except Exception:
                completion_i = 0
            try:
                total_i = int(total)
            except Exception:
                total_i = 0
            # some payloads omit total
            if total_i <= 0 and (prompt_i > 0 or completion_i > 0):
                total_i = prompt_i + completion_i
            return {
                "prompt_tokens": prompt_i,
                "completion_tokens": completion_i,
                "total_tokens": total_i,
            }

        # object-like
        try:
            prompt = int(getattr(usage, "prompt_tokens", getattr(usage, "input_tokens", 0)) or 0)
            completion = int(getattr(usage, "completion_tokens", getattr(usage, "output_tokens", 0)) or 0)
            total = int(getattr(usage, "total_tokens", 0) or 0)
            if total <= 0 and (prompt > 0 or completion > 0):
                total = prompt + completion
            return {
                "prompt_tokens": prompt,
                "completion_tokens": completion,
                "total_tokens": total,
            }
        except Exception:
            return {}

    def _usage_obj(self, usage: Any = None) -> LLMTokenUsage:
        d = self._last_usage if usage is None else self._usage_dict_from_any(usage)
        return LLMTokenUsage(
            prompt_tokens=int(d.get("prompt_tokens", 0) or 0),
            completion_tokens=int(d.get("completion_tokens", 0) or 0),
            total_tokens=int(d.get("total_tokens", 0) or 0),
        )

    async def _with_retries(self, fn, *, method: str) -> ChatCompletion:
        """
        Lightweight retry wrapper inspired by LangChain's ergonomics.
        """
        last_err: Optional[Exception] = None
        attempts = max(1, int(self._cfg.max_retries) + 1)
        for i in range(attempts):
            try:
                return await fn()
            except Exception as e:
                last_err = e
                if i >= attempts - 1:
                    break
                # exponential backoff + jitter
                base = float(self._cfg.retry_base_delay_s)
                delay = base * (2 ** i) * (0.75 + 0.5 * random.random())
                logger.warning("[llm:%s] call failed (attempt %s/%s), retrying in %.2fs: %s", method, i + 1, attempts,
                               delay, e)
                await asyncio.sleep(delay)
        raise cast(Exception, last_err)

    def _request_kwargs(self, request: LLMRequest) -> Dict[str, Any]:
        """
        Map `LLMRequest` into kwargs for OpenAI-compatible chat.completions.create.
        """
        out: Dict[str, Any] = dict(request.extra or {})
        if request.model:
            out["model"] = request.model
        if request.temperature is not None:
            out["temperature"] = float(request.temperature)
        if request.max_tokens is not None:
            out["max_tokens"] = int(request.max_tokens)
        if request.tools is not None:
            out["tools"] = request.tools
        if request.tool_choice is not None:
            out["tool_choice"] = request.tool_choice
        return out

    async def complete(self, request: LLMRequest) -> LLMResponse:
        """
        Canonical non-streaming API (preferred).
        """
        resp = await self.chat_completion(messages=request.to_messages(), **self._request_kwargs(request))

        msg: Any = None
        try:
            msg = resp.choices[0].message
        except Exception as e:
            logger.error("[llm:complete] failed to extract message: %s", e)

        text = self._message_text(cast(ChatCompletionMessage, msg)) if msg is not None else ""

        if request.parse_json:
            res = parse_json_from_model_output_detailed(text)
        else:
            res = LLMResponse(raw_text=text, content_text=text)

        # IMPORTANT: do NOT rely on shared `self._last_usage` here (race under concurrency).
        usage_obj = getattr(resp, "usage", None)
        if usage_obj is None and hasattr(resp, "model_dump"):
            try:
                dumped = resp.model_dump()
                if isinstance(dumped, dict):
                    usage_obj = dumped.get("usage") or dumped.get("x_openai_usage") or dumped.get("x_usage")
            except Exception:
                pass
        res.token_usage = self._usage_obj(usage_obj)
        res.raw_message = msg
        res.raw_completion = resp
        return res

    async def stream(self, request: LLMRequest) -> AsyncIterator[LLMStreamChunk]:
        """
        Streaming API.

        Best-effort real streaming for OpenAI-compatible servers.
        If provider does not support streaming, callers can switch to `complete()`.
        """
        client: AsyncOpenAI = self._ensure_client()
        kwargs = self._request_kwargs(request)

        stream_kwargs = dict(kwargs)
        stream_kwargs["stream"] = True
        stream_kwargs.setdefault("stream_options", {"include_usage": True})

        stream: ChatCompletion | AsyncStream[ChatCompletionChunk] = await client.chat.completions.create(
            model=stream_kwargs.get("model") or self._cfg.model,
            messages=request.to_messages(),
            temperature=stream_kwargs.get("temperature", self._cfg.temperature),
            max_tokens=stream_kwargs.get("max_tokens", self._cfg.max_tokens),
            **{k: v for k, v in stream_kwargs.items() if k not in {"model", "temperature", "max_tokens"}},
        )

        last_event: Optional[ChatCompletionChunk] = None
        final_usage: Optional[LLMTokenUsage] = None
        tool_call_store: Dict[str, Dict[str, Any]] = {}
        tool_call_order: List[str] = []

        def _as_dict(obj: Any) -> Any:
            if obj is None:
                return None
            if isinstance(obj, dict):
                return obj
            if hasattr(obj, "model_dump"):
                try:
                    return obj.model_dump()
                except Exception:
                    return obj
            # best-effort: fallback to __dict__
            try:
                return dict(obj.__dict__)
            except Exception:
                return obj

        def _merge_tool_calls_delta(delta_tool_calls_obj: Any) -> List[Dict[str, Any]]:
            """
            Merge OpenAI-compatible streaming `delta.tool_calls` into an aggregated list.

            Delta items commonly look like:
            {"index":0,"id":"...","type":"function","function":{"name":"x","arguments":"{...partial..."}}
            """
            if not delta_tool_calls_obj:
                # return current snapshot
                return [tool_call_store[k] for k in tool_call_order]

            items = delta_tool_calls_obj
            # sometimes it's a single object
            if not isinstance(items, list):
                items = [items]

            for it in items:
                d = _as_dict(it)
                if not isinstance(d, dict):
                    continue
                call_id = str(d.get("id") or d.get("index") or "")
                if not call_id:
                    # fall back to sequential synthetic id
                    call_id = f"idx_{len(tool_call_order)}"

                if call_id not in tool_call_store:
                    tool_call_store[call_id] = {
                        "id": d.get("id") or call_id,
                        "type": d.get("type") or "function",
                        "function": {"name": "", "arguments": ""},
                    }
                    tool_call_order.append(call_id)

                entry = tool_call_store[call_id]
                fn = d.get("function") or {}
                if not isinstance(fn, dict):
                    fn = _as_dict(fn) or {}
                if isinstance(fn, dict):
                    name = fn.get("name")
                    if name:
                        entry["function"]["name"] = name
                    args = fn.get("arguments")
                    if args:
                        entry["function"]["arguments"] = (entry["function"].get("arguments") or "") + str(args)

                # allow other keys to be updated if present
                if d.get("type"):
                    entry["type"] = d.get("type")

            return [tool_call_store[k] for k in tool_call_order]

        async for event in stream:
            delta_text = ""
            event: ChatCompletionChunk = event
            last_event = event
            delta_tool_calls: Any = None
            aggregated_tool_calls: List[Dict[str, Any]] = []
            try:
                choice0 = event.choices[0]
                delta = getattr(choice0, "delta", None)
                delta_text = getattr(delta, "content", "") or ""
                delta_tool_calls = getattr(delta, "tool_calls", None)
                aggregated_tool_calls = _merge_tool_calls_delta(delta_tool_calls)
            except Exception as e:
                delta_text = ""
                delta_tool_calls = None
                aggregated_tool_calls = [tool_call_store[k] for k in tool_call_order]
                logger.error("[llm:stream] failed to extract delta: %s", e)
            # Some providers send usage only on the final event when stream_options.include_usage is enabled.
            try:
                usage_obj = getattr(event, "usage", None)
                # Fallback: some SDKs/providers only expose usage via model_dump / extra fields.
                if usage_obj is None and hasattr(event, "model_dump"):
                    try:
                        dumped = event.model_dump()
                        if isinstance(dumped, dict):
                            usage_obj = dumped.get("usage") or dumped.get("x_openai_usage") or dumped.get("x_usage")
                    except Exception:
                        pass
                if usage_obj is not None:
                    # also record into last_usage so callers relying on _usage_obj() can still work
                    self._record_usage(usage_obj, method="stream")
                    final_usage = self._usage_obj(usage_obj)
            except Exception:
                # Don't fail streaming if usage parsing fails.
                pass

            if delta_text or delta_tool_calls:
                yield LLMStreamChunk(
                    delta_text=delta_text,
                    delta_tool_calls=delta_tool_calls,
                    tool_calls=aggregated_tool_calls,
                    token_usage=None,
                    raw_event=event,
                    is_final=False,
                )

        # Final chunk carries best-effort usage + last raw event so callers can inspect finish_reason, tool_calls, etc.
        yield LLMStreamChunk(
            delta_text="",
            delta_tool_calls=None,
            tool_calls=[tool_call_store[k] for k in tool_call_order],
            token_usage=final_usage,
            raw_event=last_event,
            is_final=True,
        )

    async def chat_completion(
            self,
            *,
            messages: Sequence[Dict[str, str]],
            **kwargs: Any,
    ) -> ChatCompletion:
        """
        Return the raw ChatCompletion object.
        """
        client = self._ensure_client()
        model = str(kwargs.get("model") or self._cfg.model)
        temperature = float(kwargs.get("temperature", self._cfg.temperature))
        max_tokens = int(kwargs.get("max_tokens", self._cfg.max_tokens))

        async def _call() -> ChatCompletion:
            return await client.chat.completions.create(
                model=model,
                messages=list(messages),
                temperature=temperature,
                max_tokens=max_tokens,
                **{k: v for k, v in kwargs.items() if k not in {"model", "temperature", "max_tokens"}},
            )

        resp: ChatCompletion = await self._with_retries(_call, method="chat_completion")
        usage_obj = getattr(resp, "usage", None)
        if usage_obj is None and hasattr(resp, "model_dump"):
            try:
                dumped = resp.model_dump()
                if isinstance(dumped, dict):
                    usage_obj = dumped.get("usage") or dumped.get("x_openai_usage") or dumped.get("x_usage")
            except Exception:
                pass
        self._record_usage(usage_obj, method="chat_completion")
        return resp

    def _message_text(self, msg: ChatCompletionMessage) -> str:
        """
        Convert a ChatCompletionMessage content to plain text.
        Some providers may return list content; we best-effort stringify.
        """
        content = getattr(msg, "content", None)
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        # List/parts fallback
        try:
            return "".join(str(part) for part in content).strip()
        except Exception:
            return str(content).strip()

    # NOTE: `predict/chat/predict_stream` wrappers are provided as default methods on the Protocol.