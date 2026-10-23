"""Capa de servicio de plataforma y aprovisionamiento multitenant.

Basado en docs/03-ARQUITECTURA.md (Sección 2.3: Aprovisionamiento de un tenant)
y docs/04-MODULOS.md (Sección 3).
"""

from __future__ import annotations

import json
import os
import secrets
import subprocess
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.errors import AppError
from app.core.security import sha256_hex
from app.platform.models import (
    GlobalIdempotencyKey,
    Tenant,
    TenantMembership,
    User,
)
from app.platform.repository import PlatformRepository
from app.platform.schemas import TenantCreateRequest
from app.sites.models import TenantSettings

settings = Settings()


class PlatformService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = PlatformRepository(db)

    def generate_schema_name(self) -> str:
        """Genera un identificador seguro de schema: tenant_<12 caracteres hex>."""
        while True:
            hex_suffix = secrets.token_hex(6)
            candidate = f"tenant_{hex_suffix}"
            existing = self.db.execute(
                select(Tenant).where(Tenant.schema_name == candidate)
            ).scalar_one_or_none()
            if not existing:
                return candidate

    def _backend_root(self) -> str:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    def _run_tenant_migrations(self, schema_name: str) -> None:
        """Aplica la cadena de migraciones del tenant sobre el schema indicado."""
        cmd = [
            "alembic",
            "-c",
            "migrations/tenant/alembic.ini",
            "-x",
            f"schema={schema_name}",
            "upgrade",
            "head",
        ]
        env = os.environ.copy()
        env["PYTHONPATH"] = self._backend_root()
        result = subprocess.run(
            cmd,
            cwd=self._backend_root(),
            capture_output=True,
            text=True,
            env=env,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Error aplicando migraciones del tenant {schema_name}: {result.stderr or result.stdout}"
            )

    def provision_tenant(self, data: TenantCreateRequest, idempotency_key: str | None = None) -> Tenant:
        """Aprovisiona un nuevo tenant con schema aislado.

        Pasos:
        1. Idempotencia (si se envía clave).
        2. Validar slug único.
        3. Insertar tenant en estado 'provisioning'.
        4. CREATE SCHEMA.
        5. Aplicar migraciones del tenant.
        6. Crear usuario CEO y membresía 'owner'.
        7. Insertar tenant_settings inicial.
        8. Otorgar permisos al rol de aplicación.
        9. Cambiar estado a 'pending_verification'.
        """
        scope = "platform:create_tenant"

        # 1. Idempotencia
        request_hash = sha256_hex(json.dumps(data.model_dump(mode="json"), sort_keys=True))
        idemp_row: GlobalIdempotencyKey | None = None
        if idempotency_key:
            idemp_row = self.db.execute(
                select(GlobalIdempotencyKey).where(
                    GlobalIdempotencyKey.scope == scope,
                    GlobalIdempotencyKey.key == idempotency_key,
                )
            ).scalar_one_or_none()

            if idemp_row:
                if idemp_row.status == "completed" and idemp_row.response_body:
                    tenant_id = idemp_row.response_body.get("tenant_id")
                    if tenant_id:
                        tenant = self.repo.get_tenant_by_id(uuid.UUID(tenant_id))
                        if tenant:
                            return tenant
                if idemp_row.status == "in_progress":
                    raise AppError(
                        code="IDEMPOTENCY_IN_PROGRESS",
                        message="La solicitud de aprovisionamiento ya está en proceso",
                        status_code=409,
                    )
                if idemp_row.status == "failed":
                    self.db.delete(idemp_row)
                    self.db.commit()
                    idemp_row = None

            if not idemp_row:
                idemp_row = GlobalIdempotencyKey(
                    scope=scope,
                    key=idempotency_key,
                    request_hash=request_hash,
                    status="in_progress",
                    expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
                )
                self.db.add(idemp_row)
                self.db.commit()

        # 2. Validar slug único
        existing_slug = self.repo.get_tenant_by_slug(data.slug)
        if existing_slug:
            if idemp_row:
                idemp_row.status = "failed"
                self.db.commit()
            raise AppError(
                code="SLUG_ALREADY_EXISTS",
                message="Ya existe un restaurante con ese slug",
                status_code=409,
            )

        schema_name = self.generate_schema_name()

        # 3. Insertar tenant en estado provisioning
        tenant = Tenant(
            name=data.name,
            slug=data.slug,
            schema_name=schema_name,
            legal_name=data.legal_name,
            contact_email=data.contact_email,
            timezone=data.timezone,
            currency=data.currency,
            status="provisioning",
        )
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)

        try:
            # 4. CREATE SCHEMA
            self.db.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))
            self.db.commit()

            # 5. Aplicar migraciones del tenant
            self._run_tenant_migrations(schema_name)

            # 6. Crear usuario CEO y membresía owner
            user = self.db.execute(
                select(User).where(User.email == data.owner_email.lower())
            ).scalar_one_or_none()
            if not user:
                user = User(
                    email=data.owner_email.lower(),
                    full_name=data.owner_full_name,
                    status="active",
                    password_hash=None,
                )
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)

            membership = TenantMembership(
                tenant_id=tenant.id,
                user_id=user.id,
                role="owner",
                status="active",
                created_by=user.id,
            )
            self.db.add(membership)
            self.db.commit()

            # 7. Insertar tenant_settings inicial
            self.db.execute(text(f'SET search_path TO "{schema_name}"'))
            settings_row = TenantSettings(
                id=True,
                display_name=data.name,
                tagline=None,
                description=None,
                color_primary="#0284c7",
                color_secondary="#0f172a",
                is_published=False,
            )
            self.db.add(settings_row)
            self.db.commit()

            # Restaurar search_path a platform
            self.db.execute(text("SET search_path TO platform, public"))

            # 8. Otorgar permisos al rol de aplicación
            self.db.execute(text(f'GRANT USAGE ON SCHEMA "{schema_name}" TO lixus_app'))
            self.db.execute(
                text(f'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "{schema_name}" TO lixus_app')
            )
            self.db.execute(
                text(f'ALTER DEFAULT PRIVILEGES IN SCHEMA "{schema_name}" GRANT ALL ON TABLES TO lixus_app')
            )
            self.db.commit()

            # 9. Cambiar estado
            tenant.status = "pending_verification"
            self.db.commit()
            self.db.refresh(tenant)

            if idemp_row:
                idemp_row.status = "completed"
                idemp_row.response_status = 201
                idemp_row.response_body = {"tenant_id": str(tenant.id)}
                self.db.commit()

            return tenant

        except Exception as exc:
            self.db.rollback()
            try:
                tenant.status = "provisioning_failed"
                self.db.commit()
            except Exception:
                self.db.rollback()
            if idemp_row:
                try:
                    idemp_row.status = "failed"
                    self.db.commit()
                except Exception:
                    self.db.rollback()
            raise AppError(
                code="TENANT_PROVISIONING_FAILED",
                message=f"Error al aprovisionar el restaurante: {exc}",
                status_code=500,
            )
