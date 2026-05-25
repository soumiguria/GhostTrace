# GhostTrace — Framework-Agnostic Agent Instructions

When run via **gitagent** / **gitclaw** CLI:

1. Read `agent.yaml` for skill and sub-agent registry
2. Load `SOUL.md` for orchestrator identity
3. Enforce `RULES.md` on all outputs
4. For investigation tasks, execute skills in order listed in `workflows/investigation.md`

When run via **GhostTrace FastAPI** (production MVP):

- LangGraph executes the same pipeline defined in this repo
- Prompts load from `skills/*/SKILL.md` (single source of truth)
- Results persist to SQLite; frontend polls for live logs

## Sub-Agents

See `agents/` for per-role `agent.yaml` + `SOUL.md` definitions.

## Validate

```bash
npx @open-gitagent/gitagent@latest validate --dir ./gitagent
```

## Run (CLI investigation)

```bash
# From repo root — requires OPENAI_API_KEY or compatible provider
npx @open-gitagent/gitagent@latest --dir ./gitagent "Investigate this payload: [paste suspicious text]"
```
