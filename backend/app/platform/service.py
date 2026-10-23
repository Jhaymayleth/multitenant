"""Capa de servicio de plataforma y aprovisionamiento multitenant.

Basado en docs/03-ARQUITECTURA.md (Sección 2.3: Aprovisionamiento de un tenant)
y docs/04-MODULOS.md (Sección 3).
"""

from __future__ import annotations

import secrets

from sqlalchemy.orm import Session

from app.platform.models import Tenant
from app.platform.repository import PlatformRepository
from app.platform.schemas import TenantCreateRequest


class PlatformService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = PlatformRepository(db)

    def generate_schema_name(self) -> str:
        """Genera un identificador seguro de schema: tenant_<12 caracteres hex>."""
        hex_suffix = secrets.token_hex(6)
        return f"tenant_{hex_suffix}"

    def provision_tenant(self, data: TenantCreateRequest, idempotency_key: str | None = None) -> Tenant:
        """Contrato de aprovisionamiento de un nuevo tenant:
        
        Pasos del flujo:
        1. Validar identidad, permiso global e idempotencia.
        2. Insertar tenant en estado 'provisioning' (platform).
        3. CREATE SCHEMA tenant_<id> con el rol de migraciones.
        4. Aplicar migraciones del tenant con Alembic (version_table_schema = schema).
        5. Insertar configuración inicial y usuario CEO con membresía 'owner'.
        6. Otorgar permisos al rol de aplicación sobre el schema nuevo.
        7. Cambiar estado a 'pending_verification' o 'active'.
        """
        schema_name = self.generate_schema_name()

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
        return tenant

