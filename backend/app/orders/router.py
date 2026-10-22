"""Rutas de API para pedidos en el contexto del tenant."""

from __future__ import annotations

import uuid
from typing import Sequence
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import TenantContext, get_tenant_context, require_role
from app.orders.schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from app.orders.service import OrderService

router = APIRouter(prefix="/tenant/orders", tags=["Tenant Orders"])


@router.get("", response_model=list[OrderResponse], summary="Listar pedidos del restaurante por estado")
def list_orders(
    status: str | None = None,
    context: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.repo.list_orders(status=status)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear pedido presencial o a domicilio (idempotente)",
)
def create_order(
    data: OrderCreate,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    context: TenantContext = Depends(require_role("owner", "admin", "waiter")),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.create_order(data, idempotency_key=idempotency_key)


@router.get("/{order_id}", response_model=OrderResponse, summary="Obtener detalle de un pedido")
def get_order(
    order_id: uuid.UUID,
    context: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    order = service.repo.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    return order

