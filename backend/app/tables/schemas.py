"""Esquemas Pydantic para mesas y sesiones QR.

Basado en docs/04-MODULOS.md (Sección 7).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    number: str = Field(..., min_length=1, max_length=20)
    capacity: int = Field(default=4, ge=1, le=50)


class TableResponse(BaseModel):
    id: uuid.UUID
    number: str
    capacity: int
    status: str
    qr_token: str | None = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TableSessionResponse(BaseModel):
    id: uuid.UUID
    table_id: uuid.UUID
    status: str
    opened_at: datetime
    closed_at: datetime | None = None

    model_config = {"from_attributes": True}


class ServiceRequestCreate(BaseModel):
    type: str = Field(..., pattern="^(waiter|bill|assistance)$")


class ServiceRequestResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    type: str
    status: str
    created_at: datetime
    attended_at: datetime | None = None

    model_config = {"from_attributes": True}

