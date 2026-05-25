"""Report Generator Agent."""

import json
from typing import Any

from app.agents.state import InvestigationState
from app.services.ai_service import AIService, _load_prompt, ai_service


async def run_report_generation(state: InvestigationState) -> dict[str, Any]:
    raw = state["raw_input"]
    entities = state.get("entities", {})
    reputation = state.get("reputation", {})
    risk = state.get("risk", {})
    fallback = AIService.demo_report(raw, entities, reputation, risk)
    prompt = _load_prompt("report_generator")
    user_payload = json.dumps(
        {"raw_input": raw, "entities": entities, "reputation": reputation, "risk": risk}
    )
    report = await ai_service.complete_markdown(prompt, user_payload, fallback)
    return {
        "report": report,
        "current_step": "completed",
        "logs": [
            {
                "agent_name": "Report Agent",
                "message": "Intelligence report compiled and ready for analyst review.",
            }
        ],
    }
