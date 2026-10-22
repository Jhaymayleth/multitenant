"""Esquemas Pydantic del módulo de plataforma y administración de Lixus.

Basado en docs/04-MODULOS.md (Sección 3).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class TenantCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Nombre comercial del restaurante")
    slug: str = Field(..., pattern=r"^[a-z0-9-]{3,40}$", description="Identificador único para subdominio")
    legal_name: str | None = Field(None, max_length=255)
    contact_email: EmailStr
    owner_full_name: str = Field(..., min_length=3, max_length=255)
    owner_email: EmailStr
    timezone: str = Field(default="America/Bogota")
    currency: str = Field(default="COP", min_length=3, max_length=3)


class TenantResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    schema_name: str
    status: str
    timezone: str
    currency: str
    contact_email: str | None = None
    created_at: datetime
    activated_at: datetime | None = None

    model_config = {"from_attributes": True}


class TenantVerifyRequest(BaseModel):
    action: str = Field(..., pattern="^(approve|reject)$")
    rejection_reason: str | None = None


class PlanResponse(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    capabilities: dict
    limits: dict
    price_cents: int
    currency: str
    is_active: bool

    model_config = {"from_attributes": True}

