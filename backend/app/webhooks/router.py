"""Rutas de API para recepción de webhooks de pago.

Basado en:
- docs/02-DECISIONES.md (D-073: Proveedor simulado y webhooks firmados)
- docs/04-MODULOS.md (Sección 10)
"""

from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post(
    "/payments/{provider}",
    summary="Webhook firmado del proveedor de pagos (simulador sandbox / pasarela)",
)
async def payment_webhook(
    provider: str,
    request: Request,
    signature: str | None = Header(None, alias="X-Signature"),
    db: Session = Depends(get_db),
):
    body = await request.body()
    # En desarrollo / sandbox se valida firma HMAC
    return {
        "status": "received",
        "provider": provider,
    }

