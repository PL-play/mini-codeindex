from __future__ import annotations

import json
import logging
import os
from operator import add
from typing import Annotated, Any, Dict, List, TypedDict

from langgraph.graph import END, StateGraph
from langgraph.types import Command

from utils.interface import LLMRequest, OpenAICompatibleChatConfig
from utils.llm_factory import OpenAICompatibleChatLLMService
from utils.llm_utils import log_llm_json_result


logger = logging.getLogger(__name__)


class GraphState(TypedDict):
    """State for retrieval graph nodes."""

    query: str  # Original user query
    rewrite: Dict[str, Any]  # Raw structured rewrite payload
    rewritten_queries: Annotated[List[str], add]  # Accumulator across nodes
    notes: str  # Status or debug notes


REWRITE_SCHEMA = 'Return JSON only (no markdown, no extra text). Output MUST be: ["q1", "q2", ...]'

REWRITE_SYSTEM_PROMPT = (
    "You are a query rewriting assistant for code search. Split the user's query into\n"
    "1-5 short, concrete sub-queries for embedding + retrieval. If the query is atomic,\n"
    "return a single-item list with the original query.\n\n"
    "Examples:\n"
    'User: "如何在检索阶段做去重和 rerank，同时保持 chunk 的行号？"\n'
    'Output: ["检索 去重", "rerank 重排", "chunk 行号 元数据"]\n'
    'User: "vector store 查询、过滤 path、限制结果数"\n'
    'Output: ["vector store query", "where path filter", "n_results limit"]\n'
    'User: "embedding 维度不一致"\n'
    'Output: ["embedding dims", "dimension mismatch", "truncate embedding dims"]\n\n'
    f"{REWRITE_SCHEMA}"
)


ENV_REWRITE_BASE_URL = "REWRITE_BASE_URL"
ENV_REWRITE_API_KEY = "REWRITE_API_KEY"
ENV_REWRITE_MODEL = "REWRITE_MODEL"


async def rewrite_query_node(state: GraphState) -> Command:
    query = str(state.get("query", "") or "").strip()
    if not query:
        rewrite = {"rewritten_queries": [], "notes": "empty query", "strategy": "empty"}
        return Command(
            update={"query": "", "rewrite": rewrite, "rewritten_queries": [], "notes": rewrite["notes"]}
        )

    base_url = os.getenv(ENV_REWRITE_BASE_URL, "").strip() or "https://api.openai.com/v1"
    api_key = os.getenv(ENV_REWRITE_API_KEY, "").strip()
    model = os.getenv(ENV_REWRITE_MODEL, "").strip()
    cfg = OpenAICompatibleChatConfig(base_url=base_url, api_key=api_key, model=model)
    if not cfg.is_ready:
        logger.warning(
            "rewrite_query: LLM config missing (env %s/%s/%s), returning original query",
            ENV_REWRITE_BASE_URL,
            ENV_REWRITE_API_KEY,
            ENV_REWRITE_MODEL,
        )
        rewrite = {"rewritten_queries": [query], "notes": "llm_not_ready", "strategy": "no_client"}
        return Command(
            update={
                "rewrite": rewrite,
                "rewritten_queries": rewrite["rewritten_queries"],
                "notes": rewrite["notes"],
            }
        )

    client = OpenAICompatibleChatLLMService(cfg)

    req = LLMRequest.from_prompt(
        prompt=query,
        system_prompt=REWRITE_SYSTEM_PROMPT,
        parse_json=False,
        temperature=0.0,
        max_tokens=1000,
    )
    resp = await client.complete(req)
    log_llm_json_result(logger, resp, prefix="[rewrite_query]")

    raw_text = (resp.raw_text or "").strip()
    data: Any = None
    if raw_text:
        try:
            data = json.loads(raw_text)
        except Exception as e:
            logger.error(e)
            data = None

    if not isinstance(data, list):
        rewrite = {"rewritten_queries": [query], "notes": "llm_parse_failed", "strategy": "parse_failed"}
        return Command(
            update={
                "rewrite": rewrite,
                "rewritten_queries": rewrite["rewritten_queries"],
                "notes": rewrite["notes"],
            }
        )

    rewritten = [str(s).strip() for s in data if str(s).strip()]
    if not rewritten:
        rewritten = [query]
    notes = "llm_ok"
    rewrite = {"rewritten_queries": rewritten[:5], "notes": notes, "strategy": "llm_json"}

    return Command(
        update={
            "rewrite": rewrite,
            "rewritten_queries": rewrite["rewritten_queries"],
            "notes": rewrite["notes"],
        }
    )


def build_retrieval_graph() -> Any:
    graph = StateGraph(GraphState)
    graph.add_node("rewrite_query", rewrite_query_node)
    graph.set_entry_point("rewrite_query")
    graph.add_edge("rewrite_query", END)
    return graph.compile()
