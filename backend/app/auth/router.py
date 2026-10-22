"""Rutas de API para autenticación y control de sesión.

Basado en docs/04-MODULOS.md (Sección 4).
"""

from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest, SwitchTenantRequest, TokenResponse, UserMeResponse
from app.auth.service import AuthService
from app.core.database import get_db
from app.core.dependencies import CurrentUser, get_current_user
from app.shared.schemas import MessageResponse

router = APIRouter(prefix="/auth", tags=["Auth & Session"])


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión y emitir cookie httpOnly")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.authenticate_user(data.email, data.password)
    if not user:
        # Mensaje genérico para no filtrar existencia de correos (docs/04-MODULOS.md)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    token = service.generate_session_token(user)

    # Configuración de cookie HttpOnly segura
    response.set_cookie(
        key="lixus_session",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # En producción: True
        max_age=3600,
    )

    return TokenResponse(expires_in_minutes=60)


@router.post("/logout", response_model=MessageResponse, summary="Cerrar sesión")
def logout(response: Response):
    response.delete_cookie("lixus_session")
    return MessageResponse(message="Sesión cerrada correctamente")


@router.get("/me", response_model=UserMeResponse, summary="Obtener usuario actual y tenant activo")
def get_me(user: CurrentUser = Depends(get_current_user)):
    return UserMeResponse(
        id=uuid.UUID(user.id),
        email=user.email,
        full_name="Usuario Autenticado",
        active_tenant_id=uuid.UUID(user.tenant_id) if user.tenant_id else None,
        role=user.role,
    )


@router.post("/switch-tenant", response_model=TokenResponse, summary="Cambiar de restaurante y emitir token nuevo")
def switch_tenant(
    data: SwitchTenantRequest,
    response: Response,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Esqueleto de cambio de tenant
    return TokenResponse(expires_in_minutes=60)

