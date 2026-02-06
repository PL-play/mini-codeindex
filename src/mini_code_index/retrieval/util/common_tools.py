from datetime import datetime

from langchain_core.tools import BaseTool, tool
import logging
import dotenv

dotenv.load_dotenv()


async def execute_tool_safely(tool: BaseTool, args: dict) -> any:
    """安全地执行工具，并处理潜在的异常"""
    try:
        return await tool.ainvoke(args)
    except Exception as e:
        # 捕获任何在工具执行期间发生的错误
        logging.warning(f"工具 '{tool.name}' 执行失败: {e}")
        return f"工具执行错误: {e}"


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
    return datetime.now().strftime("%Y年%m月%d日")