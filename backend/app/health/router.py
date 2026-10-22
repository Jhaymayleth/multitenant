"""Endpoint de estado de salud del backend para Docker y Kubernetes."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import Settings

settings = Settings()

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str = "ok"
    app: str
    version: str
    environment: str


@router.get("/health", response_model=HealthResponse, summary="Verificar estado operativo del backend")
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )

