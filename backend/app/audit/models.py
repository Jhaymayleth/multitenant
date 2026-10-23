"""Modelos ORM de auditoría global y por tenant.

Basado en docs/07-MODELO-DATOS.md (Sección 2.11).
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class AuditLog(Base):
    __tablename__ = "audit_log"
    __table_args__ = {"schema": "platform"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_user_id = Column(UUID(as_uuid=True), nullable=True)
    actor_kind = Column(
        String(20),
        CheckConstraint("actor_kind IN ('user', 'platform_admin', 'system', 'ai')"),
        nullable=False,
        default="system",
    )
    tenant_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=True)
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    ip = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    details = Column("metadata", JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

