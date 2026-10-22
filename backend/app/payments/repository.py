"""Repositorio para pagos y comprobantes en el schema del tenant."""

from __future__ import annotations

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.payments.models import Payment, Receipt


class PaymentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_payment_by_id(self, payment_id: uuid.UUID) -> Payment | None:
        stmt = select(Payment).where(Payment.id == payment_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_receipt_by_token(self, token: str) -> Receipt | None:
        stmt = select(Receipt).where(Receipt.token == token)
        return self.db.execute(stmt).scalar_one_or_none()

