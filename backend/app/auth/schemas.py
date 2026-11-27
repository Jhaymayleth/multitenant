"""Esquemas Pydantic del módulo de autenticación."""

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


class TenantBrief(BaseModel):
    id: uuid.UUID
    slug: str
    name: str
    status: str


class UserMeResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    active_tenant_id: uuid.UUID | None = None
    active_tenant: TenantBrief | None = None
    role: str | None = None
    permissions: list[str] = Field(default_factory=list)


class SwitchTenantRequest(BaseModel):
    tenant_id: uuid.UUID


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    code: str = Field(..., min_length=16, max_length=128)
    new_password: str = Field(..., min_length=8)
