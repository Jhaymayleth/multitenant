"""Modelos ORM de configuración visual y pública del tenant (tabla singleton).

Basado en:
- docs/02-DECISIONES.md (1.2: Web pública del restaurante)
- docs/07-MODELO-DATOS.md (Sección 3.1: tenant_settings)
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class TenantSettings(Base):
    __tablename__ = "tenant_settings"
    __table_args__ = (CheckConstraint("id = true", name="singleton_tenant_settings"),)

    id = Column(Boolean, primary_key=True, default=True)
    display_name = Column(String(255), nullable=False)
    tagline = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    logo_url = Column(Text, nullable=True)
    hero_image_url = Column(Text, nullable=True)
    color_primary = Column(String(7), nullable=True, default="#0284c7")
    color_secondary = Column(String(7), nullable=True, default="#0f172a")
    sections = Column(JSONB, nullable=False, default=dict)
    contact = Column(JSONB, nullable=False, default=dict)
    address = Column(Text, nullable=True)
    hours = Column(JSONB, nullable=True)
    is_published = Column(Boolean, nullable=False, default=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

