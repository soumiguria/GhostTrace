"""Risk Scoring Agent."""

import json
from typing import Any

from app.agents.state import InvestigationState
from app.services.ai_service import AIService, _load_prompt, ai_service


async def run_risk_scoring(state: InvestigationState) -> dict[str, Any]:
    reputation = state.get("reputation", {})
    entities = state.get("entities", {})
    fallback = AIService.demo_risk(reputation)
    prompt = _load_prompt("risk_scoring")
    user_payload = json.dumps({"entities": entities, "reputation": reputation})
    risk = await ai_service.complete_json(prompt, user_payload, fallback)
    score = int(risk.get("risk_score", 50))
    return {
        "risk": risk,
        "current_step": "report",
        "logs": [
            {
                "agent_name": "Risk Agent",
                "message": f"Threat score elevated to {score}. Classification: {risk.get('classification', 'Unknown')}.",
            }
        ],
    }
