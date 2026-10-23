"""Rutas de API para caja ligera y pagos del restaurante."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import TenantContext, require_role
from app.payments.schemas import PaymentCreate, PaymentResponse
from app.payments.service import PaymentService

router = APIRouter(prefix="/tenant/payments", tags=["Tenant Payments & Receipts"])


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar pago de pedido o reserva (CEO/Admin/Cajero)",
)
def create_payment(
    data: PaymentCreate,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    context: TenantContext = Depends(require_role("owner", "admin", "cashier")),
    db: Session = Depends(get_db),
):
    service = PaymentService(db)
    return service.register_payment(data)


@router.post(
    "/{payment_id}/confirm",
    response_model=PaymentResponse,
    summary="Confirmar pago y liberar mesa automáticamente",
)
def confirm_payment(
    payment_id: uuid.UUID,
    context: TenantContext = Depends(require_role("owner", "admin", "cashier")),
    db: Session = Depends(get_db),
):
    service = PaymentService(db)
    payment = service.repo.get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    return payment

