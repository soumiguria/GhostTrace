# GhostTrace GitAgent Definition

This directory is a **[GitAgent](https://github.com/open-gitagent/gitagent)**-compliant agent repository — the **version-controlled source of truth** for GhostTrace's investigation swarm.

| File | Purpose |
|------|---------|
| `agent.yaml` | Orchestrator manifest (skills, sub-agents, model) |
| `SOUL.md` | Orchestrator identity |
| `RULES.md` | Safety and output constraints |
| `DUTIES.md` | Segregation of duties across agents |
| `skills/` | Investigation skills (Agent Skills standard `SKILL.md`) |
| `agents/` | Sub-agent definitions (entity, reputation, risk, report) |
| `tools/` | HTTP tools for FastAPI integration |
| `workflows/` | Investigation pipeline documentation |

## Validate

```bash
npx @open-gitagent/gitagent@latest validate --dir ./gitagent
```

## Run with GitAgent CLI

```bash
export OPENAI_API_KEY=sk-...   # or use Gemini/Groq via provider config
npx @open-gitagent/gitagent@latest --dir ./gitagent "Investigate: [paste suspicious text]"
```

## Runtime Integration

The **FastAPI backend** loads prompts from `skills/*/SKILL.md` automatically (see `backend/app/utils/gitagent_loader.py`). LangGraph executes the same workflow defined here.

**Product UI:** `frontend/` + `backend/` — live logs, threat meter, intelligence report.
