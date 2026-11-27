"""Rutas de API para menú en el contexto del tenant."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import TenantContext, get_tenant_context, require_role
from app.menus.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    OrderUpdate,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    PublicationUpdate,
)
from app.menus.service import MenuService

router = APIRouter(prefix="/tenant/menu", tags=["Tenant Menu"])
WRITE_ROLES = ("owner", "admin")


@router.get("/categories", response_model=list[CategoryResponse], summary="Listar categorías del menú")
def list_categories(
    context: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    return MenuService(db).repo.list_categories()


@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear categoría (owner/admin)",
)
def create_category(
    data: CategoryCreate,
    context: TenantContext = Depends(require_role(*WRITE_ROLES)),
    db: Session = Depends(get_db),
):
    return MenuService(db).create_category(data)


@router.put("/categories/{category_id}", response_model=CategoryResponse, summary="Editar categoría (owner/admin)")
def update_category(
    category_id: uuid.UUID,
    data: CategoryUpdate,
    context: TenantContext = Depends(require_role(*WRITE_ROLES)),
    db: Session = Depends(get_db),
):
    return MenuService(db).update_category(category_id, data)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Retirar categoría (owner/admin)")
def delete_category(
    category_id: uuid.UUID,
    context: TenantContext = Depends(require_role(*WRITE_ROLES)),
    db: Session = Depends(get_db),
):
    MenuService(db).delete_category(category_id)


@router.get("/products", response_model=list[ProductResponse], summary="Listar productos del menú")
def list_products(
    category_id: uuid.UUID | None = None,
    context: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    return MenuService(db).repo.list_products(category_id=category_id)


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto (owner/admin)",
)
def create_product(
    data: ProductCreate,
    context: TenantContext = Depends(require_role(*WRITE_ROLES)),
    db: Session = Depends(get_db),
):
    return MenuService(db).create_product(data)


@router.put("/products/{product_id}", response_model=ProductResponse, summary="Editar producto (owner/admin)")
def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    context: TenantContext = Depends(require_role(*WRITE_ROLES)),
    db: Session = Depends(get_db),
):
    return MenuService(db).update_product(product_id, data)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Retirar producto (owner/admin)")
def delete_product(
    product_id: uuid.UUID,
    context: TenantContext = Depends(require_role(*WRITE_ROLES)),
    db: Session = Depends(get_db),
):
    MenuService(db).delete_product(product_id)


@router.patch(
    "/products/{product_id}/publication",
    response_model=ProductResponse,
    summary="Publicar u ocultar producto (owner/admin)",
)
def publish_product(
    product_id: uuid.UUID,
    data: PublicationUpdate,
    context: TenantContext = Depends(require_role(*WRITE_ROLES)),
    db: Session = Depends(get_db),
):
    return MenuService(db).publish_product(product_id, data)


@router.patch(
    "/products/{product_id}/order",
    response_model=ProductResponse,
    summary="Reordenar producto (owner/admin)",
)
def reorder_product(
    product_id: uuid.UUID,
    data: OrderUpdate,
    context: TenantContext = Depends(require_role(*WRITE_ROLES)),
    db: Session = Depends(get_db),
):
    return MenuService(db).reorder_product(product_id, data)
