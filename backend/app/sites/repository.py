"""Repositorio para la configuración singleton del sitio en el schema del tenant."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.sites.models import TenantSettings


class SiteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_settings(self) -> TenantSettings | None:
        stmt = select(TenantSettings).where(TenantSettings.id == True)
        return self.db.execute(stmt).scalar_one_or_none()

