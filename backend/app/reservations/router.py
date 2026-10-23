"""Rutas de API para reservas en el contexto del tenant."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import TenantContext, get_tenant_context, require_role
from app.reservations.schemas import ReservationCreate, ReservationResponse
from app.reservations.service import ReservationService

router = APIRouter(prefix="/tenant/reservations", tags=["Tenant Reservations"])


@router.get("", response_model=list[ReservationResponse], summary="Listar reservas del restaurante")
def list_reservations(
    context: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = ReservationService(db)
    return service.repo.list_reservations()


@router.post(
    "",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear reserva en el restaurante",
)
def create_reservation(
    data: ReservationCreate,
    context: TenantContext = Depends(require_role("owner", "admin", "waiter")),
    db: Session = Depends(get_db),
):
    service = ReservationService(db)
    return service.create_reservation(data)

