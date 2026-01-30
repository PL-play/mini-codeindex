from __future__ import annotations

import asyncio
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Iterable, Optional, Protocol, Sequence

import aiohttp
import logging


class EmbeddingError(RuntimeError):
    pass


logger = logging.getLogger(__name__)


class Embedder(Protocol):
    async def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


# Approximate token estimation: ~4 characters per token for English.
# This is a rough estimate; real tokenization depends on the model.
CHARS_PER_TOKEN_ESTIMATE = 4


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // CHARS_PER_TOKEN_ESTIMATE)


def _create_token_aware_batches(
    texts: Sequence[str], *, batch_size: int, token_limit: Optional[int]
) -> list[list[str]]:
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    if not token_limit:
        return [list(texts[i : i + batch_size]) for i in range(0, len(texts), batch_size)]

    token_counts = [_estimate_tokens(t) for t in texts]
    if token_counts and max(token_counts) > token_limit:
        raise EmbeddingError(
            f"Single input exceeds token limit ({token_limit} tokens)."
        )

    if sum(token_counts) <= token_limit:
        return [list(texts)]

    batches: list[list[str]] = []
    current: list[str] = []
    current_tokens = 0

    for t, t_tokens in zip(texts, token_counts):

        would_exceed_tokens = current_tokens + t_tokens > token_limit
        would_exceed_batch = len(current) >= batch_size

        if current and (would_exceed_tokens or would_exceed_batch):
            batches.append(current)
            current = []
            current_tokens = 0

        current.append(t)
        current_tokens += t_tokens

    if current:
        batches.append(current)
    return batches


def _parse_openai_embeddings_response(payload: dict[str, Any], n_expected: int) -> list[list[float]]:
    data = payload.get("data")
    if not isinstance(data, list):
        raise EmbeddingError("Invalid embeddings response: missing 'data' list")

    # OpenAI-compatible schema: each item has {index, embedding, object}
    by_index: dict[int, list[float]] = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        idx = item.get("index")
        emb = item.get("embedding")
        if isinstance(idx, int) and isinstance(emb, list) and all(
            isinstance(x, (int, float)) for x in emb
        ):
            by_index[idx] = [float(x) for x in emb]

    if len(by_index) != n_expected:
        raise EmbeddingError(
            f"Invalid embeddings response: expected {n_expected} vectors, got {len(by_index)}"
        )

    return [by_index[i] for i in range(n_expected)]


@dataclass
class OpenAICompatibleEmbedder:
    """Minimal OpenAI-compatible embeddings client.

    Targets the standard endpoint: POST {base_url}/v1/embeddings

    Env defaults:
    - OPENAI_API_KEY
    - OPENAI_BASE_URL (default: https://api.openai.com)
    - OPENAI_EMBEDDING_MODEL (default: text-embedding-3-small)

    Notes:
    - This module intentionally does NOT manage retries/backoff yet.
    - It preserves input order using the returned `index` field.
    """

    api_key: str
    model: str = "text-embedding-3-small"
    base_url: str = "https://api.openai.com"
    timeout_s: float = 60.0
    batch_size: int = 128
    dimensions: Optional[int] = None
    token_limit: Optional[int] = None
    max_retries: int = 3
    retry_delay_s: float = 1.0
    _session: Optional[aiohttp.ClientSession] = None

    @classmethod
    def from_env(cls) -> "OpenAICompatibleEmbedder":
        # Preferred env var set (matches your config style):
        # - EMBEDDING_BINDING_HOST, EMBEDDING_BINDING_API_KEY, EMBEDDING_MODEL, EMBEDDING_DIM, EMBEDDING_TOKEN_LIMIT
        api_key = os.environ.get("EMBEDDING_BINDING_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EmbeddingError("Missing EMBEDDING_BINDING_API_KEY (or OPENAI_API_KEY)")

        base_url = os.environ.get("EMBEDDING_BINDING_HOST") or os.environ.get(
            "OPENAI_BASE_URL", "https://api.openai.com"
        )
        model = os.environ.get("EMBEDDING_MODEL") or os.environ.get(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        )

        dims = os.environ.get("EMBEDDING_DIM") or os.environ.get("OPENAI_EMBEDDING_DIMS")
        dimensions = int(dims) if dims and str(dims).isdigit() else None

        tok = os.environ.get("EMBEDDING_TOKEN_LIMIT")
        token_limit = int(tok) if tok and str(tok).isdigit() else None

        # Optional tuning knobs (not required by your config, but useful).
        bs = os.environ.get("EMBEDDING_BATCH_SIZE")
        batch_size = int(bs) if bs and str(bs).isdigit() else 128

        to = os.environ.get("EMBEDDING_TIMEOUT_S")
        timeout_s = float(to) if to and str(to).replace(".", "", 1).isdigit() else 60.0

        mr = os.environ.get("EMBEDDING_MAX_RETRIES")
        max_retries = int(mr) if mr and str(mr).isdigit() else 3

        rd = os.environ.get("EMBEDDING_RETRY_DELAY_S")
        retry_delay_s = float(rd) if rd and str(rd).replace(".", "", 1).isdigit() else 1.0

        return cls(
            api_key=api_key,
            base_url=base_url,
            model=model,
            dimensions=dimensions,
            token_limit=token_limit,
            batch_size=batch_size,
            timeout_s=timeout_s,
            max_retries=max_retries,
            retry_delay_s=retry_delay_s,
        )

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout_s)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
        self._session = None

    async def __aenter__(self) -> "OpenAICompatibleEmbedder":
        await self._get_session()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    def _embeddings_url(self) -> str:
        """Build embeddings endpoint for OpenAI-compatible APIs.

        Some providers expose:
        - https://host/v1/embeddings
        Others (e.g. OpenRouter) may expose:
        - https://openrouter.ai/api/v1/embeddings
        """
        root = self.base_url.rstrip("/")
        if root.endswith("/v1"):
            return root + "/embeddings"
        return root + "/v1/embeddings"

    async def _request(self, inputs: Sequence[str]) -> dict[str, Any]:
        url = self._embeddings_url()

        # OpenRouter docs accept either a string input or a list input.
        # Using a string for single-item batches matches that behavior.
        _input: Any = list(inputs)
        if len(inputs) == 1:
            _input = inputs[0]

        body: dict[str, Any] = {"model": self.model, "input": _input}
        if self.dimensions is not None:
            body["dimensions"] = int(self.dimensions)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                session = await self._get_session()
                async with session.post(url, json=body, headers=headers) as resp:
                    raw = await resp.text()

                    if resp.status == 429:
                        retry_after = None
                        try:
                            ra = resp.headers.get("Retry-After") if resp.headers else None
                            retry_after = float(ra) if ra else None
                        except Exception:
                            retry_after = None
                        delay = (
                            retry_after
                            if retry_after is not None
                            else self.retry_delay_s * (2**attempt)
                        )
                        logger.warning(
                            "Embeddings HTTP 429. Retry %d/%d in %.2fs",
                            attempt + 1,
                            self.max_retries,
                            delay,
                        )
                        await asyncio.sleep(delay)
                        continue

                    if 500 <= resp.status < 600:
                        delay = self.retry_delay_s * (2**attempt)
                        logger.warning(
                            "Embeddings HTTP %d. Retry %d/%d in %.2fs",
                            resp.status,
                            attempt + 1,
                            self.max_retries,
                            delay,
                        )
                        await asyncio.sleep(delay)
                        continue

                    if resp.status >= 400:
                        raise EmbeddingError(
                            f"Embeddings HTTP error: {resp.status} {resp.reason} {raw}"
                        )

                    try:
                        payload = json.loads(raw)
                    except json.JSONDecodeError as e:
                        raise EmbeddingError("Embeddings response is not valid JSON") from e

                    if isinstance(payload, dict) and payload.get("error"):
                        err = payload.get("error") or {}
                        code = err.get("code", "unknown")
                        message = err.get("message", "unknown error")
                        raise EmbeddingError(f"Embeddings API error: {code} {message}")

                    return payload
            except (aiohttp.ClientConnectionError, asyncio.TimeoutError) as e:
                last_error = e
                delay = self.retry_delay_s * (2**attempt)
                logger.warning(
                    "Embeddings connection error: %s. Retry %d/%d in %.2fs",
                    e,
                    attempt + 1,
                    self.max_retries,
                    delay,
                )
                await asyncio.sleep(delay)
                continue
        else:
            raise EmbeddingError(f"Embeddings request failed after {self.max_retries} retries: {last_error}")

    async def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        vectors: list[list[float]] = []
        embed_start_time = time.time()
        text_lengths = [len(t) for t in texts]
        total_chars = sum(text_lengths)
        min_chars = min(text_lengths) if text_lengths else 0
        max_chars = max(text_lengths) if text_lengths else 0
        avg_chars = int(total_chars / len(texts)) if texts else 0
        logger.info(
            "[EMBED_INPUT] texts=%d chars(min/avg/max)=%d/%d/%d",
            len(texts),
            min_chars,
            avg_chars,
            max_chars,
        )
        batches = _create_token_aware_batches(
            list(texts), batch_size=self.batch_size, token_limit=self.token_limit
        )
        logger.debug(
            "[EMBED_BATCHING] %d texts -> %d batch(es) (max_batch=%d, token_limit=%s)",
            len(texts),
            len(batches),
            self.batch_size,
            str(self.token_limit),
        )
        
        batch_num = 0
        total_tokens = 0
        dims_seen: set[int] = set()
        for batch in batches:
            batch_num += 1
            approx_tokens = sum(_estimate_tokens(t) for t in batch)
            total_tokens += approx_tokens
            batch_chars = sum(len(t) for t in batch)
            logger.info(
                "    [BATCH %d] input_texts=%d chars=%d tokens=%d",
                batch_num,
                len(batch),
                batch_chars,
                approx_tokens,
            )
            logger.debug(
                "    [BATCH %d] size=%d tokens=%d model=%s",
                batch_num,
                len(batch),
                approx_tokens,
                self.model,
            )
            req_start = time.time()
            payload = await self._request(batch)
            req_elapsed = time.time() - req_start
            logger.debug("    [BATCH %d] API request completed (%.2fs)", batch_num, req_elapsed)
            batch_vectors = _parse_openai_embeddings_response(payload, n_expected=len(batch))
            if batch_vectors:
                dims_seen.add(len(batch_vectors[0]))
            logger.info(
                "    [BATCH %d] output_vectors=%d dim=%s",
                batch_num,
                len(batch_vectors),
                len(batch_vectors[0]) if batch_vectors else 0,
            )
            vectors.extend(batch_vectors)
        
        embed_elapsed = time.time() - embed_start_time
        dim_summary = ",".join(str(d) for d in sorted(dims_seen)) if dims_seen else "0"
        logger.info(
            "[EMBED_OUTPUT] vectors=%d dims=%s elapsed=%.2fs",
            len(vectors),
            dim_summary,
            embed_elapsed,
        )
        logger.debug(
            "[EMBED_SUMMARY] %d texts embedded | total_tokens=%d | elapsed=%.2fs",
            len(texts),
            total_tokens,
            embed_elapsed,
        )
        return vectors
