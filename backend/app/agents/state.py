"""LangGraph investigation state."""

from typing import Any, TypedDict


class InvestigationState(TypedDict, total=False):
    investigation_id: str
    raw_input: str
    entities: dict[str, Any]
    reputation: dict[str, Any]
    risk: dict[str, Any]
    report: str
    current_step: str
    logs: list[dict[str, str]]
