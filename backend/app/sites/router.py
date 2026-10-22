"""Rutas de API para configuración del sitio web del restaurante."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import TenantContext, get_tenant_context, require_role
from app.sites.schemas import SiteSettingsResponse, SiteSettingsUpdate
from app.sites.service import SiteService

router = APIRouter(prefix="/tenant/public-site", tags=["Tenant Public Site Admin"])


@router.get("", response_model=SiteSettingsResponse, summary="Obtener configuración del sitio web del restaurante")
def get_site_settings(
    context: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = SiteService(db)
    settings = service.repo.get_settings()
    if not settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuración no encontrada")
    return settings


@router.put("", response_model=SiteSettingsResponse, summary="Actualizar configuración del sitio web (CEO)")
def update_site_settings(
    data: SiteSettingsUpdate,
    context: TenantContext = Depends(require_role("owner")),
    db: Session = Depends(get_db),
):
    service = SiteService(db)
    return service.update_settings(data)

