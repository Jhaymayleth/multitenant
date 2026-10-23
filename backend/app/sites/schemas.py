"""Esquemas Pydantic para configuración del sitio web del restaurante."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SiteSettingsUpdate(BaseModel):
    display_name: str = Field(..., min_length=2, max_length=255)
    tagline: str | None = None
    description: str | None = None
    color_primary: str | None = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    color_secondary: str | None = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    address: str | None = None
    hours: dict | None = None


class SiteSettingsResponse(BaseModel):
    display_name: str
    tagline: str | None = None
    description: str | None = None
    logo_url: str | None = None
    hero_image_url: str | None = None
    color_primary: str | None = None
    color_secondary: str | None = None
    address: str | None = None
    hours: dict | None = None
    is_published: bool
    updated_at: datetime

    model_config = {"from_attributes": True}

