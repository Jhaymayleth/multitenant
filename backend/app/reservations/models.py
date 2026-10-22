"""Modelos ORM de reservas en el schema del tenant.

Basado en docs/04-MODULOS.md (Sección 9) y docs/07-MODELO-DATOS.md.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_id = Column(UUID(as_uuid=True), ForeignKey("restaurant_tables.id"), nullable=True)
    customer_id = Column(UUID(as_uuid=True), nullable=True)
    reserved_for = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(SmallInteger, nullable=False, default=90)
    party_size = Column(SmallInteger, nullable=False, default=2)
    status = Column(
        String(20),
        CheckConstraint("status IN ('pending', 'confirmed', 'seated', 'cancelled', 'no_show')"),
        nullable=False,
        default="confirmed",
    )
    contact_name = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

