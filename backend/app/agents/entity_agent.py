"""Entity Extraction Agent — regex + LLM refinement."""

import json
from typing import Any

from app.agents.state import InvestigationState
from app.services.ai_service import AIService, _load_prompt, ai_service
from app.utils.entity_regex import extract_entities_regex


async def run_entity_extraction(state: InvestigationState) -> dict[str, Any]:
    raw = state["raw_input"]
    regex_entities = extract_entities_regex(raw)
    fallback = AIService.demo_entity_enhancement(dict(regex_entities), raw)
    prompt = _load_prompt("entity_extraction")
    user_payload = json.dumps({"raw_input": raw, "regex_entities": regex_entities})
    entities = await ai_service.complete_json(prompt, user_payload, fallback)
    for key in ("emails", "usernames", "urls", "domains", "phone_numbers", "wallet_addresses"):
        entities.setdefault(key, regex_entities.get(key, []))
    log_msgs = []
    if entities.get("domains"):
        log_msgs.append(f"Found {len(entities['domains'])} domain(s) for reputation cross-check.")
    if entities.get("emails"):
        log_msgs.append(f"Extracted {len(entities['emails'])} email address(es).")
    if entities.get("urls"):
        log_msgs.append("Suspicious URL pattern identified in payload.")
    if not log_msgs:
        log_msgs.append("Entity scan complete — minimal structured indicators.")
    return {
        "entities": entities,
        "current_step": "reputation",
        "logs": [{"agent_name": "Entity Agent", "message": m} for m in log_msgs],
    }
