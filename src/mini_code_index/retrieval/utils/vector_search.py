from __future__ import annotations

import asyncio
import json
import os
from typing import Any, Dict, List, Mapping, Optional
from urllib.parse import urlparse

from mini_code_index.db import _collection_name_for_root
from mini_code_index.embedding import OpenAICompatibleEmbedder


def _to_json_str(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _compact_metadata(meta: Mapping[str, Any]) -> Dict[str, Any]:
    keep_keys = [
        "path",
        "relpath",
        "language",
        "chunk_kind",
        "symbol_names",
        "start_line",
        "end_line",
        "start_col",
        "end_col",
        "scope_path_str",
    ]
    compact: Dict[str, Any] = {}
    for key in keep_keys:
        if key in meta:
            compact[key] = meta.get(key)
    return compact


async def code_vector_search_tool(
    query: str,
    *,
    root_dir: str,
    n_results: int = 5,
) -> str:
    """LLM Tool: Run vector-based code search in ChromaDB and return JSON as a string.

    Args:
        query: User query text to embed and search.
        root_dir: Project root directory used to derive the collection name.
        n_results: Number of top results to return.

    Returns:
        JSON string encoding:
            {
              "query": str,
              "collection": str,
              "root_dir": str,
              "results": [
                {
                  "id": str,
                  "distance": float,
                  "document": str,
                                    "metadata": {
                                        "path": str,              # absolute file path
                                        "relpath": str,           # project-relative path
                                        "language": str,          # detected language
                                        "chunk_kind": str,        # e.g. code/comment
                                        "symbol_names": str,      # symbol identifier string
                                        "start_line": int,
                                        "end_line": int,
                                        "start_col": int,
                                        "end_col": int,
                                        "scope_path_str": str     # hierarchical scope path, e.g. file::class::function
                                    }
                }
              ]
            }

    Usage:
        await code_vector_search_tool(
            "decorate",
            root_dir="/repo",
            n_results=3,
        )
    """
    chroma_url = (
        os.environ.get("CHROMADB_HOST")
        or os.environ.get("CHROMA_URL")
        or "http://127.0.0.1:8010"
    )

    try:
        import chromadb  # type: ignore
        from chromadb.config import Settings  # type: ignore
    except Exception as e:  # pragma: nocover
        return _to_json_str({"error": f"chromadb not available: {e}"})

    parsed = urlparse(chroma_url)
    client = chromadb.HttpClient(
        host=parsed.hostname or "127.0.0.1",
        port=int(parsed.port or 8000),
        settings=Settings(anonymized_telemetry=False),
    )

    collection_name = _collection_name_for_root(root_dir)
    try:
        collection = client.get_collection(collection_name)
    except Exception as e:
        return _to_json_str({"error": f"collection not found: {e}", "collection": collection_name})

    where_filter = {"$and": [{"chunk_kind": "code"}, {"is_comment": False}, {"is_trivia": False}]}
    include_fields = ["metadatas", "documents", "distances"]

    try:
        embedder = OpenAICompatibleEmbedder.from_env()
    except Exception as e:
        return _to_json_str({"error": f"embedder config missing: {e}"})

    async with embedder:
        embedding = (await embedder.embed([query]))[0]

    results = await asyncio.to_thread(
        collection.query,
        query_embeddings=[embedding],
        n_results=n_results,
        where=where_filter,
        include=include_fields,
    )

    ids = (results or {}).get("ids") or [[]]
    distances = (results or {}).get("distances") or [[]]
    documents = (results or {}).get("documents") or [[]]
    metadatas = (results or {}).get("metadatas") or [[]]

    items: List[Dict[str, Any]] = []
    for i, item_id in enumerate(ids[0]):
        meta = metadatas[0][i] if i < len(metadatas[0]) and isinstance(metadatas[0][i], dict) else {}
        items.append(
            {
                "id": item_id,
                "distance": distances[0][i] if i < len(distances[0]) else None,
                "document": documents[0][i] if i < len(documents[0]) else None,
                "metadata": _compact_metadata(meta),
            }
        )

    return _to_json_str(
        {
            "query": query,
            "collection": collection_name,
            "root_dir": root_dir,
            "results": items,
        }
    )
