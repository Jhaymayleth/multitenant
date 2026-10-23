"""Dependencias de FastAPI para inyección de contexto multitenant y seguridad.

Basado en:
- docs/03-ARQUITECTURA.md (Sección 2.4: Dependencia tenant_context)
- docs/08-SEGURIDAD-Y-ACCESO.md
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

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

    import uuid as _uuid

    from sqlalchemy import select

    from app.platform.models import Tenant, TenantMembership

    try:
        user_uuid = _uuid.UUID(user.id)
        tenant_uuid = _uuid.UUID(user.tenant_id)
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Identificador de usuario o tenant inválido",
        )

    # Resolver el tenant y la membresía activa desde la base de datos (autoritativo)
    tenant = db.execute(
        select(Tenant).where(Tenant.id == tenant_uuid, Tenant.status == "active")
    ).scalar_one_or_none()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Restaurante no encontrado o inactivo",
        )

    membership = db.execute(
        select(TenantMembership).where(
            TenantMembership.tenant_id == tenant.id,
            TenantMembership.user_id == user_uuid,
            TenantMembership.status == "active",
        )
    ).scalar_one_or_none()
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene una membresía activa en este restaurante",
        )

    schema_name = tenant.schema_name
    if not SAFE_SCHEMA_REGEX.match(schema_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Identificador de schema de tenant inválido",
        )

    # Configurar el search_path local a la transacción y recordarlo para transacciones futuras
    db.info["tenant_schema"] = schema_name
    set_tenant_schema(db, schema_name)

    return TenantContext(
        tenant_id=str(tenant.id),
        schema_name=schema_name,
        role=membership.role,
        user_id=str(user_uuid),
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

