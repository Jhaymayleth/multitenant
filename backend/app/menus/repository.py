"""Repositorio para catálogo de menú en el schema del tenant."""

from __future__ import annotations

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.menus.models import MenuCategory, MenuProduct


class MenuRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_categories(self, only_active: bool = False) -> Sequence[MenuCategory]:
        stmt = select(MenuCategory).order_by(MenuCategory.display_order.asc())
        if only_active:
            stmt = stmt.where(MenuCategory.is_active == True)
        return self.db.execute(stmt).scalars().all()

    def list_products(self, category_id: uuid.UUID | None = None, only_active: bool = False) -> Sequence[MenuProduct]:
        stmt = select(MenuProduct).order_by(MenuProduct.name.asc())
        if category_id:
            stmt = stmt.where(MenuProduct.category_id == category_id)
        if only_active:
            stmt = stmt.where(MenuProduct.is_active == True)
        return self.db.execute(stmt).scalars().all()

