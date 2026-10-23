"""Seguridad del backend.

Basado en:
- docs/04-MODULOS.md (Sección 4: Autenticación y sesión)
- docs/08-SEGURIDAD-Y-ACCESO.md
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from app.core.config import Settings

settings = Settings()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def constant_time_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def sha256_hex(data: str) -> str:
    if not isinstance(data, str):
        data = str(data)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def random_hex(bytes_: int = 16) -> str:
    return secrets.token_hex(bytes_)


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    now = datetime.now(UTC)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.jwt_access_token_ttl_minutes)

    to_encode.update({
        "exp": expire,
        "iat": now,
        "iss": "lixus-api",
    })
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            issuer="lixus-api",
        )
        return payload
    except jwt.PyJWTError:
        return None
