import os
import socket
import urllib.error
import urllib.request

import pytest


def _get_status_code(url: str, timeout_s: float = 1.5) -> int:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return int(getattr(resp, "status", 200))


@pytest.mark.integration
def test_chromadb_heartbeat_local_8010() -> None:
    """Verify a locally running ChromaDB is reachable.

    This is an integration test: it will be skipped if the server isn't running.

    Default target: http://127.0.0.1:8010
    Override with: CHROMA_URL=http://127.0.0.1:8010
    """

    base_url = os.environ.get("CHROMA_URL", "http://127.0.0.1:8010").rstrip("/")
    heartbeat_urls = [
        f"{base_url}/api/v2/heartbeat",
        f"{base_url}/api/v1/heartbeat",
    ]

    last_err: Exception | None = None
    for url in heartbeat_urls:
        try:
            status = _get_status_code(url)
        except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
            last_err = e
            continue
        assert status == 200
        return

    pytest.skip(f"ChromaDB is not reachable at {base_url}: {last_err}")
