"""Eventos y dispatcher interno del backend.

Aquí se define la infraestructura para eventos de dominio y auditoría.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ActorKind(StrEnum):
    USER = "user"
    PLATFORM_ADMIN = "platform_admin"
    SYSTEM = "system"
    AI = "ai"


@dataclass
class AuditEvent:
    actor_user_id: str | None = None
    actor_kind: ActorKind = ActorKind.SYSTEM
    tenant_id: str | None = None
    action: str = ""
    entity_type: str | None = None
    entity_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
