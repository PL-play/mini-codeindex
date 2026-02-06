"""Retrieval agent state definitions and structured output models."""

from __future__ import annotations

import operator
from typing import Annotated, List, Optional, Dict, Any

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from typing_extensions import Required, TypedDict

class RetrievalAgentState(TypedDict, total=False):
    """State for the retrieval agent workflow.

    Fields are intentionally broad to support different query types.
    """

    root_dir: Required[str]
    query: Required[str]
    plan: Dict[str, Any]
    sub_tasks: List[Dict[str, Any]]
    sub_results: List[Dict[str, Any]]
    answer: str
    needs_more: bool
    iteration: int
    max_iterations: int
    notes: str

class RetrievalPlan(BaseModel):
    """High-level plan guiding the overall retrieval workflow."""

    objective: str = Field(description="Core goal of the retrieval task")
    focus: str = Field(description="Key aspects or scope boundaries to emphasize")
    success_criteria: str = Field(description="What a good answer should cover")
    sub_tasks: List["SubTask"] = Field(description="List of sub-questions/tasks to run")


class SubTask(BaseModel):
    """Single retrieval subtask descriptor."""

    title: str = Field(description="Short title for the subtask")
    query: str = Field(description="Focused query for this subtask")


class EvidenceItem(BaseModel):
    """Normalized evidence item from retrieval tools."""

    path: str = Field(description="File path containing the evidence")
    snippet: str = Field(description="Relevant code or text snippet")
    start_line: Optional[int] = Field(default=None, description="Start line in file")
    end_line: Optional[int] = Field(default=None, description="End line in file")
    note: Optional[str] = Field(default=None, description="Why this evidence is relevant")


class SubtaskResult(BaseModel):
    """Structured output for one subtask."""

    summary: str = Field(description="Concise summary for this subtask")
    evidence: List[EvidenceItem] = Field(description="Supporting evidence list")


class FinalAnswer(BaseModel):
    """Structured final answer for the user."""

    answer: str = Field(description="Final response to the user")
    evidence: List[EvidenceItem] = Field(description="Key evidence items")
    followups: List[str] = Field(description="Suggested next questions or explorations")


class Clarification(BaseModel):
    """Clarification decision for ambiguous queries."""

    need_clarification: bool = Field(description="Whether clarification is required")
    question: str = Field(description="Clarifying question to ask the user")
    verification: str = Field(description="Confirmation message if no clarification")


class RetrievalComplete(BaseModel):
    """Tool-style marker indicating retrieval is complete."""

    pass


class AgentState(TypedDict):
    """Main agent state across the retrieval workflow."""

    messages: Annotated[list[BaseMessage], operator.add]
    root_dir: str
    query: str
    plan: Optional[RetrievalPlan]
    sub_tasks: List[SubTask]
    sub_results: Annotated[list[SubtaskResult], operator.add]
    notes: Annotated[list[str], operator.add]
    final_answer: Optional[FinalAnswer]
    clarification_response: Optional[Clarification]


class PlannerState(TypedDict):
    """Planner state for strategy and task decomposition."""

    messages: Annotated[list[BaseMessage], operator.add]
    query: str
    plan: Optional[RetrievalPlan]
    sub_tasks: List[SubTask]
    notes: Annotated[list[str], operator.add]


class SubtaskState(TypedDict):
    """Subtask graph state for retrieval/synthesis/verification."""

    messages: Annotated[list[BaseMessage], operator.add]
    sub_task: SubTask
    evidence: Annotated[list[EvidenceItem], operator.add]
    result: Optional[SubtaskResult]
    needs_more: bool
    iteration: int
    max_iterations: int
    notes: Annotated[list[str], operator.add]


class SummarizeState(TypedDict):
    """Summarize state to merge subtask outputs into a final answer."""

    messages: Annotated[list[BaseMessage], operator.add]
    sub_results: List[SubtaskResult]
    final_answer: Optional[FinalAnswer]
    notes: Annotated[list[str], operator.add]
