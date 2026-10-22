"""Esquemas Pydantic para eventos de auditoría."""

from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    actor_user_id: uuid.UUID | None = None
    actor_kind: str
    tenant_id: uuid.UUID | None = None
    action: str
    entity_type: str | None = None
    entity_id: uuid.UUID | None = None
    ip: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

