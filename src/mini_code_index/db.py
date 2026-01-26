from __future__ import annotations

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

    def ping(self) -> bool: ...

    def delete_by_path(self, *, path: str) -> None: ...

    def upsert(
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
    return "mci_" + hasher.hexdigest()[:59]


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

    def ping(self) -> bool:
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
                "chromadb is not installed. Install it with `pip install chromadb<=0.6.3` "
                "(or add it to your environment extras)."
            ) from e

        parsed = urlparse(self.base_url)
        host = parsed.hostname or "127.0.0.1"
        port = int(parsed.port or 8000)
        settings = Settings(anonymized_telemetry=False)
        self._client = chromadb.HttpClient(host=host, port=port, settings=settings)
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

    def delete_by_path(self, *, path: str) -> None:
        collection = self._ensure_collection()
        full = os.path.abspath(os.path.expanduser(path))
        collection.delete(where={"path": full})

    def upsert(
        self,
        *,
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
