from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Iterable, Optional, Protocol, Sequence


class EmbeddingError(RuntimeError):
    pass


class Embedder(Protocol):
    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


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

    batches: list[list[str]] = []
    current: list[str] = []
    current_tokens = 0

    for t in texts:
        t_tokens = _estimate_tokens(t)

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
    model: str = ""
    base_url: str = "https://api.openai.com"
    timeout_s: float = 60.0
    batch_size: int = 128
    dimensions: Optional[int] = None
    token_limit: Optional[int] = None
    max_retries: int = 3
    retry_delay_s: float = 1.0

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

    def _request(self, inputs: Sequence[str]) -> dict[str, Any]:
        url = self._embeddings_url()

        # OpenRouter docs accept either a string input or a list input.
        # Using a string for single-item batches matches that behavior.
        _input: Any = list(inputs)
        if len(inputs) == 1:
            _input = inputs[0]

        body: dict[str, Any] = {"model": self.model, "input": _input}
        if self.dimensions is not None:
            body["dimensions"] = int(self.dimensions)

        req = urllib.request.Request(
            url=url,
            method="POST",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                    raw = resp.read().decode("utf-8")
                break
            except urllib.error.HTTPError as e:
                last_error = e
                # Handle 429 + 5xx with backoff; other 4xx are treated as fatal.
                detail = ""
                try:
                    detail = e.read().decode("utf-8")
                except Exception:
                    pass

                if e.code == 429:
                    retry_after = None
                    try:
                        ra = e.headers.get("Retry-After") if e.headers else None
                        retry_after = float(ra) if ra else None
                    except Exception:
                        retry_after = None
                    delay = retry_after if retry_after is not None else self.retry_delay_s * (2**attempt)
                    time.sleep(delay)
                    continue
                if 500 <= e.code < 600:
                    delay = self.retry_delay_s * (2**attempt)
                    time.sleep(delay)
                    continue

                raise EmbeddingError(f"Embeddings HTTP error: {e.code} {e.reason} {detail}") from e
            except urllib.error.URLError as e:
                last_error = e
                delay = self.retry_delay_s * (2**attempt)
                time.sleep(delay)
                continue
        else:
            raise EmbeddingError(f"Embeddings request failed after {self.max_retries} retries: {last_error}")

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise EmbeddingError("Embeddings response is not valid JSON") from e

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        vectors: list[list[float]] = []
        batches = _create_token_aware_batches(
            list(texts), batch_size=self.batch_size, token_limit=self.token_limit
        )
        for batch in batches:
            payload = self._request(batch)
            vectors.extend(_parse_openai_embeddings_response(payload, n_expected=len(batch)))
        return vectors
