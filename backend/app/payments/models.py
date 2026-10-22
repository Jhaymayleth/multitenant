"""Modelos ORM de caja ligera, pagos y comprobantes en el schema del tenant.

Basado en:
- docs/02-DECISIONES.md (D-070: Caja ligera y comprobantes)
- docs/04-MODULOS.md (Sección 10: Caja ligera, pagos y comprobantes)
- docs/07-MODELO-DATOS.md
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    reservation_id = Column(UUID(as_uuid=True), ForeignKey("reservations.id"), nullable=True)
    amount_cents = Column(Integer, nullable=False)
    status = Column(
        String(20),
        CheckConstraint("status IN ('pending', 'paid', 'refunded', 'failed')"),
        nullable=False,
        default="pending",
    )
    method = Column(
        String(20),
        CheckConstraint("method IN ('cash', 'card', 'online_sandbox')"),
        nullable=False,
    )
    reference = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    paid_at = Column(DateTime(timezone=True), nullable=True)

    events = relationship("PaymentEvent", back_populates="payment")
    receipt = relationship("Receipt", back_populates="payment", uselist=False)


class PaymentEvent(Base):
    __tablename__ = "payment_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), nullable=False)
    provider = Column(String(50), nullable=False)
    event_id = Column(String(255), unique=True, nullable=False)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    payment = relationship("Payment", back_populates="events")


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), unique=True, nullable=False)
    receipt_number = Column(String(50), nullable=False)
    token = Column(String(64), unique=True, nullable=False)  # Token aleatorio de descarga por QR
    total_cents = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    payment = relationship("Payment", back_populates="receipt")

