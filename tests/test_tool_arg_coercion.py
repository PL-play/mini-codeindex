import asyncio

from mini_code_index.retrieval.util.llm_tooling import execute_tool_safely, tool_spec_from


async def _typed_tool(max_depth: int = 4, include_files: bool = True, score: float = 1.0):
    # Return types so the test can assert coercion.
    return {
        "max_depth": max_depth,
        "max_depth_type": type(max_depth).__name__,
        "include_files": include_files,
        "include_files_type": type(include_files).__name__,
        "score": score,
        "score_type": type(score).__name__,
    }


def test_execute_tool_safely_coerces_basic_types():
    spec = tool_spec_from(_typed_tool)

    # Simulate LLM-provided JSON where scalars come through as strings.
    args = {"max_depth": "3", "include_files": "false", "score": "1.5"}

    result = asyncio.run(execute_tool_safely(spec, args))
    assert isinstance(result, dict)
    assert "error" not in result

    assert result["max_depth"] == 3
    assert result["max_depth_type"] == "int"

    assert result["include_files"] is False
    assert result["include_files_type"] == "bool"

    assert abs(result["score"] - 1.5) < 1e-9
    assert result["score_type"] == "float"
