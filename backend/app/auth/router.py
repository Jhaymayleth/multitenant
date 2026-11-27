"""Rutas de API para autenticación y control de sesión."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.auth.schemas import (
    ForgotPasswordRequest,
    LoginRequest,
    ResetPasswordRequest,
    SwitchTenantRequest,
    TenantBrief,
    TokenResponse,
    UserMeResponse,
)
from app.auth.service import AuthService
from app.core.config import Settings
from app.core.database import get_db
from app.core.dependencies import CurrentUser, get_current_user, permissions_for_role
from app.core.errors import AppError
from app.platform.models import Tenant, User
from app.shared.schemas import MessageResponse

router = APIRouter(prefix="/auth", tags=["Auth & Session"])
settings = Settings()


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="lixus_session",
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure or settings.app_env == "production",
        max_age=settings.jwt_access_token_ttl_minutes * 60,
    )


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión y emitir cookie httpOnly")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    service = AuthService(db)
    auth_result = service.authenticate_user(data.email, data.password, data.tenant_slug)
    if not auth_result:
        # Mensaje genérico: no revela si el correo existe (RN-111).
        raise AppError(
            code="INVALID_CREDENTIALS",
            message="No pudimos iniciar sesión. Revisa tus datos.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    user, tenant_id, role = auth_result
    token = service.generate_session_token(user, tenant_id=tenant_id, role=role)
    _set_session_cookie(response, token)
    return TokenResponse(expires_in_minutes=settings.jwt_access_token_ttl_minutes)


@router.post("/logout", response_model=MessageResponse, summary="Cerrar sesión")
def logout(response: Response):
    response.delete_cookie("lixus_session")
    return MessageResponse(message="Sesión cerrada correctamente")


@router.get("/me", response_model=UserMeResponse, summary="Obtener usuario, tenant y rol")
def get_me(
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_id = uuid.UUID(user.id)
    except (ValueError, AttributeError):
        raise AppError(code="INVALID_TOKEN", message="Sesión no válida.", status_code=401)

    account = db.get(User, user_id)
    if not account or account.status != "active":
        raise AppError(code="INVALID_TOKEN", message="Sesión no válida.", status_code=401)

    tenant: Tenant | None = None
    if user.tenant_id:
        try:
            tenant = db.get(Tenant, uuid.UUID(user.tenant_id))
        except (ValueError, AttributeError):
            tenant = None

    return UserMeResponse(
        id=account.id,
        email=account.email,
        full_name=account.full_name,
        active_tenant_id=tenant.id if tenant else None,
        active_tenant=TenantBrief(
            id=tenant.id,
            slug=tenant.slug,
            name=tenant.name,
            status=tenant.status,
        ) if tenant else None,
        role=user.role,
        permissions=permissions_for_role(user.role),
    )


@router.post("/switch-tenant", response_model=TokenResponse, summary="Cambiar de restaurante y emitir token nuevo")
def switch_tenant(
    data: SwitchTenantRequest,
    response: Response,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user_id = uuid.UUID(user.id)
    except (ValueError, AttributeError):
        raise AppError(code="INVALID_TOKEN", message="Sesión no válida.", status_code=401)

    service = AuthService(db)
    account, tenant_id, role = service.resolve_switch_tenant(user_id, data.tenant_id)
    token = service.generate_session_token(account, tenant_id=tenant_id, role=role)
    _set_session_cookie(response, token)
    return TokenResponse(expires_in_minutes=settings.jwt_access_token_ttl_minutes)


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Solicitar código de recuperación",
)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    AuthService(db).request_password_reset(data.email)
    return MessageResponse(message="Si la cuenta existe, enviamos un código de recuperación.")


@router.post("/reset-password", response_model=MessageResponse, summary="Restablecer contraseña con código")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    AuthService(db).reset_password(data.code, data.new_password)
    return MessageResponse(message="Contraseña actualizada. Ya puedes iniciar sesión.")
