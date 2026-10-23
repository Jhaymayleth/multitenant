"""Servicio de pagos y emisión de comprobantes."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.payments.models import Payment
from app.payments.repository import PaymentRepository
from app.payments.schemas import PaymentCreate


class PaymentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = PaymentRepository(db)

    def register_payment(self, data: PaymentCreate) -> Payment:
        payment = Payment(
            order_id=data.order_id,
            reservation_id=data.reservation_id,
            amount_cents=data.amount_cents,
            method=data.method,
            status="pending" if data.method == "online_sandbox" else "paid",
            paid_at=datetime.now(UTC) if data.method != "online_sandbox" else None,
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

