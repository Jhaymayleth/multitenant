"""Rutas públicas del restaurante (Cara 1).

Basado en:
- docs/02-DECISIONES.md (1.2: Web pública del restaurante)
- docs/04-MODULOS.md (Secciones 6, 7, 10 y 11)

Regla clave:
El backend resuelve el tenant por el slug de la URL o el subdominio,
y fija el search_path hacia el schema de ese restaurante.
No expone datos internos del SaaS ni de otros restaurantes.
"""

from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db, set_tenant_schema
from app.menus.models import MenuCategory, MenuProduct
from app.menus.schemas import CategoryResponse, ProductResponse
from app.payments.models import Receipt
from app.payments.schemas import ReceiptResponse
from app.platform.models import Tenant
from app.sites.models import TenantSettings
from app.sites.schemas import SiteSettingsResponse
from app.tables.models import RestaurantTable, TableSession
from app.tables.schemas import ServiceRequestCreate, ServiceRequestResponse

router = APIRouter(prefix="/public", tags=["Public Client Endpoints"])


def resolve_tenant_by_slug(slug: str, db: Session) -> Tenant:
    stmt = select(Tenant).where(Tenant.slug == slug, Tenant.status == "active")
    tenant = db.execute(stmt).scalar_one_or_none()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado o inactivo",
        )
    set_tenant_schema(db, tenant.schema_name)
    return tenant


@router.get(
    "/{slug}",
    response_model=SiteSettingsResponse,
    summary="Obtener configuración visual e información pública del restaurante",
)
def get_public_site(slug: str, db: Session = Depends(get_db)):
    resolve_tenant_by_slug(slug, db)
    stmt = select(TenantSettings).where(TenantSettings.id == True, TenantSettings.is_published == True)
    settings = db.execute(stmt).scalar_one_or_none()
    if not settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sitio web no publicado")
    return settings


@router.get(
    "/{slug}/menu",
    response_model=list[ProductResponse],
    summary="Obtener menú público del restaurante",
)
def get_public_menu(slug: str, db: Session = Depends(get_db)):
    resolve_tenant_by_slug(slug, db)
    stmt = select(MenuProduct).where(MenuProduct.is_active == True).order_by(MenuProduct.name.asc())
    return db.execute(stmt).scalars().all()


@router.get(
    "/table/{token}",
    summary="Obtener o iniciar sesión anónima de mesa mediante código QR",
)
def get_table_by_qr(token: str, db: Session = Depends(get_db)):
    # Búsqueda de mesa por token opaco
    return {"message": "Sesión QR activa", "token": token}


@router.post(
    "/table/{token}/requests",
    summary="Enviar solicitud anónima desde la mesa (llamar mesero o pedir cuenta)",
)
def create_service_request(
    token: str,
    data: ServiceRequestCreate,
    db: Session = Depends(get_db),
):
    return {"message": f"Solicitud '{data.type}' recibida con éxito"}


@router.get(
    "/receipts/{token}",
    response_model=ReceiptResponse,
    summary="Descargar comprobante público mediante token QR",
)
def get_public_receipt(token: str, db: Session = Depends(get_db)):
    # Búsqueda en schema del tenant
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprobante no encontrado")

