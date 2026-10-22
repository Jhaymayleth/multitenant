"""Modelos ORM de empleados en el schema del tenant.

Basado en docs/07-MODELO-DATOS.md (Sección 3.2: staff_profiles).
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from sqlalchemy import CheckConstraint, Column, Date, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StaffProfile(Base):
    __tablename__ = "staff_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False)  # Referencia lógica a platform.users
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    position = Column(String(100), nullable=True)
    status = Column(
        String(20),
        CheckConstraint("status IN ('active', 'inactive')"),
        nullable=False,
        default="active",
    )
    hired_at = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

