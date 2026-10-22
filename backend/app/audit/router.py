"""Rutas de API para consulta de eventos de auditoría."""

from __future__ import annotations

from typing import Sequence
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit.models import AuditLog
from app.audit.schemas import AuditLogResponse
from app.core.database import get_db

router = APIRouter(prefix="/audit", tags=["Platform Audit"])


@router.get("", response_model=list[AuditLogResponse], summary="Consultar log de auditoría global")
def list_audit_events(limit: int = 50, db: Session = Depends(get_db)):
    stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    return db.execute(stmt).scalars().all()

