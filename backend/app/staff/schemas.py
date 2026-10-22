"""Esquemas Pydantic para personal del restaurante."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field


class StaffCreateRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    role: str = Field(..., pattern="^(admin|waiter|cashier|cook)$")
    phone: str | None = None
    position: str | None = None


class StaffProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    full_name: str
    phone: str | None = None
    position: str | None = None
    status: str
    hired_at: date | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

