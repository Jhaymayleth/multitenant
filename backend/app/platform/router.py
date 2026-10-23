"""Rutas de la API para plataforma y administración global de Lixus.

Basado en docs/04-MODULOS.md (Sección 3).
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.platform.schemas import (
    PlanResponse,
    TenantCreateRequest,
    TenantResponse,
    TenantVerifyRequest,
)
from app.platform.service import PlatformService

router = APIRouter(prefix="/platform", tags=["Platform (Lixus)"])


@router.post(
    "/tenants",
    response_model=TenantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Aprovisionar un nuevo restaurante (tenant) con schema aislado",
)
def create_tenant(
    data: TenantCreateRequest,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    db: Session = Depends(get_db),
):
    service = PlatformService(db)
    tenant = service.provision_tenant(data, idempotency_key=idempotency_key)
    return tenant


@router.get(
    "/tenants",
    response_model=list[TenantResponse],
    summary="Listar restaurantes registrados en la plataforma",
)
def list_tenants(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    service = PlatformService(db)
    return service.repo.list_tenants(limit=limit, offset=offset)


@router.get(
    "/tenants/{tenant_id}",
    response_model=TenantResponse,
    summary="Obtener detalle y estado de un restaurante",
)
def get_tenant(
    tenant_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    service = PlatformService(db)
    tenant = service.repo.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant no encontrado")
    return tenant


@router.post(
    "/tenants/{tenant_id}/verify",
    response_model=TenantResponse,
    summary="Aprobar o rechazar la verificación de un restaurante",
)
def verify_tenant(
    tenant_id: uuid.UUID,
    data: TenantVerifyRequest,
    db: Session = Depends(get_db),
):
    service = PlatformService(db)
    tenant = service.repo.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant no encontrado")
    # Esqueleto de verificación
    return tenant


@router.get(
    "/plans",
    response_model=list[PlanResponse],
    summary="Listar planes y capacidades disponibles",
)
def list_plans(
    db: Session = Depends(get_db),
):
    service = PlatformService(db)
    return service.repo.list_active_plans()

