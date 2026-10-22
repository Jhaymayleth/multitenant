"""Repositorio para pedidos en el schema del tenant."""

from __future__ import annotations

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.orders.models import Order


class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_orders(self, status: str | None = None) -> Sequence[Order]:
        stmt = select(Order).options(selectinload(Order.items)).order_by(Order.created_at.desc())
        if status:
            stmt = stmt.where(Order.status == status)
        return self.db.execute(stmt).scalars().all()

    def get_order_by_id(self, order_id: uuid.UUID) -> Order | None:
        stmt = select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
        return self.db.execute(stmt).scalar_one_or_none()

