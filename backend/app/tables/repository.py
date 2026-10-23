"""Repositorio para mesas y sesiones en el schema del tenant."""

from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.tables.models import RestaurantTable, TableSession


class TableRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_tables(self) -> Sequence[RestaurantTable]:
        stmt = select(RestaurantTable).order_by(RestaurantTable.number.asc())
        return self.db.execute(stmt).scalars().all()

    def get_table_by_qr_token(self, qr_token: str) -> RestaurantTable | None:
        stmt = select(RestaurantTable).where(RestaurantTable.qr_token == qr_token)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_active_session(self, table_id: uuid.UUID) -> TableSession | None:
        stmt = select(TableSession).where(
            TableSession.table_id == table_id,
            TableSession.status == "active",
        )
        return self.db.execute(stmt).scalar_one_or_none()

