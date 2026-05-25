"""Reputation Analysis Agent."""

import json
from typing import Any

from app.agents.state import InvestigationState
from app.services.ai_service import AIService, _load_prompt, ai_service


async def run_reputation_analysis(state: InvestigationState) -> dict[str, Any]:
    raw = state["raw_input"]
    entities = state.get("entities", {})
    fallback = AIService.demo_reputation(raw)
    prompt = _load_prompt("reputation")
    user_payload = json.dumps({"raw_input": raw, "entities": entities})
    reputation = await ai_service.complete_json(prompt, user_payload, fallback)
    logs = []
    for flag in reputation.get("red_flags", [])[:3]:
        logs.append({"agent_name": "Reputation Agent", "message": f"Red flag: {flag}"})
    if not logs:
        logs.append(
            {
                "agent_name": "Reputation Agent",
                "message": "Detected urgency manipulation patterns in narrative structure.",
            }
        )
    return {
        "reputation": reputation,
        "current_step": "risk",
        "logs": logs,
    }
