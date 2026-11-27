"""Prueba de integración del código de recuperación (D-153)."""

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.auth.service import AuthService
from app.core.database import SessionLocal
from app.core.security import hash_password, verify_password
from app.platform.models import TenantMembership, User, VerificationCode


class CapturingEmailProvider:
    def __init__(self) -> None:
        self.code: str | None = None
        self.email: str | None = None

    def send_password_reset(self, email: str, code: str) -> None:
        self.email = email
        self.code = code


@pytest.mark.integration
def test_reset_password_consumes_single_use_code(client: TestClient, monkeypatch):
    provider = CapturingEmailProvider()
    monkeypatch.setattr("app.auth.service.get_email_provider", lambda settings=None: provider)

    user_id = uuid.uuid4()
    email = f"reset-{user_id.hex[:8]}@example.com"
    db = SessionLocal()
    try:
        db.add(User(id=user_id, email=email, password_hash=hash_password("clave-inicial-1"), full_name="Prueba", status="active"))
        db.commit()

        AuthService(db).request_password_reset(email)
        assert provider.code is not None
        assert provider.email == email

        code_row = db.execute(
            select(VerificationCode).where(VerificationCode.user_id == user_id, VerificationCode.purpose == "password_reset")
        ).scalar_one()
        assert code_row.consumed_at is None

        response = client.post("/api/v1/auth/reset-password", json={"code": provider.code, "new_password": "clave-nueva-123"})
        assert response.status_code == 200, response.text

        db.refresh(code_row)
        assert code_row.consumed_at is not None
        user = db.get(User, user_id)
        assert verify_password("clave-nueva-123", user.password_hash)

        reused = client.post("/api/v1/auth/reset-password", json={"code": provider.code, "new_password": "otra-clave-1234"})
        assert reused.status_code == 400
    finally:
        db.rollback()
        db.execute(select(VerificationCode).where(VerificationCode.user_id == user_id)).delete()
        db.execute(select(TenantMembership).where(TenantMembership.user_id == user_id)).delete()
        user = db.get(User, user_id)
        if user:
            db.delete(user)
        db.commit()
        db.close()
