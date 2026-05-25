"""LangGraph orchestration for multi-agent investigation pipeline."""

from typing import Any

from langgraph.graph import END, StateGraph

from app.agents.entity_agent import run_entity_extraction
from app.agents.report_agent import run_report_generation
from app.agents.reputation_agent import run_reputation_analysis
from app.agents.risk_agent import run_risk_scoring
from app.agents.state import InvestigationState


def _merge_logs(state: InvestigationState, update: dict[str, Any]) -> list[dict[str, str]]:
    existing = list(state.get("logs", []))
    existing.extend(update.get("logs", []))
    return existing


async def _entity_node(state: InvestigationState) -> dict[str, Any]:
    result = await run_entity_extraction(state)
    result["logs"] = _merge_logs(state, result)
    return result


async def _reputation_node(state: InvestigationState) -> dict[str, Any]:
    result = await run_reputation_analysis(state)
    result["logs"] = _merge_logs(state, result)
    return result


async def _risk_node(state: InvestigationState) -> dict[str, Any]:
    result = await run_risk_scoring(state)
    result["logs"] = _merge_logs(state, result)
    return result


async def _report_node(state: InvestigationState) -> dict[str, Any]:
    result = await run_report_generation(state)
    result["logs"] = _merge_logs(state, result)
    return result


def build_investigation_graph():
    """Input → Entity → Reputation → Risk → Report → END"""
    graph = StateGraph(InvestigationState)
    graph.add_node("entity_extraction", _entity_node)
    graph.add_node("reputation_analysis", _reputation_node)
    graph.add_node("risk_scoring", _risk_node)
    graph.add_node("report_generation", _report_node)

    graph.set_entry_point("entity_extraction")
    graph.add_edge("entity_extraction", "reputation_analysis")
    graph.add_edge("reputation_analysis", "risk_scoring")
    graph.add_edge("risk_scoring", "report_generation")
    graph.add_edge("report_generation", END)

    return graph.compile()


investigation_graph = build_investigation_graph()
