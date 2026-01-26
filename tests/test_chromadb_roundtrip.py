import os
import uuid

import pytest


@pytest.mark.integration
def test_chromadb_roundtrip_python_client() -> None:
    """Create a collection, upsert one vector, query it back, then clean up.

    Requires:
    - ChromaDB running on localhost:8010 (docker compose)
    - chromadb python package installed

    Skips when not available.
    """

    try:
        import chromadb  # type: ignore
        from chromadb.config import Settings  # type: ignore
    except Exception as e:
        pytest.skip(f"chromadb python package not installed: {e}")

    base_url = os.environ.get("CHROMA_URL", "http://127.0.0.1:8010")
    parsed = __import__("urllib.parse").parse.urlparse(base_url)
    host = parsed.hostname or "127.0.0.1"
    port = int(parsed.port or 8010)

    client = chromadb.HttpClient(host=host, port=port, settings=Settings(anonymized_telemetry=False))

    # If the server is down, chromadb may raise during collection ops.
    name = f"mci_test_{uuid.uuid4().hex[:16]}"
    try:
        col = client.get_or_create_collection(name=name, metadata={"created-by": "mini-code-index-test"})
    except Exception as e:
        pytest.skip(f"ChromaDB not reachable at {base_url}: {e}")

    try:
        doc = "hello chroma"
        emb = [0.1, 0.2, 0.3]
        col.upsert(
            ids=["1"],
            documents=[doc],
            embeddings=[emb],
            metadatas=[{"path": "/tmp/hello.txt", "sha256": "test"}],
        )

        res = col.query(
            query_embeddings=[emb],
            n_results=1,
            include=["documents", "metadatas", "distances"],
        )
        assert res["ids"] and res["ids"][0][0] == "1"
        assert res["documents"] and res["documents"][0][0] == doc
    finally:
        # Always cleanup.
        client.delete_collection(name)
