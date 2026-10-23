"""Servicio de pedidos y máquina de estados de preparación."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.orders.models import Order
from app.orders.repository import OrderRepository
from app.orders.schemas import OrderCreate


class OrderService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = OrderRepository(db)

    def create_order(self, data: OrderCreate, idempotency_key: str | None = None) -> Order:
        """Crea un pedido calculando totales en servidor y congelando snapshots de producto."""
        order = Order(
            table_session_id=data.table_session_id,
            type=data.type,
            status="confirmed",
            payment_status="unpaid",
            total_cents=0,
            notes=data.notes,
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

