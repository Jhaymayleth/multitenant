"""Modelos ORM de pedidos y líneas de pedido en el schema del tenant.

Basado en:
- docs/04-MODULOS.md (Sección 8: Pedidos)
- docs/07-MODELO-DATOS.md (Sección 3: Pedidos)
Regla clave: Snapshots de nombre y precio en cada línea al confirmar.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_session_id = Column(UUID(as_uuid=True), ForeignKey("table_sessions.id"), nullable=True)
    customer_id = Column(UUID(as_uuid=True), nullable=True)
    type = Column(
        String(20),
        CheckConstraint("type IN ('dine_in', 'delivery')"),
        nullable=False,
        default="dine_in",
    )
    status = Column(
        String(30),
        CheckConstraint(
            "status IN ('draft', 'confirmed', 'in_preparation', 'ready', 'served', 'out_for_delivery', 'delivered', 'closed', 'cancelled')"
        ),
        nullable=False,
        default="draft",
    )
    payment_status = Column(
        String(20),
        CheckConstraint("payment_status IN ('unpaid', 'pending', 'paid', 'refunded', 'not_applicable')"),
        nullable=False,
        default="unpaid",
    )
    total_cents = Column(Integer, nullable=False, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    product_name = Column(String(80), nullable=False)  # Snapshot
    unit_price_cents = Column(Integer, nullable=False)  # Snapshot
    quantity = Column(SmallInteger, nullable=False, default=1)
    total_cents = Column(Integer, nullable=False)  # Snapshot
    notes = Column(String(255), nullable=True)

    order = relationship("Order", back_populates="items")

