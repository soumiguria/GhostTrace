"""Reusable OpenAI service layer with demo fallback."""

import json
import re
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

from app.config.settings import get_settings

PROMPTS_DIR = Path(__file__).parent / "prompts"


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")


class AIService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client: AsyncOpenAI | None = None
        if self.settings.openai_api_key:
            self._client = AsyncOpenAI(api_key=self.settings.openai_api_key)

    async def complete_json(
        self,
        system_prompt: str,
        user_content: str,
        fallback: dict[str, Any],
    ) -> dict[str, Any]:
        if self.settings.use_demo_fallback or not self._client:
            return fallback
        try:
            response = await self._client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or "{}"
            return json.loads(content)
        except Exception:
            return fallback

    async def complete_markdown(
        self,
        system_prompt: str,
        user_content: str,
        fallback: str,
    ) -> str:
        if self.settings.use_demo_fallback or not self._client:
            return fallback
        try:
            response = await self._client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=0.4,
            )
            return response.choices[0].message.content or fallback
        except Exception:
            return fallback

    @staticmethod
    def demo_entity_enhancement(entities: dict[str, Any], raw: str) -> dict[str, Any]:
        notes = []
        if entities.get("urls"):
            notes.append(f"Flagged {len(entities['urls'])} URL(s) for domain reputation check.")
        if entities.get("wallet_addresses"):
            notes.append("Cryptocurrency wallet reference detected.")
        if "@" in raw and not entities.get("emails"):
            notes.append("Possible obfuscated email pattern.")
        entities["notes"] = notes or ["No high-confidence entities beyond regex scan."]
        return entities

    @staticmethod
    def demo_reputation(raw: str) -> dict[str, Any]:
        lower = raw.lower()
        red_flags = []
        if any(w in lower for w in ("urgent", "immediately", "act now", "limited time")):
            red_flags.append("Artificial urgency language detected")
        if any(w in lower for w in ("verify", "confirm account", "suspended", "click here")):
            red_flags.append("Account verification / credential harvesting pattern")
        if any(w in lower for w in ("bitcoin", "crypto", "wallet", "investment", "guaranteed")):
            red_flags.append("Financial / crypto scam lexicon present")
        if any(w in lower for w in ("ceo", "hr", "payroll", "invoice", "wire transfer")):
            red_flags.append("Business email compromise (BEC) indicators")
        if not red_flags:
            red_flags.append("Generic unsolicited outreach pattern")
        return {
            "reputation_notes": ["Heuristic reputation scan completed (demo mode)."],
            "trust_signals": ["No verified sender identity in submitted content"],
            "red_flags": red_flags,
            "behavioral_analysis": (
                "The message exhibits pressure tactics and unsolicited contact patterns "
                "commonly associated with social engineering campaigns."
            ),
        }

    @staticmethod
    def demo_risk(reputation: dict[str, Any]) -> dict[str, Any]:
        score = min(95, 35 + len(reputation.get("red_flags", [])) * 12)
        return {
            "risk_score": score,
            "confidence": min(95, score + 5),
            "scam_likelihood": round(score / 100, 2),
            "classification": "Likely phishing attempt" if score >= 60 else "Suspicious - manual review advised",
            "reasoning": (
                f"Elevated risk driven by {len(reputation.get('red_flags', []))} active threat indicators "
                "and absence of trust signals."
            ),
        }

    @staticmethod
    def demo_report(
        raw: str,
        entities: dict[str, Any],
        reputation: dict[str, Any],
        risk: dict[str, Any],
    ) -> str:
        flags = "\n".join(f"- {f}" for f in reputation.get("red_flags", []))
        ents = json.dumps({k: v for k, v in entities.items() if k != "notes"}, indent=2)
        return f"""## Executive Summary

GhostTrace AI completed an autonomous multi-agent investigation. **Classification:** {risk.get('classification')}. **Risk Score:** {risk.get('risk_score')}/100.

## Extracted Entities

```json
{ents}
```

## Behavioral Analysis

{reputation.get('behavioral_analysis', 'N/A')}

## Threat Indicators

{flags}

## Risk Assessment

- **Score:** {risk.get('risk_score')}/100
- **Confidence:** {risk.get('confidence')}%
- **Scam Likelihood:** {risk.get('scam_likelihood', 0)}

{risk.get('reasoning', '')}

## Recommended Actions

1. Do not click links or open attachments from this source.
2. Verify sender identity through an independent channel.
3. Report to your security team and block associated domains.
4. If credentials were shared, initiate password rotation immediately.

---
*Investigation input (truncated):* `{raw[:200]}{'...' if len(raw) > 200 else ''}`
"""


ai_service = AIService()
