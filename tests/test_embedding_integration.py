import os
import math
import pytest

from mini_code_index.embedding import OpenAICompatibleEmbedder
import dotenv
dotenv.load_dotenv()

def _cosine(a: list[float], b: list[float]) -> float:
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


def _integration_enabled() -> bool:
    # Opt-in gate to avoid accidental paid network calls in CI.
    return os.environ.get("MINI_CODE_INDEX_RUN_INTEGRATION") == "1"


@pytest.mark.skipif(not _integration_enabled(), reason="Set MINI_CODE_INDEX_RUN_INTEGRATION=1 to run paid network integration tests")
def test_openrouter_real_embedding_and_similarity_prints() -> None:
    # Requires:
    # - EMBEDDING_BINDING_API_KEY
    # - EMBEDDING_BINDING_HOST (e.g. https://openrouter.ai/api/v1)
    # - EMBEDDING_MODEL (e.g. qwen/qwen3-embedding-4b)
    # - EMBEDDING_DIM (optional)
    embedder = OpenAICompatibleEmbedder.from_env()

    texts = [
        "A function that adds two integers.",
        "A method that sums two numbers.",
        "How to cook pasta al dente?",
    ]
    vecs = embedder.embed(texts)

    print("model=", embedder.model)
    print("base_url=", embedder.base_url)
    print("n_vecs=", len(vecs))
    print("dim=", len(vecs[0]) if vecs else 0)
    for i, v in enumerate(vecs):
        preview = ", ".join(f"{x:.5f}" for x in v[:8])
        print(f"vec[{i}] first8= [{preview}]")

    assert len(vecs) == len(texts)
    assert all(len(v) == len(vecs[0]) for v in vecs)

    sim_0_1 = _cosine(vecs[0], vecs[1])
    sim_0_2 = _cosine(vecs[0], vecs[2])
    print("cos(0,1)=", sim_0_1)
    print("cos(0,2)=", sim_0_2)

    # Very loose sanity check: similar paraphrase should be closer than unrelated.
    assert sim_0_1 > sim_0_2
