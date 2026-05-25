# GhostTrace AI

**Autonomous multi-agent cyber investigation platform** — analyze suspicious text, URLs, emails, and domains with a LangGraph-orchestrated agent swarm and receive structured threat intelligence reports.

![Stack](https://img.shields.io/badge/Next.js-14-black) ![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688) ![LangGraph](https://img.shields.io/badge/LangGraph-Agents-7C3AED)

## Demo Experience

1. Paste suspicious content (or click **Load demo payload**)
2. Click **Investigate**
3. Watch agents stream logs in real time
4. Risk meter, entity panel, and timeline update live
5. Final markdown intelligence report appears

## Architecture

```
Input → Entity Extraction → Reputation Analysis → Risk Scoring → Report Generation
         (regex + LLM)        (scam patterns)      (0-100 score)    (markdown)
```

| Layer | Tech |
|-------|------|
| Frontend | Next.js 14, TypeScript, Tailwind, Framer Motion |
| Backend | FastAPI, SQLAlchemy, SQLite (async) |
| Agents | LangGraph pipeline + OpenAI (demo fallback without API key) |
| Live updates | HTTP polling (800ms) |

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
ghosttrace/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/routes.py
│   │   ├── agents/          # Entity, Reputation, Risk, Report
│   │   ├── workflows/       # LangGraph graph
│   │   ├── services/        # AI + investigation lifecycle
│   │   ├── models/          # Investigation, AgentLog
│   │   └── database/
│   └── requirements.txt
└── frontend/
    └── src/
        ├── app/page.tsx
        ├── components/      # ThreatMeter, Console, Report, etc.
        └── hooks/           # Polling hook
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

## License

MIT — built as an MVP demo project.
