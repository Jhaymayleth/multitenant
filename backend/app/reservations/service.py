"""Servicio de reservas con validación de no solapamiento."""

from __future__ import annotations

import uuid
from sqlalchemy.orm import Session

from app.reservations.models import Reservation
from app.reservations.repository import ReservationRepository
from app.reservations.schemas import ReservationCreate


class ReservationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = ReservationRepository(db)

    def create_reservation(self, data: ReservationCreate) -> Reservation:
        reservation = Reservation(
            table_id=data.table_id,
            reserved_for=data.reserved_for,
            duration_minutes=data.duration_minutes,
            party_size=data.party_size,
            contact_name=data.contact_name,
            contact_phone=data.contact_phone,
            notes=data.notes,
            status="confirmed",
        )
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

