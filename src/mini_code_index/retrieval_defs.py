from __future__ import annotations

from operator import add
from typing import Annotated, Any, Dict, List, TypedDict


class GraphState(TypedDict):
    """State for retrieval graph nodes."""

    query: str  # Original user query
    rewrite: Dict[str, Any]  # Raw structured rewrite payload
    rewritten_queries: Annotated[List[str], add]  # Accumulator across nodes
    notes: str  # Status or debug notes


REWRITE_SCHEMA = 'Return JSON only (no markdown, no extra text). Output MUST be: ["q1", "q2", ...]'

REWRITE_SYSTEM_PROMPT = (
    "You are a query rewriting assistant for code retrieval.\n"
    "Goal: maximize recall for code search by generating precise, code-oriented sub-queries.\n"
    "Split the input into 1-5 short, concrete queries that look like code or API terms.\n"
    "If the user provides long natural language, compress it into precise, technical\n"
    "sub-queries that surface likely identifiers, file paths, APIs, or concepts.\n"
    "- prefer identifiers, component names, function/class terms, file/path hints\n"
    "- include key nouns and technical terms; avoid verbose natural language\n"
    "- keep each query compact (aim ~6-20 tokens), but allow longer if needed for clarity\n"
    "If the query is already atomic, return a single-item list with the original query.\n\n"
    "Examples:\n"
    'User: "How do we deduplicate retrieval results and rerank while keeping chunk line numbers?"\n'
    'Output: ["retrieval dedup", "rerank", "chunk line numbers metadata"]\n'
    'User: "vector store query filtering path and limit results"\n'
    'Output: ["vector store query", "where path filter", "n_results limit"]\n'
    'User: "embedding dimension mismatch"\n'
    'Output: ["embedding dims", "dimension mismatch", "truncate embedding"]\n'
    'User: "How is query chunking implemented for code search?"\n'
    'Output: ["query chunking", "string chunker", "query rewrite"]\n\n'
    f"{REWRITE_SCHEMA}"
)


ENV_REWRITE_BASE_URL = "REWRITE_BASE_URL"
ENV_REWRITE_API_KEY = "REWRITE_API_KEY"
ENV_REWRITE_MODEL = "REWRITE_MODEL"
