"""Dependencias de FastAPI para inyección de contexto multitenant y seguridad.

Basado en:
- docs/03-ARQUITECTURA.md (Sección 2.4: Dependencia tenant_context)
- docs/08-SEGURIDAD-Y-ACCESO.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Callable
from fastapi import Cookie, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import SAFE_SCHEMA_REGEX, get_db, set_tenant_schema
from app.core.security import decode_access_token


@dataclass
class CurrentUser:
    id: str
    email: str
    tenant_id: str | None = None
    role: str | None = None


@dataclass
class TenantContext:
    tenant_id: str
    schema_name: str
    role: str
    user_id: str


async def get_current_user(
    request: Request,
    lixus_session: Annotated[str | None, Cookie()] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    """Extrae y valida el usuario actual desde la cookie httpOnly o cabecera Authorization."""
    token = lixus_session
    if not token and authorization and authorization.startswith("Bearer "):
        token = authorization[7:]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o expirada",
        )

    user_id = payload.get("sub")
    email = payload.get("email", "")
    tenant_id = payload.get("tenant_id")
    role = payload.get("role")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sin identificador de usuario",
        )

    return CurrentUser(
        id=user_id,
        email=email,
        tenant_id=tenant_id,
        role=role,
    )


async def get_tenant_context(
    request: Request,
    user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> TenantContext:
    """Resuelve el contexto de tenant para la petición actual.
    
    Verifica que el usuario tenga un tenant_id y un schema_name válido,
    y fija el search_path local a la transacción.
    """
    if not user.tenant_id or not user.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene un restaurante activo seleccionado",
        )

    # El schema_name se resuelve en base de datos o se deriva del tenant_id
    # En producción / BD se lee de platform.tenants.schema_name
    # Para la estructura base validamos el patrón de seguridad:
    schema_name = getattr(user, "schema_name", None) or f"tenant_{user.tenant_id[:12]}"

    if not SAFE_SCHEMA_REGEX.match(schema_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Identificador de schema de tenant inválido",
        )

    # Configurar el search_path local a la transacción
    set_tenant_schema(db, schema_name)

    return TenantContext(
        tenant_id=user.tenant_id,
        schema_name=schema_name,
        role=user.role,
        user_id=user.id,
    )


def require_role(*allowed_roles: str) -> Callable:
    """Guard de roles que valida la autorización del usuario para la operación."""
    async def role_checker(
        context: Annotated[TenantContext, Depends(get_tenant_context)],
    ) -> TenantContext:
        if context.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado. Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}",
            )
        return context

    return role_checker

