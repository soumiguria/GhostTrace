"""Agent log ORM model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id: Mapped[str] = mapped_column(String(36), ForeignKey("investigations.id"))
    agent_name: Mapped[str] = mapped_column(String(64), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    investigation: Mapped["Investigation"] = relationship("Investigation", back_populates="logs")


from app.models.investigation import Investigation  # noqa: E402
