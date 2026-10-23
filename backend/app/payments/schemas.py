"""Esquemas Pydantic para pagos y comprobantes."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    order_id: uuid.UUID | None = None
    reservation_id: uuid.UUID | None = None
    amount_cents: int = Field(..., ge=1)
    method: str = Field(..., pattern="^(cash|card|online_sandbox)$")


class PaymentResponse(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID | None = None
    amount_cents: int
    status: str
    method: str
    reference: str | None = None
    created_at: datetime
    paid_at: datetime | None = None

    model_config = {"from_attributes": True}


class ReceiptResponse(BaseModel):
    id: uuid.UUID
    receipt_number: str
    token: str
    total_cents: int
    created_at: datetime

    model_config = {"from_attributes": True}

