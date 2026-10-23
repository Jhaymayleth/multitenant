"""Modelos ORM de mesas, sesiones QR y solicitudes en el schema del tenant.

Basado en docs/07-MODELO-DATOS.md (Sección 3: Mesas y atención).
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    number = Column(String(20), nullable=False, unique=True)
    capacity = Column(SmallInteger, nullable=False, default=4)
    status = Column(
        String(20),
        CheckConstraint("status IN ('available', 'occupied', 'pending_payment', 'reserved', 'inactive')"),
        nullable=False,
        default="available",
    )
    qr_token = Column(String(64), nullable=True, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    sessions = relationship("TableSession", back_populates="table")


class TableSession(Base):
    __tablename__ = "table_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_id = Column(UUID(as_uuid=True), ForeignKey("restaurant_tables.id"), nullable=False)
    status = Column(
        String(20),
        CheckConstraint("status IN ('active', 'closed')"),
        nullable=False,
        default="active",
    )
    opened_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    closed_at = Column(DateTime(timezone=True), nullable=True)

    table = relationship("RestaurantTable", back_populates="sessions")
    service_requests = relationship("ServiceRequest", back_populates="session")


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("table_sessions.id"), nullable=False)
    type = Column(
        String(20),
        CheckConstraint("type IN ('waiter', 'bill', 'assistance')"),
        nullable=False,
    )
    status = Column(
        String(20),
        CheckConstraint("status IN ('pending', 'attended')"),
        nullable=False,
        default="pending",
    )
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    attended_at = Column(DateTime(timezone=True), nullable=True)

    session = relationship("TableSession", back_populates="service_requests")

