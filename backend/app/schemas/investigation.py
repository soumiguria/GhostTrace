"""Pydantic schemas for investigation API."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class InvestigateRequest(BaseModel):
    input: str = Field(..., min_length=1, max_length=50000)


class InvestigateResponse(BaseModel):
    investigation_id: str
    status: str


class AgentLogSchema(BaseModel):
    id: str
    agent_name: str
    message: str
    timestamp: datetime

    model_config = {"from_attributes": True}


class InvestigationDetail(BaseModel):
    investigation_id: str
    status: str
    raw_input: str
    created_at: datetime
    workflow_state: dict[str, Any] | None = None
    logs: list[AgentLogSchema] = []
    risk_score: float | None = None
    findings: dict[str, Any] | None = None
    final_report: str | None = None

    model_config = {"from_attributes": True}


class HealthResponse(BaseModel):
    status: str
    service: str
