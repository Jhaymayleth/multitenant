"""Rutas de API para administración de mesas en el restaurante."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import TenantContext, get_tenant_context, require_role
from app.tables.schemas import TableCreate, TableResponse
from app.tables.service import TableService

router = APIRouter(prefix="/tenant/tables", tags=["Tenant Tables & QR"])


@router.get("", response_model=list[TableResponse], summary="Listar mesas y estado de atención")
def list_tables(
    context: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = TableService(db)
    return service.repo.list_tables()


@router.post(
    "",
    response_model=TableResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear mesa y generar token QR opaco (CEO/Admin)",
)
def create_table(
    data: TableCreate,
    context: TenantContext = Depends(require_role("owner", "admin")),
    db: Session = Depends(get_db),
):
    service = TableService(db)
    return service.create_table(data)

