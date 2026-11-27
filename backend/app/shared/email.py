"""Envío de correo transaccional detrás de una interfaz.

El proveedor concreto sigue en PD-23. En local se usa un proveedor que
registra el código en el log para poder probar la recuperación; en otros
entornos no se envía nada hasta configurar un proveedor real.
"""

from __future__ import annotations

import logging
from typing import Protocol

from app.core.config import Settings

logger = logging.getLogger(__name__)


class EmailProvider(Protocol):
    def send_password_reset(self, email: str, code: str) -> None: ...


class LoggingEmailProvider:
    def send_password_reset(self, email: str, code: str) -> None:
        logger.warning("Código de recuperación para %s: %s", email, code)


class NoopEmailProvider:
    def send_password_reset(self, email: str, code: str) -> None:
        return None


def get_email_provider(settings: Settings | None = None) -> EmailProvider:
    current = settings or Settings()
    if current.app_env == "local":
        return LoggingEmailProvider()
    return NoopEmailProvider()
