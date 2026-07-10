# GhostTrace AI

**Autonomous multi-agent cyber investigation platform** — analyze suspicious text, URLs, emails, and domains with a **[GitAgent](https://github.com/open-gitagent/gitagent)**-defined agent swarm, LangGraph orchestration, and a live investigation dashboard.

![Stack](https://img.shields.io/badge/GitAgent-Repo--Native-22d3ee) ![Stack](https://img.shields.io/badge/Next.js-14-black) ![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688) ![LangGraph](https://img.shields.io/badge/LangGraph-Agents-7C3AED)

## Demo Experience

1. Paste suspicious content (or click **Load demo payload**)
2. Click **Investigate**
3. Watch agents stream logs in real time
4. Risk meter, entity panel, and timeline update live
5. Final markdown intelligence report appears

## Architecture

```
gitagent/ (SOUL, RULES, skills, sub-agents)  ← version-controlled agent definition
        ↓
Input → Entity Extraction → Reputation Analysis → Risk Scoring → Report Generation
        ↓
FastAPI + LangGraph + SQLite logs
        ↓
Next.js dashboard (live polling)
```

| Layer | Tech |
|-------|------|
| **GitAgent** | `gitagent/` — agent.yaml, SOUL.md, RULES.md, skills/, agents/, tools/ |
| Frontend | Next.js 14, TypeScript, Tailwind, Framer Motion |
| Backend | FastAPI, SQLAlchemy, SQLite (async) |
| Runtime | LangGraph pipeline; prompts loaded from GitAgent `SKILL.md` files |
| Live updates | HTTP polling (800ms) |

### GitAgent validate & CLI

```bash
npx @open-gitagent/gitagent@latest validate --dir ./gitagent

# Optional CLI investigation (requires LLM API key)
npx @open-gitagent/gitagent@latest --dir ./gitagent "Investigate this phishing email: ..."
```

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- OpenAI API key (optional — `DEMO_MODE=true` works without it)

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env — set OPENAI_API_KEY or keep DEMO_MODE=true

# From backend/ directory:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/investigate` | Start investigation `{ "input": "..." }` |
| `GET` | `/investigation/{id}` | Status, logs, findings, report |

## Project Structure

```
GhostTrace/
├── gitagent/                # GitAgent standard (agent.yaml, SOUL.md, skills/, agents/)
├── backend/
│   ├── app/
│   │   ├── agents/          # LangGraph agent runners
│   │   ├── workflows/       # LangGraph graph
│   │   ├── services/        # AI + investigation (loads gitagent skills)
│   │   └── utils/gitagent_loader.py
│   └── requirements.txt
├── frontend/
│   └── src/components/      # ThreatMeter, LiveAgentConsole, etc.
└── SUBMISSION.md            
```

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI key for LLM agents |
| `OPENAI_MODEL` | Default: `gpt-4o-mini` |
| `DATABASE_URL` | Default: `sqlite+aiosqlite:///./ghosttrace.db` |
| `CORS_ORIGINS` | Default: `http://localhost:3000` |
| `DEMO_MODE` | `true` = heuristic analysis without API |

### Frontend (`frontend/.env.local`)

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Default: `http://localhost:8000` |

## Agents

1. **Entity Agent** — regex extraction + LLM refinement (emails, URLs, domains, wallets)
2. **Reputation Agent** — scam/phishing/urgency pattern analysis
3. **Risk Agent** — threat score 0–100, confidence, classification
4. **Report Agent** — executive markdown intelligence report

Logs persist to SQLite after each step for live polling.
