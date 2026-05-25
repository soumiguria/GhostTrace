"""Investigation lifecycle: DB persistence + async workflow execution."""

import asyncio
import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.agent_log import AgentLog
from app.models.investigation import Investigation
from app.workflows.investigation_graph import investigation_graph


class InvestigationService:
    async def create_investigation(self, db: AsyncSession, raw_input: str) -> Investigation:
        inv = Investigation(raw_input=raw_input, status="started")
        db.add(inv)
        await db.flush()
        await self._append_log(db, inv.id, "Orchestrator", "Investigation initiated. Deploying agent swarm.")
        return inv

    async def _append_log(
        self,
        db: AsyncSession,
        investigation_id: str,
        agent_name: str,
        message: str,
    ) -> AgentLog:
        log = AgentLog(
            investigation_id=investigation_id,
            agent_name=agent_name,
            message=message,
        )
        db.add(log)
        await db.flush()
        return log

    async def run_workflow_background(self, investigation_id: str, raw_input: str) -> None:
        """Run LangGraph pipeline in background with fresh DB sessions."""
        from app.database.session import async_session_factory

        async with async_session_factory() as db:
            try:
                inv = await db.get(Investigation, investigation_id)
                if not inv:
                    return
                inv.status = "running"
                await db.commit()

                initial_state = {
                    "investigation_id": investigation_id,
                    "raw_input": raw_input,
                    "logs": [],
                }

                # Step through graph manually to persist logs after each step
                steps = [
                    ("entity_extraction", "Entity Extraction"),
                    ("reputation_analysis", "Reputation Analysis"),
                    ("risk_scoring", "Risk Scoring"),
                    ("report_generation", "Report Generation"),
                ]

                state: dict[str, Any] = dict(initial_state)
                from app.agents.entity_agent import run_entity_extraction
                from app.agents.reputation_agent import run_reputation_analysis
                from app.agents.risk_agent import run_risk_scoring
                from app.agents.report_agent import run_report_generation

                runners = [
                    run_entity_extraction,
                    run_reputation_analysis,
                    run_risk_scoring,
                    run_report_generation,
                ]

                for runner, (step_key, label) in zip(runners, steps):
                    await asyncio.sleep(1.2)  # Stagger steps for live log streaming UX
                    inv = await db.get(Investigation, investigation_id)
                    if inv:
                        inv.status = "running"
                        workflow = self._load_workflow_state(inv)
                        workflow["current_step"] = step_key
                        inv.workflow_state = json.dumps(workflow)
                        await self._append_log(db, investigation_id, "Orchestrator", f"Activating {label} agent...")
                        await db.commit()

                    result = await runner(state)  # type: ignore[arg-type]
                    for log_entry in result.get("logs", []):
                        if log_entry not in state.get("logs", []):
                            await self._append_log(
                                db,
                                investigation_id,
                                log_entry["agent_name"],
                                log_entry["message"],
                            )
                    state.update({k: v for k, v in result.items() if k != "logs"})
                    state.setdefault("logs", []).extend(result.get("logs", []))

                    inv = await db.get(Investigation, investigation_id)
                    if inv:
                        workflow = self._build_workflow_snapshot(state)
                        inv.workflow_state = json.dumps(workflow)
                        if state.get("risk"):
                            inv.risk_score = float(state["risk"].get("risk_score", 0))
                        await db.commit()

                inv = await db.get(Investigation, investigation_id)
                if inv:
                    inv.status = "completed"
                    inv.final_report = state.get("report", "")
                    inv.risk_score = float(state.get("risk", {}).get("risk_score", inv.risk_score or 0))
                    inv.workflow_state = json.dumps(self._build_workflow_snapshot(state))
                    await self._append_log(
                        db,
                        investigation_id,
                        "Orchestrator",
                        "Investigation complete. Intelligence report available.",
                    )
                    await db.commit()
            except Exception as exc:
                await db.rollback()
                async with async_session_factory() as err_db:
                    inv = await err_db.get(Investigation, investigation_id)
                    if inv:
                        inv.status = "failed"
                        await self._append_log(
                            err_db,
                            investigation_id,
                            "Orchestrator",
                            f"Workflow error: {exc}",
                        )
                        await err_db.commit()

    def _load_workflow_state(self, inv: Investigation) -> dict[str, Any]:
        if inv.workflow_state:
            try:
                return json.loads(inv.workflow_state)
            except json.JSONDecodeError:
                pass
        return {}

    def _build_workflow_snapshot(self, state: dict[str, Any]) -> dict[str, Any]:
        return {
            "current_step": state.get("current_step", "pending"),
            "entities": state.get("entities"),
            "reputation": state.get("reputation"),
            "risk": state.get("risk"),
            "findings": {
                "entities": state.get("entities"),
                "reputation": state.get("reputation"),
                "risk": state.get("risk"),
            },
        }

    async def get_investigation(self, db: AsyncSession, investigation_id: str) -> Investigation | None:
        result = await db.execute(
            select(Investigation)
            .where(Investigation.id == investigation_id)
            .options(selectinload(Investigation.logs))
        )
        return result.scalar_one_or_none()

    def schedule_investigation(self, investigation_id: str, raw_input: str) -> None:
        asyncio.create_task(self.run_workflow_background(investigation_id, raw_input))


investigation_service = InvestigationService()
