"""Servicio de reglas de negocio para menú y categorías."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.menus.models import MenuCategory, MenuProduct
from app.menus.repository import MenuRepository
from app.menus.schemas import CategoryCreate, ProductCreate


class MenuService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = MenuRepository(db)

    def create_category(self, data: CategoryCreate) -> MenuCategory:
        category = MenuCategory(
            name=data.name,
            display_order=data.display_order,
            is_active=True,
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def create_product(self, data: ProductCreate) -> MenuProduct:
        product = MenuProduct(
            category_id=data.category_id,
            name=data.name,
            description=data.description,
            price_cents=data.price_cents,
            image_url=data.image_url,
            is_active=True,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

