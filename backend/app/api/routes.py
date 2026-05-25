"""FastAPI route handlers."""

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.investigation import (
    HealthResponse,
    InvestigateRequest,
    InvestigateResponse,
    InvestigationDetail,
    AgentLogSchema,
)
from app.services.investigation_service import investigation_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="ghosttrace-api")


@router.post("/investigate", response_model=InvestigateResponse)
async def investigate(
    body: InvestigateRequest,
    db: AsyncSession = Depends(get_db),
) -> InvestigateResponse:
    inv = await investigation_service.create_investigation(db, body.input)
    investigation_service.schedule_investigation(inv.id, body.input)
    return InvestigateResponse(investigation_id=inv.id, status="started")


@router.get("/investigation/{investigation_id}", response_model=InvestigationDetail)
async def get_investigation(
    investigation_id: str,
    db: AsyncSession = Depends(get_db),
) -> InvestigationDetail:
    inv = await investigation_service.get_investigation(db, investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    workflow_state: dict[str, Any] | None = None
    findings: dict[str, Any] | None = None
    if inv.workflow_state:
        try:
            workflow_state = json.loads(inv.workflow_state)
            findings = workflow_state.get("findings") or {
                "entities": workflow_state.get("entities"),
                "reputation": workflow_state.get("reputation"),
                "risk": workflow_state.get("risk"),
            }
        except json.JSONDecodeError:
            workflow_state = None

    return InvestigationDetail(
        investigation_id=inv.id,
        status=inv.status,
        raw_input=inv.raw_input,
        created_at=inv.created_at,
        workflow_state=workflow_state,
        logs=[AgentLogSchema.model_validate(log) for log in inv.logs],
        risk_score=inv.risk_score,
        findings=findings,
        final_report=inv.final_report,
    )
