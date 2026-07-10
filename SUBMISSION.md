# GitAgent (Soumi Guria)

**Email:** guriasoumi29@gmail.com  
**GitHub:** https://github.com/soumiguria/GhostTrace  

---

## Form Answers

### Project Title

**GhostTrace AI — Git-Native Autonomous Cyber Investigation Lab**

### What did you build?

> **GhostTrace AI** is a multi-agent investigation platform (not a chatbot). Users submit suspicious text, URLs, or emails. A **GitAgent-defined agent swarm** runs: Entity Extraction → Reputation Analysis → Risk Scoring → Report Generation.
>
> **GitAgent (`/gitagent`):** `agent.yaml`, `SOUL.md`, `RULES.md`, `DUTIES.md`, four `skills/*/SKILL.md`, four sub-agents under `agents/`, HTTP `tools/`, and `workflows/investigation.md`. Prompts are version-controlled in the repo; FastAPI loads them at runtime.
>
> **Product layer:** FastAPI + LangGraph orchestration, SQLite logs, Next.js 14 dashboard with live agent console, threat meter, entity panel, and markdown intelligence report. Works without paid API keys via `DEMO_MODE`.

### Explain your project in simple words.

> Paste something sketchy — a fake job message, phishing email, or scam link. GhostTrace sends it through four specialist AI agents like a mini detective team: one pulls out emails and links, one spots scam patterns, one gives a danger score, and one writes a report. You watch **live logs** and a **risk meter** update on screen, like a cyber investigation control room.

### Why did you choose this idea?

> The challenge evaluates **agent workflow design** and **GitAgent usage**. Cyber investigation naturally splits into extract → analyze → score → report — perfect for GitAgent skills + sub-agents with segregation of duties. It demos well in 3–5 minutes (streaming logs, animated UI) and ships fast with `DEMO_MODE` so judges need no OpenAI key.

### GitHub Repository Link

https://github.com/soumiguria/GhostTrace

**Suggested 3–5 min script:**
1. Show `gitagent/` folder (agent.yaml, SOUL.md, skills) — "repo is the agent"
2. `npx @open-gitagent/gitagent@latest validate --dir ./gitagent`
3. Live UI demo: demo payload → Investigate → logs + threat meter + report
4. Architecture: GitAgent skills → FastAPI/LangGraph → polling UI

### What would you improve if given 1 more week?

> 1. Full **gitclaw** CLI path as first-class runner alongside FastAPI  
> 2. **Gemini / Groq / Ollama** provider switch (free tiers)  
> 3. WebSocket log streaming  
> 4. Investigation history + PDF/markdown export  
> 5. Optional domain reputation API behind a "deep scan" toggle  

---

## Architecture (for video / reviewers)

```
User Input
    ↓
GitAgent skills (gitagent/skills/*.md)  ← single source of truth
    ↓
FastAPI POST /investigate → LangGraph pipeline
    ↓
SQLite (investigations + agent_logs)
    ↓
Next.js polls GET /investigation/{id} → live dashboard
```

**Thought process:** Separate *agent definition* (GitAgent files in git) from *runtime* (FastAPI/LangGraph) and *presentation* (Next.js). Optimize for judge experience: visible workflow, honest MVP scope, runnable without API billing.
