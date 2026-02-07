import asyncio
import json
import os
from datetime import datetime
from typing import Any, Annotated, Dict, List, Literal

from langchain_core.tools import BaseTool, tool, InjectedToolArg
import logging
import dotenv
from tavily import AsyncTavilyClient

from mini_code_index.retrieval.prompts import summarize_webpage_prompt
from mini_code_index.retrieval.util.interface import LLMRequest, LLMService

dotenv.load_dotenv()

TAVILY_SEARCH_API_KEY = os.getenv("TAVILY_SEARCH_API_KEY")

def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

async def execute_tool_safely(tool: BaseTool, args: dict) -> Any:
    """安全地执行工具，并处理潜在的异常"""
    try:
        return await tool.ainvoke(args)
    except Exception as e:
        # 捕获任何在工具执行期间发生的错误
        logging.warning(f"工具 '{tool.name}' 执行失败: {e}")
        return f"工具执行错误: {e}"

##########################
# Tavily Search Tool Utils
##########################
TAVILY_SEARCH_DESCRIPTION = (
    "A search engine optimized for comprehensive, accurate, and trusted results. "
    "Useful for when you need to answer questions about current events."
)


async def tavily_search_results(
    queries: List[str],
    *,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
) -> List[Dict[str, str]]:
    """Run Tavily search and return results.

    The returned list contains objects with:
    - title
    - url
    - content
    """
    if not TAVILY_SEARCH_API_KEY or not TAVILY_SEARCH_API_KEY.strip():
        raise RuntimeError("Missing required environment variable: TAVILY_SEARCH_API_KEY")

    search_results = await tavily_search_async(
        queries,
        max_results=max_results,
        topic=topic,
        include_raw_content=False,
    )

    seen_urls: set[str] = set()
    items: List[Dict[str, str]] = []

    for response in search_results:
        for result in response.get("results", []) or []:
            url = str(result.get("url") or "").strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            items.append(
                {
                    "title": str(result.get("title") or "").strip(),
                    "url": url,
                    "content": str(result.get("content") or "").strip(),
                }
            )

    return items


def _format_search_results(items: List[Dict[str, str]]) -> str:
    if not isinstance(items, list) or not items:
        return "No valid search results found. Please try different search queries."

    out = "Search results:\n\n"
    for i, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "").strip()
        url = str(item.get("url") or "").strip()
        content = str(item.get("content") or "").strip()
        out += f"--- SOURCE {i}: {title} ---\n"
        out += f"URL: {url}\n\n"
        out += f"CONTENT:\n{content}\n\n"
        out += "-" * 20 + "\n\n"
    return out.strip()

@tool(description=TAVILY_SEARCH_DESCRIPTION)
async def tavily_search(
        queries: List[str],
        max_results: Annotated[int, InjectedToolArg] = 5,
        topic: Annotated[Literal["general", "news", "finance"], InjectedToolArg] = "general",
) -> str:
    """
    Fetch and summarize search results from Tavily search API.

    Args:
        queries: List of search queries to execute
        max_results: Maximum number of results to return per query
        topic: Topic filter for search results (general, news, or finance)

    Returns:
        Formatted string containing summarized search results
    """
    logger = logging.getLogger(__name__)
    logger.info(f"🔍 [TAVILY_SEARCH] 开始搜索，查询数量: {len(queries)}")

    results = await tavily_search_results(
        queries,
        max_results=max_results,
        topic=topic,
    )
    return _format_search_results(results)

async def summarize_webpage(llm_client: LLMService, webpage_content: str) -> str:
    """Summarize webpage content using the project's LLM client with timeout protection.

    Args:
        llm_client: An LLM client implementing `LLMService`
        webpage_content: Raw webpage content to be summarized

    Returns:
        Formatted summary with key excerpts, or original content if summarization fails
    """
    try:
        # Create prompt with current date context
        prompt_content = summarize_webpage_prompt.format(
            webpage_content=webpage_content,
            date=get_today_str()
        )

        req = LLMRequest.from_prompt(
            prompt=prompt_content,
            parse_json=True,
            temperature=0.0,
            max_tokens=2000,
        )

        # Execute summarization with timeout to prevent hanging
        resp = await asyncio.wait_for(
            llm_client.complete(req),
            timeout=60.0,
        )

        if resp.parse_error or not resp.json_data:
            logging.warning(f"Summarization JSON parse failed: {resp.parse_error}")
            return webpage_content

        data: Dict[str, Any] = dict(resp.json_data)
        summary_text = str(data.get("summary") or "").strip()
        key_excerpts_obj: Any = data.get("key_excerpts")

        excerpts: List[str] = []
        if isinstance(key_excerpts_obj, list):
            excerpts = [str(x).strip() for x in key_excerpts_obj if str(x).strip()]
        elif isinstance(key_excerpts_obj, str):
            # Allow the prompt's comma-separated format.
            excerpts = [s.strip() for s in key_excerpts_obj.split(",") if s.strip()]

        if not summary_text:
            summary_text = (resp.content_text or resp.raw_text or "").strip()

        excerpts = excerpts[:5]
        excerpt_block = "\n".join(f"- {e}" for e in excerpts) if excerpts else ""

        formatted_summary = f"<summary>\n{summary_text}\n</summary>"
        if excerpt_block:
            formatted_summary += f"\n\n<key_excerpts>\n{excerpt_block}\n</key_excerpts>"

        return formatted_summary

    except asyncio.TimeoutError:
        # Timeout during summarization - return original content
        logging.warning("Summarization timed out after 60 seconds, returning original content")
        return webpage_content
    except Exception as e:
        # Other errors during summarization - log and return original content
        logging.warning(f"Summarization failed with error: {str(e)}, returning original content")
        return webpage_content

async def tavily_search_async(
        search_queries,
        max_results: int = 5,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = True,
):
    """Execute multiple Tavily search queries asynchronously.

    Args:
        search_queries: List of search query strings to execute
        max_results: Maximum number of results per query
        topic: Topic category for filtering results, "general", "news", "finance"
        include_raw_content: Whether to include full webpage content

    Returns:
        List of search result dictionaries from Tavily API
    """
    # Initialize the Tavily client with API key from config
    tavily_client = AsyncTavilyClient(api_key=TAVILY_SEARCH_API_KEY)

    # Create search tasks for parallel execution
    search_tasks = [
        tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic
        )
        for query in search_queries
    ]

    # Execute all search queries in parallel and return results
    search_results = await asyncio.gather(*search_tasks)
    return search_results

@tool(description="Strategic reflection tool for research planning")
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"


def get_today_str() -> str:
    """获取格式化为字符串的当前日期"""
    return datetime.now().strftime("%Y-%m-%d")