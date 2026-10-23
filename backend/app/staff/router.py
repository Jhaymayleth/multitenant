"""Rutas de API para personal en el restaurante."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import TenantContext, require_role
from app.staff.models import StaffProfile
from app.staff.schemas import StaffCreateRequest, StaffProfileResponse

router = APIRouter(prefix="/tenant/staff", tags=["Tenant Staff"])


@router.get("", response_model=list[StaffProfileResponse], summary="Listar personal del restaurante")
def list_staff(
    context: TenantContext = Depends(require_role("owner", "admin")),
    db: Session = Depends(get_db),
):
    stmt = select(StaffProfile).order_by(StaffProfile.full_name.asc())
    return db.execute(stmt).scalars().all()


@router.post(
    "",
    response_model=StaffProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Pre-registrar empleado con rol e invitación (CEO)",
)
def create_staff(
    data: StaffCreateRequest,
    context: TenantContext = Depends(require_role("owner")),
    db: Session = Depends(get_db),
):
    profile = StaffProfile(
        user_id=uuid.uuid4(),  # En implementación real: busca o crea en platform.users
        full_name=data.full_name,
        phone=data.phone,
        position=data.position,
        status="active",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

