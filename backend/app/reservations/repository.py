"""Repositorio para reservas en el schema del tenant."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.reservations.models import Reservation


class ReservationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_reservations(self) -> Sequence[Reservation]:
        stmt = select(Reservation).order_by(Reservation.reserved_for.asc())
        return self.db.execute(stmt).scalars().all()

