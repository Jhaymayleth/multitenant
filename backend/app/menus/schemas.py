"""Esquemas Pydantic para el menú del restaurante.

Basado en docs/04-MODULOS.md (Sección 6).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    display_order: int = Field(default=0, ge=0)


class CategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    display_order: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    category_id: uuid.UUID | None = None
    name: str = Field(..., min_length=2, max_length=80)
    description: str | None = Field(None, max_length=500)
    price_cents: int = Field(..., ge=0, description="Precio en centavos de la moneda del tenant")
    image_url: str | None = None


class ProductResponse(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID | None = None
    name: str
    description: str | None = None
    price_cents: int
    image_url: str | None = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

