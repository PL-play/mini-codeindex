import math
import os

import dotenv
import pytest

from mini_code_index.embedding import OpenAICompatibleEmbedder


dotenv.load_dotenv()


_RUN_INTEGRATION = os.environ.get("MINI_CODE_INDEX_RUN_INTEGRATION") == "1"


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


def _print_vec_preview(idx: int, text: str, vec: list[float]) -> None:
    t_preview = text.replace("\n", "\\n")
    if len(t_preview) > 160:
        t_preview = t_preview[:160] + "..."
    v_preview = ", ".join(f"{x:.5f}" for x in vec[:8])
    print(f"[{idx}] text= {t_preview}")
    print(f"    vec_first8= [{v_preview}]")


def _run_case(
    *,
    title: str,
    embedder: OpenAICompatibleEmbedder,
    texts: list[str],
    positives: list[tuple[int, int]],
    negatives: list[tuple[int, int]],
) -> None:
    vecs = embedder.embed(texts)
    print("\n===", title, "===")
    print("model=", embedder.model)
    print("base_url=", embedder.base_url)
    print("n_texts=", len(texts), "dim=", len(vecs[0]) if vecs else 0)
    for i, (t, v) in enumerate(zip(texts, vecs)):
        _print_vec_preview(i, t, v)

    assert len(vecs) == len(texts)
    assert all(len(v) == len(vecs[0]) for v in vecs)

    pos_sims: list[float] = []
    neg_sims: list[float] = []
    for a, b in positives:
        s = _cosine(vecs[a], vecs[b])
        pos_sims.append(s)
        print(f"pos cos({a},{b})=", s)
    for a, b in negatives:
        s = _cosine(vecs[a], vecs[b])
        neg_sims.append(s)
        print(f"neg cos({a},{b})=", s)

    # Loose ordering check; avoid absolute thresholds.
    for ps in pos_sims:
        for ns in neg_sims:
            assert ps > ns


@pytest.mark.skipif(
    not _RUN_INTEGRATION,
    reason="Set MINI_CODE_INDEX_RUN_INTEGRATION=1 to run paid network integration tests",
)
def test_embed_nl_baseline_paraphrase_vs_unrelated() -> None:
    embedder = OpenAICompatibleEmbedder.from_env()
    texts = [
        "A function that adds two integers.",
        "A method that sums two numbers.",
        "How to cook pasta al dente?",
    ]
    _run_case(
        title="NL baseline: paraphrase vs unrelated",
        embedder=embedder,
        texts=texts,
        positives=[(0, 1)],
        negatives=[(0, 2)],
    )


@pytest.mark.skipif(
    not _RUN_INTEGRATION,
    reason="Set MINI_CODE_INDEX_RUN_INTEGRATION=1 to run paid network integration tests",
)
def test_embed_python_short_code_docstring_and_query() -> None:
    embedder = OpenAICompatibleEmbedder.from_env()
    py_code = (
        "def add(a: int, b: int) -> int:\n"
        "    \"\"\"Add two integers and return the sum.\"\"\"\n"
        "    return a + b\n"
    )
    py_summary = "Python function add(a, b) returns a + b. Adds two integers."
    py_query = "Where is the function that adds two integers?"
    unrelated = "How to implement quicksort in Python?"
    _run_case(
        title="Python: code + summary + query (short)",
        embedder=embedder,
        texts=[py_code, py_summary, py_query, unrelated],
        positives=[(0, 1), (0, 2)],
        negatives=[(0, 3)],
    )


@pytest.mark.skipif(
    not _RUN_INTEGRATION,
    reason="Set MINI_CODE_INDEX_RUN_INTEGRATION=1 to run paid network integration tests",
)
def test_embed_python_longer_code_with_comments_and_summary() -> None:
    embedder = OpenAICompatibleEmbedder.from_env()
    py_code = (
        "# Computes cosine similarity between two vectors.\n"
        "# Returns a float in [-1, 1].\n"
        "from math import sqrt\n\n"
        "def cosine(a, b):\n"
        "    \"\"\"Cosine similarity for equal-length vectors.\"\"\"\n"
        "    dot = 0.0\n"
        "    na = 0.0\n"
        "    nb = 0.0\n"
        "    for x, y in zip(a, b):\n"
        "        dot += x * y\n"
        "        na += x * x\n"
        "        nb += y * y\n"
        "    if na == 0.0 or nb == 0.0:\n"
        "        return 0.0\n"
        "    return dot / (sqrt(na) * sqrt(nb))\n"
    )
    summary = (
        "This Python function computes cosine similarity between two numeric vectors. "
        "It accumulates dot product and vector norms, then returns dot/(|a|*|b|). "
        "If either vector is all zeros, it returns 0.0."
    )
    query = "Find the code that computes cosine similarity between vectors."
    negative = "Python code that reads a JSON file from disk and parses it."
    _run_case(
        title="Python: longer code + summary + query",
        embedder=embedder,
        texts=[py_code, summary, query, negative],
        positives=[(0, 1), (0, 2)],
        negatives=[(0, 3)],
    )


@pytest.mark.skipif(
    not _RUN_INTEGRATION,
    reason="Set MINI_CODE_INDEX_RUN_INTEGRATION=1 to run paid network integration tests",
)
def test_embed_java_code_comment_and_query() -> None:
    embedder = OpenAICompatibleEmbedder.from_env()
    java_code = (
        "package com.example;\n\n"
        "/**\n"
        " * Adds two integers.\n"
        " * @return a + b\n"
        " */\n"
        "public class MathUtil {\n"
        "  public static int add(int a, int b) {\n"
        "    return a + b;\n"
        "  }\n"
        "}\n"
    )
    java_summary = "Java utility class MathUtil with static add(a,b) that returns the sum of two integers."
    java_query = "Find the Java method that adds two numbers and returns the sum."
    java_unrelated = "Java method that parses JSON string into an object."
    _run_case(
        title="Java: code + summary + query",
        embedder=embedder,
        texts=[java_code, java_summary, java_query, java_unrelated],
        positives=[(0, 1), (0, 2)],
        negatives=[(0, 3)],
    )


@pytest.mark.skipif(
    not _RUN_INTEGRATION,
    reason="Set MINI_CODE_INDEX_RUN_INTEGRATION=1 to run paid network integration tests",
)
def test_embed_cross_language_queries_against_code() -> None:
    embedder = OpenAICompatibleEmbedder.from_env()
    query_en = "Where is the function/method that adds two integers?"
    query_zh = "查找把两个整数相加并返回结果的函数/方法"
    py_code = "def add(a, b):\n    return a + b\n"
    java_code = "public static int add(int a, int b) { return a + b; }"
    unrelated_code = (
        "def read_json(path):\n"
        "    import json\n"
        "    with open(path) as f:\n"
        "        return json.load(f)\n"
    )

    texts = [query_en, query_zh, py_code, java_code, unrelated_code]
    vecs = embedder.embed(texts)

    print("\n=== Cross-language queries ===")
    print("model=", embedder.model)
    print("base_url=", embedder.base_url)
    print("n_texts=", len(texts), "dim=", len(vecs[0]) if vecs else 0)
    for i, (t, v) in enumerate(zip(texts, vecs)):
        _print_vec_preview(i, t, v)

    sim_qen_py = _cosine(vecs[0], vecs[2])
    sim_qen_un = _cosine(vecs[0], vecs[4])
    sim_qzh_java = _cosine(vecs[1], vecs[3])
    sim_qzh_un = _cosine(vecs[1], vecs[4])
    print("cos(query_en, py_add)=", sim_qen_py)
    print("cos(query_en, unrelated)=", sim_qen_un)
    print("cos(query_zh, java_add)=", sim_qzh_java)
    print("cos(query_zh, unrelated)=", sim_qzh_un)

    assert sim_qen_py > sim_qen_un
    assert sim_qzh_java > sim_qzh_un
