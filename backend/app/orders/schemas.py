"""Esquemas Pydantic para pedidos y líneas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(default=1, ge=1, le=100)
    notes: str | None = Field(None, max_length=255)


class OrderCreate(BaseModel):
    table_session_id: uuid.UUID | None = None
    type: str = Field(default="dine_in", pattern="^(dine_in|delivery)$")
    items: list[OrderItemCreate] = Field(default_factory=list)
    notes: str | None = None


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    unit_price_cents: int
    quantity: int
    total_cents: int
    notes: str | None = None

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: uuid.UUID
    table_session_id: uuid.UUID | None = None
    type: str
    status: str
    payment_status: str
    total_cents: int
    notes: str | None = None
    items: list[OrderItemResponse] = Field(default_factory=list)
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(confirmed|in_preparation|ready|served|closed|cancelled)$")

