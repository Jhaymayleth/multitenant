"""Servicio de autenticación y emisión de tokens de sesión."""

from __future__ import annotations

import secrets
import uuid
from datetime import UTC, datetime, timedelta
from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.errors import AppError
from app.core.security import create_access_token, hash_password, sha256_hex, verify_password
from app.platform.models import Tenant, TenantMembership, User, VerificationCode
from app.shared.email import get_email_provider

settings = Settings()
RESET_CODE_TTL_MINUTES = 15
MAX_RESET_ATTEMPTS = 5


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

    def resolve_switch_tenant(
        self, user_id: uuid.UUID, tenant_id: uuid.UUID
    ) -> Tuple[User, uuid.UUID, str]:
        user = self.db.get(User, user_id)
        if not user or user.status != "active":
            raise AppError(code="INVALID_TOKEN", message="Sesión no válida.", status_code=401)

        tenant = self.db.execute(
            select(Tenant).where(Tenant.id == tenant_id, Tenant.status == "active")
        ).scalar_one_or_none()
        if not tenant:
            raise AppError(code="TENANT_INACTIVE", message="Restaurante no disponible.", status_code=403)

        membership = self.db.execute(
            select(TenantMembership).where(
                TenantMembership.tenant_id == tenant.id,
                TenantMembership.user_id == user.id,
                TenantMembership.status == "active",
            )
        ).scalar_one_or_none()
        if not membership:
            raise AppError(code="MEMBERSHIP_INACTIVE", message="No tienes acceso a ese restaurante.", status_code=403)

        return user, tenant.id, membership.role

    def request_password_reset(self, email: str) -> None:
        """Crea un código de un solo uso con caducidad de 15 minutos (D-153).

        La respuesta siempre es la misma: no revela si el correo existe.
        """
        user = self.db.execute(
            select(User).where(User.email == email.lower(), User.status == "active")
        ).scalar_one_or_none()
        if not user:
            return

        code = secrets.token_urlsafe(24)
        record = VerificationCode(
            user_id=user.id,
            purpose="password_reset",
            code_hash=sha256_hex(code),
            expires_at=datetime.now(UTC) + timedelta(minutes=RESET_CODE_TTL_MINUTES),
            attempts=0,
        )
        self.db.add(record)
        self.db.commit()

        try:
            get_email_provider(settings).send_password_reset(user.email, code)
        except Exception:
            # La entrega depende del proveedor (PD-23); no bloquea la respuesta.
            pass

    def reset_password(self, code: str, new_password: str) -> None:
        if len(new_password) < 8:
            raise AppError(code="WEAK_PASSWORD", message="La contraseña debe tener al menos 8 caracteres.", status_code=422)

        now = datetime.now(UTC)
        record = self.db.execute(
            select(VerificationCode).where(
                VerificationCode.code_hash == sha256_hex(code),
                VerificationCode.purpose == "password_reset",
                VerificationCode.consumed_at.is_(None),
            )
        ).scalar_one_or_none()

        if not record or record.attempts >= MAX_RESET_ATTEMPTS:
            raise AppError(code="CODE_INVALID", message="El código no es válido o ya se usó. Pide uno nuevo.", status_code=400)
        if record.expires_at < now:
            raise AppError(code="CODE_EXPIRED", message="El código venció. Pide uno nuevo.", status_code=400)

        record.attempts += 1
        user = self.db.get(User, record.user_id)
        if not user or user.status != "active":
            self.db.commit()
            raise AppError(code="CODE_INVALID", message="El código no es válido. Pide uno nuevo.", status_code=400)

        user.password_hash = hash_password(new_password)
        user.updated_at = now
        record.consumed_at = now
        self.db.commit()
