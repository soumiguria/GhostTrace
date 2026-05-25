"""Investigation ORM model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    raw_input: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    final_report: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    workflow_state: Mapped[str | None] = mapped_column(Text, nullable=True)

    logs: Mapped[list["AgentLog"]] = relationship(
        "AgentLog",
        back_populates="investigation",
        cascade="all, delete-orphan",
        order_by="AgentLog.timestamp",
    )


from app.models.agent_log import AgentLog  # noqa: E402
