"""Esquemas Pydantic del módulo de autenticación.

Basado en docs/04-MODULOS.md (Sección 4).
"""

from __future__ import annotations

import uuid
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    tenant_slug: str | None = Field(None, description="Slug del tenant al que se desea ingresar")


class TokenResponse(BaseModel):
    token_type: str = "bearer"
    expires_in_minutes: int


class UserMeResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    active_tenant_id: uuid.UUID | None = None
    role: str | None = None


class SwitchTenantRequest(BaseModel):
    tenant_id: uuid.UUID

