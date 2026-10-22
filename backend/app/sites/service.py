"""Servicio de configuración del sitio público."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.sites.models import TenantSettings
from app.sites.repository import SiteRepository
from app.sites.schemas import SiteSettingsUpdate


class SiteService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = SiteRepository(db)

    def update_settings(self, data: SiteSettingsUpdate) -> TenantSettings:
        settings = self.repo.get_settings()
        if not settings:
            settings = TenantSettings(
                id=True,
                display_name=data.display_name,
                tagline=data.tagline,
                description=data.description,
                color_primary=data.color_primary,
                color_secondary=data.color_secondary,
                address=data.address,
                hours=data.hours,
                is_published=True,
            )
            self.db.add(settings)
        else:
            settings.display_name = data.display_name
            settings.tagline = data.tagline
            settings.description = data.description
            if data.color_primary:
                settings.color_primary = data.color_primary
            if data.color_secondary:
                settings.color_secondary = data.color_secondary
            settings.address = data.address
            settings.hours = data.hours

        self.db.commit()
        self.db.refresh(settings)
        return settings

