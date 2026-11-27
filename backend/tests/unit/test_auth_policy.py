"""Pruebas unitarias de la política de autenticación aprobada."""

import pytest
from pydantic import ValidationError

from app.auth.schemas import LoginRequest, ResetPasswordRequest
from app.core.dependencies import permissions_for_role
from app.core.security import hash_password, verify_password


def test_password_hash_roundtrip():
    hashed = hash_password("clave-segura-123")
    assert hashed != "clave-segura-123"
    assert verify_password("clave-segura-123", hashed)
    assert not verify_password("otra-clave", hashed)


def test_minimum_password_length_is_eight():
    LoginRequest(email="usuario@example.com", password="12345678")
    with pytest.raises(ValidationError):
        LoginRequest(email="usuario@example.com", password="1234567")
    with pytest.raises(ValidationError):
        ResetPasswordRequest(code="x" * 24, new_password="1234567")


def test_permissions_follow_approved_roles():
    owner = permissions_for_role("owner")
    admin = permissions_for_role("admin")
    cook = permissions_for_role("cook")
    waiter = permissions_for_role("waiter")

    assert "site:publish" in owner
    assert "site:publish" not in admin
    assert "kitchen:write" in cook
    assert "tables:write" in waiter
    assert permissions_for_role("cashier") == []
