"""Esquemas Pydantic para reservas."""

from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    table_id: uuid.UUID | None = None
    reserved_for: datetime
    duration_minutes: int = Field(default=90, ge=30, le=360)
    party_size: int = Field(default=2, ge=1, le=50)
    contact_name: str = Field(..., min_length=2, max_length=255)
    contact_phone: str | None = None
    notes: str | None = None


class ReservationResponse(BaseModel):
    id: uuid.UUID
    table_id: uuid.UUID | None = None
    reserved_for: datetime
    duration_minutes: int
    party_size: int
    status: str
    contact_name: str
    contact_phone: str | None = None
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

