# Investigation Workflow

**Trigger:** User submits suspicious text, URL, email, or domain via UI or CLI.

## Steps

1. **entity-extraction** — Regex scan + LLM refinement → structured entities
2. **reputation-analysis** — Scam/phishing/urgency/impersonation patterns
3. **risk-scoring** — threat score 0–100, confidence, classification
4. **report-generation** — Markdown intelligence report

## Persistence

Each step appends to `AgentLog` with `agent_name` and `message` for live dashboard polling.

## Completion Criteria

- `status`: completed
- `final_report`: non-empty markdown
- `risk_score`: set
