"""Modelos ORM de menú en el schema del tenant.

Basado en:
- docs/03-ARQUITECTURA.md (Regla clave: sin columna tenant_id dentro del schema del tenant)
- docs/07-MODELO-DATOS.md (Sección 3: Catálogo)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MenuCategory(Base):
    __tablename__ = "menu_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(80), nullable=False)
    display_order = Column(SmallInteger, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    products = relationship("MenuProduct", back_populates="category")


class MenuProduct(Base):
    __tablename__ = "menu_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("menu_categories.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(80), nullable=False)
    description = Column(String(500), nullable=True)
    price_cents = Column(Integer, nullable=False, default=0)
    image_url = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    category = relationship("MenuCategory", back_populates="products")

