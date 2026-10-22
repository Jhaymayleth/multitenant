"""Servicio de reglas de negocio para mesas y sesiones QR."""

from __future__ import annotations

import secrets
import uuid
from sqlalchemy.orm import Session

from app.tables.models import RestaurantTable, TableSession
from app.tables.repository import TableRepository
from app.tables.schemas import TableCreate


class TableService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = TableRepository(db)

    def create_table(self, data: TableCreate) -> RestaurantTable:
        qr_token = secrets.token_urlsafe(32)
        table = RestaurantTable(
            number=data.number,
            capacity=data.capacity,
            status="available",
            qr_token=qr_token,
            is_active=True,
        )
        self.db.add(table)
        self.db.commit()
        self.db.refresh(table)
        return table

