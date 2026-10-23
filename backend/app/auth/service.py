"""Servicio de autenticación y emisión de tokens de sesión.

Basado en docs/04-MODULOS.md (Sección 4) y docs/08-SEGURIDAD-Y-ACCESO.md.
"""

from __future__ import annotations

import uuid
from datetime import timedelta
from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.security import create_access_token, verify_password
from app.platform.models import Tenant, TenantMembership, User

settings = Settings()


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def authenticate_user(
        self, email: str, password: str, tenant_slug: str | None = None
    ) -> Optional[Tuple[User, uuid.UUID | None, str | None]]:
        stmt = select(User).where(User.email == email.lower(), User.status == "active")
        user = self.db.execute(stmt).scalar_one_or_none()
        if not user or not user.password_hash:
            return None
        if not verify_password(password, user.password_hash):
            return None

        tenant_id: uuid.UUID | None = None
        role: str | None = None

        if tenant_slug:
            tenant = self.db.execute(
                select(Tenant).where(Tenant.slug == tenant_slug, Tenant.status == "active")
            ).scalar_one_or_none()
            if not tenant:
                return None
            membership = self.db.execute(
                select(TenantMembership).where(
                    TenantMembership.tenant_id == tenant.id,
                    TenantMembership.user_id == user.id,
                    TenantMembership.status == "active",
                )
            ).scalar_one_or_none()
            if not membership:
                return None
            tenant_id = tenant.id
            role = membership.role
        else:
            # Si no se indica tenant, tomar la primera membresía activa (si existe)
            membership = self.db.execute(
                select(TenantMembership).where(
                    TenantMembership.user_id == user.id,
                    TenantMembership.status == "active",
                )
            ).scalars().first()
            if membership:
                tenant = self.db.execute(
                    select(Tenant).where(Tenant.id == membership.tenant_id, Tenant.status == "active")
                ).scalar_one_or_none()
                if tenant:
                    tenant_id = tenant.id
                    role = membership.role

        return user, tenant_id, role

    def generate_session_token(
        self, user: User, tenant_id: uuid.UUID | None = None, role: str | None = None
    ) -> str:
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "tenant_id": str(tenant_id) if tenant_id else None,
            "role": role,
        }
        return create_access_token(payload, expires_delta=timedelta(minutes=settings.jwt_access_token_ttl_minutes))
