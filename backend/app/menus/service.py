"""Servicio de reglas de negocio para menú y categorías."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.menus.models import MenuCategory, MenuProduct
from app.menus.repository import MenuRepository
from app.menus.schemas import (
    CategoryCreate,
    CategoryUpdate,
    OrderUpdate,
    ProductCreate,
    ProductUpdate,
    PublicationUpdate,
)


class MenuService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = MenuRepository(db)

    # Categorías ---------------------------------------------------------
    def _validate_category_name(self, name: str, exclude_id: uuid.UUID | None = None) -> None:
        for category in self.repo.list_categories():
            if category.is_active and category.name.lower() == name.lower() and category.id != exclude_id:
                raise AppError(code="DUPLICATE_CATEGORY_NAME", message="Ya existe una categoría con ese nombre.", status_code=409)

    def create_category(self, data: CategoryCreate) -> MenuCategory:
        self._validate_category_name(data.name)
        category = MenuCategory(
            name=data.name,
            display_order=data.display_order,
            is_active=True,
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(self, category_id: uuid.UUID, data: CategoryUpdate) -> MenuCategory:
        category = self.repo.get_category(category_id)
        if not category or not category.is_active:
            raise AppError(code="CATEGORY_NOT_FOUND", message="Categoría no encontrada.", status_code=404)
        self._validate_category_name(data.name, exclude_id=category.id)
        category.name = data.name
        category.display_order = data.display_order
        category.is_active = data.is_active
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete_category(self, category_id: uuid.UUID) -> None:
        category = self.repo.get_category(category_id)
        if not category or not category.is_active:
            raise AppError(code="CATEGORY_NOT_FOUND", message="Categoría no encontrada.", status_code=404)
        active_products = [
            product for product in self.repo.list_products(category_id=category.id, only_active=True)
        ]
        if active_products:
            raise AppError(
                code="CATEGORY_IN_USE",
                message="Mueve o retira los productos antes de borrar la categoría.",
                status_code=409,
            )
        category.is_active = False
        self.db.commit()

    # Productos ----------------------------------------------------------
    def _validate_product(self, category_id: uuid.UUID | None, name: str, exclude_id: uuid.UUID | None = None) -> None:
        if not category_id:
            raise AppError(code="INVALID_CATEGORY", message="Selecciona una categoría.", status_code=422)
        category = self.repo.get_category(category_id)
        if not category or not category.is_active:
            raise AppError(code="INVALID_CATEGORY", message="La categoría no existe o está inactiva.", status_code=422)
        if self.repo.product_name_exists(name, category_id, exclude_id=exclude_id):
            raise AppError(code="DUPLICATE_PRODUCT_NAME", message="Ya existe ese producto en la categoría.", status_code=409)

    def create_product(self, data: ProductCreate) -> MenuProduct:
        self._validate_product(data.category_id, data.name)
        product = MenuProduct(
            category_id=data.category_id,
            name=data.name,
            description=data.description,
            price_cents=data.price_cents,
            image_url=data.image_url,
            display_order=data.display_order,
            is_active=True,
            is_published=data.is_published,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product_id: uuid.UUID, data: ProductUpdate) -> MenuProduct:
        product = self.repo.get_product(product_id)
        if not product or not product.is_active:
            raise AppError(code="PRODUCT_NOT_FOUND", message="Producto no encontrado.", status_code=404)
        self._validate_product(data.category_id, data.name, exclude_id=product.id)

        product.category_id = data.category_id
        product.name = data.name
        product.description = data.description
        product.price_cents = data.price_cents
        product.image_url = data.image_url
        product.display_order = data.display_order
        product.is_active = data.is_active
        product.is_published = data.is_published if data.is_active else False
        self.db.commit()
        self.db.refresh(product)
        return product

    def publish_product(self, product_id: uuid.UUID, data: PublicationUpdate) -> MenuProduct:
        product = self.repo.get_product(product_id)
        if not product or not product.is_active:
            raise AppError(code="PRODUCT_NOT_FOUND", message="Producto no encontrado.", status_code=404)
        product.is_published = data.is_published
        self.db.commit()
        self.db.refresh(product)
        return product

    def reorder_product(self, product_id: uuid.UUID, data: OrderUpdate) -> MenuProduct:
        product = self.repo.get_product(product_id)
        if not product or not product.is_active:
            raise AppError(code="PRODUCT_NOT_FOUND", message="Producto no encontrado.", status_code=404)
        product.display_order = data.display_order
        self.db.commit()
        self.repo.normalize_order(product.category_id)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: uuid.UUID) -> None:
        product = self.repo.get_product(product_id)
        if not product or not product.is_active:
            raise AppError(code="PRODUCT_NOT_FOUND", message="Producto no encontrado.", status_code=404)
        product.is_active = False
        product.is_published = False
        self.db.commit()
