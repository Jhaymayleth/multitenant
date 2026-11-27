"""Repositorio para catálogo de menú en el schema del tenant."""

from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.menus.models import MenuCategory, MenuProduct


class MenuRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_categories(self, only_active: bool = False) -> Sequence[MenuCategory]:
        stmt = select(MenuCategory).order_by(MenuCategory.display_order.asc(), MenuCategory.name.asc())
        if only_active:
            stmt = stmt.where(MenuCategory.is_active.is_(True))
        return self.db.execute(stmt).scalars().all()

    def get_category(self, category_id: uuid.UUID) -> MenuCategory | None:
        return self.db.get(MenuCategory, category_id)

    def list_products(
        self,
        category_id: uuid.UUID | None = None,
        only_active: bool = False,
        only_published: bool = False,
    ) -> Sequence[MenuProduct]:
        stmt = select(MenuProduct).order_by(MenuProduct.display_order.asc(), MenuProduct.name.asc())
        if category_id:
            stmt = stmt.where(MenuProduct.category_id == category_id)
        if only_active:
            stmt = stmt.where(MenuProduct.is_active.is_(True))
        if only_published:
            stmt = stmt.where(MenuProduct.is_published.is_(True))
        return self.db.execute(stmt).scalars().all()

    def get_product(self, product_id: uuid.UUID) -> MenuProduct | None:
        return self.db.get(MenuProduct, product_id)

    def product_name_exists(
        self, name: str, category_id: uuid.UUID | None, exclude_id: uuid.UUID | None = None
    ) -> bool:
        stmt = select(MenuProduct.id).where(
            MenuProduct.name.ilike(name),
            MenuProduct.is_active.is_(True),
        )
        if category_id:
            stmt = stmt.where(MenuProduct.category_id == category_id)
        else:
            stmt = stmt.where(MenuProduct.category_id.is_(None))
        if exclude_id:
            stmt = stmt.where(MenuProduct.id != exclude_id)
        return self.db.execute(stmt).first() is not None

    def normalize_order(self, category_id: uuid.UUID | None) -> None:
        stmt = select(MenuProduct)
        if category_id:
            stmt = stmt.where(MenuProduct.category_id == category_id)
        else:
            stmt = stmt.where(MenuProduct.category_id.is_(None))
        products = self.db.execute(
            stmt.order_by(MenuProduct.display_order.asc(), MenuProduct.name.asc())
        ).scalars().all()
        for index, product in enumerate(products):
            product.display_order = index
