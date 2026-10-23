"""Rutas de API para menú en el contexto del tenant.

Basado en docs/04-MODULOS.md (Sección 6).
Requiere contexto de tenant resuelto por el servidor.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import TenantContext, get_tenant_context, require_role
from app.menus.schemas import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse
from app.menus.service import MenuService

router = APIRouter(prefix="/tenant/menu", tags=["Tenant Menu"])


@router.get(
    "/categories",
    response_model=list[CategoryResponse],
    summary="Listar categorías del menú del restaurante",
)
def list_categories(
    context: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = MenuService(db)
    return service.repo.list_categories()


@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva categoría de menú (CEO/Admin)",
)
def create_category(
    data: CategoryCreate,
    context: TenantContext = Depends(require_role("owner", "admin")),
    db: Session = Depends(get_db),
):
    service = MenuService(db)
    return service.create_category(data)


@router.get(
    "/products",
    response_model=list[ProductResponse],
    summary="Listar productos del menú del restaurante",
)
def list_products(
    category_id: uuid.UUID | None = None,
    context: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = MenuService(db)
    return service.repo.list_products(category_id=category_id)


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto en el menú (CEO/Admin)",
)
def create_product(
    data: ProductCreate,
    context: TenantContext = Depends(require_role("owner", "admin")),
    db: Session = Depends(get_db),
):
    service = MenuService(db)
    return service.create_product(data)

