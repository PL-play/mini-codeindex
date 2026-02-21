from __future__ import annotations

import asyncio
import hashlib
import os
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Protocol, Sequence
from urllib.parse import urlparse


class VectorStoreError(RuntimeError):
    pass


class VectorStore(Protocol):
    """Abstract storage backend.

    This is intentionally small for now. The goal is to let the indexing pipeline
    call into a backend without committing to Chroma's Python client yet.
    """

    async def ping(self) -> bool: ...

    async def get_one_by_path(self, *, path: str) -> Optional[Mapping[str, Any]]: ...

    async def delete_by_path(self, *, path: str) -> None: ...

    async def upsert(
        self,
        *,
        ids: Sequence[str],
        documents: Sequence[str],
        embeddings: Sequence[Sequence[float]],
        metadatas: Sequence[Mapping[str, Any]],
    ) -> None: ...



def _collection_name_for_root(root_dir: str) -> str:
    """Stable, short collection name for a project root.

    We intentionally avoid putting raw paths into collection names.
    """

    full = os.path.abspath(os.path.expanduser(root_dir))
    hasher = hashlib.sha256(full.encode("utf-8"))
    return hasher.hexdigest()[:63]


@dataclass
class ChromaStore(VectorStore):
    """ChromaDB backend using the official `chromadb` Python client.

    This targets a running Chroma server (docker-compose in your setup).
    """

    base_url: str = "http://127.0.0.1:8010"
    root_dir: Optional[str] = None
    collection_name: Optional[str] = None

    _client: Any = None
    _collection: Any = None

    def _heartbeat_urls(self) -> list[str]:
        root = self.base_url.rstrip("/")
        return [f"{root}/api/v2/heartbeat", f"{root}/api/v1/heartbeat"]

    async def ping(self) -> bool:
        return await asyncio.to_thread(self._ping_sync)

    def _ping_sync(self) -> bool:
        for url in self._heartbeat_urls():
            try:
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=1.5) as resp:
                    status = int(getattr(resp, "status", 200))
                if status == 200:
                    return True
            except (urllib.error.URLError, socket.timeout, TimeoutError):
                continue
        return False

    def _ensure_client(self) -> Any:
        if self._client is not None:
            return self._client

        try:
            import chromadb  # type: ignore
            from chromadb.config import Settings  # type: ignore
        except Exception as e:  # pragma: nocover
            raise VectorStoreError(
                "chromadb is not installed. Install it with `pip install chromadb==1.5.0` "
                "(or add it to your environment extras)."
            ) from e

        parsed = urlparse(self.base_url)
        host = parsed.hostname or "127.0.0.1"
        port = int(parsed.port or 8000)
        settings = Settings(anonymized_telemetry=False)
        
        # Bypass proxy for localhost/127.0.0.1 connections
        # This prevents issues when system proxy is configured
        import os
        old_no_proxy = os.environ.get("NO_PROXY")
        try:
            os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
            self._client = chromadb.HttpClient(host=host, port=port, settings=settings)
        finally:
            if old_no_proxy is not None:
                os.environ["NO_PROXY"] = old_no_proxy
            elif "NO_PROXY" in os.environ:
                del os.environ["NO_PROXY"]
        return self._client

    def _ensure_collection(self) -> Any:
        if self._collection is not None:
            return self._collection

        client = self._ensure_client()

        name = self.collection_name
        if not name:
            if not self.root_dir:
                raise ValueError("root_dir or collection_name must be provided")
            name = _collection_name_for_root(self.root_dir)
            self.collection_name = name

        meta: dict[str, Any] = {
            "created-by": "mini-code-index",
            "hostname": socket.gethostname(),
        }
        if self.root_dir is not None:
            meta["path"] = os.path.abspath(os.path.expanduser(self.root_dir))

        self._collection = client.get_or_create_collection(name=name, metadata=meta)
        return self._collection

    async def get_one_by_path(self, *, path: str) -> Optional[Mapping[str, Any]]:
        return await asyncio.to_thread(self._get_one_by_path_sync, path)

    def _get_one_by_path_sync(self, path: str) -> Optional[Mapping[str, Any]]:
        collection = self._ensure_collection()
        full = os.path.abspath(os.path.expanduser(path))
        try:
            result = collection.get(where={"path": full}, limit=1, include=["metadatas"])
        except TypeError:
            result = collection.get(where={"path": full}, include=["metadatas"])

        metadatas = (result or {}).get("metadatas") or []
        if not metadatas or not isinstance(metadatas[0], dict):
            return None
        return metadatas[0]

    async def delete_by_path(self, *, path: str) -> None:
        await asyncio.to_thread(self._delete_by_path_sync, path)

    def _delete_by_path_sync(self, path: str) -> None:
        collection = self._ensure_collection()
        full = os.path.abspath(os.path.expanduser(path))
        collection.delete(where={"path": full})

    async def upsert(
        self,
        *,
        ids: Sequence[str],
        documents: Sequence[str],
        embeddings: Sequence[Sequence[float]],
        metadatas: Sequence[Mapping[str, Any]],
    ) -> None:
        await asyncio.to_thread(
            self._upsert_sync,
            ids,
            documents,
            embeddings,
            metadatas,
        )

    def _upsert_sync(
        self,
        ids: Sequence[str],
        documents: Sequence[str],
        embeddings: Sequence[Sequence[float]],
        metadatas: Sequence[Mapping[str, Any]],
    ) -> None:
        if not (len(ids) == len(documents) == len(embeddings) == len(metadatas)):
            raise ValueError("ids/documents/embeddings/metadatas must have the same length")

        collection = self._ensure_collection()
        collection.upsert(
            ids=list(ids),
            documents=list(documents),
            embeddings=[list(map(float, v)) for v in embeddings],
            metadatas=[dict(m) for m in metadatas],
        )

