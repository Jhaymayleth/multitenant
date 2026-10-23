"""Capa de repositorio para el schema global platform."""

from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.platform.models import Plan, Tenant


class PlatformRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_tenant_by_id(self, tenant_id: uuid.UUID) -> Tenant | None:
        return self.db.execute(select(Tenant).where(Tenant.id == tenant_id)).scalar_one_or_none()

    def get_tenant_by_slug(self, slug: str) -> Tenant | None:
        return self.db.execute(select(Tenant).where(Tenant.slug == slug)).scalar_one_or_none()

    def list_tenants(self, limit: int = 50, offset: int = 0) -> Sequence[Tenant]:
        stmt = select(Tenant).order_by(Tenant.created_at.desc()).limit(limit).offset(offset)
        return self.db.execute(stmt).scalars().all()

    def list_active_plans(self) -> Sequence[Plan]:
        stmt = select(Plan).where(Plan.is_active == True)
        return self.db.execute(stmt).scalars().all()

