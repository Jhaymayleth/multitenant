"""Servicio de autenticación y emisión de tokens de sesión.

Basado en docs/04-MODULOS.md (Sección 4) y docs/08-SEGURIDAD-Y-ACCESO.md.
"""

from __future__ import annotations

import uuid
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.security import create_access_token, verify_password
from app.platform.models import User

settings = Settings()


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def authenticate_user(self, email: str, password: str) -> User | None:
        stmt = select(User).where(User.email == email.lower(), User.status == "active")
        user = self.db.execute(stmt).scalar_one_or_none()
        if not user or not user.password_hash:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def generate_session_token(self, user: User, tenant_id: uuid.UUID | None = None, role: str | None = None) -> str:
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "tenant_id": str(tenant_id) if tenant_id else None,
            "role": role,
        }
        return create_access_token(payload, expires_delta=timedelta(minutes=settings.jwt_access_token_ttl_minutes))

