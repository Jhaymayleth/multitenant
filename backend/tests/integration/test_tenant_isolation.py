"""Pruebas de aislamiento multitenant entre dos tenants.

Requieren base de datos PostgreSQL disponible (ver CI).
"""

import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.platform.models import TenantMembership, User


PASSWORD = "devpass123"


def _provision_tenant(client: TestClient, slug: str) -> dict:
    response = client.post(
        "/api/v1/platform/tenants",
        json={
            "name": f"Restaurante {slug}",
            "slug": slug,
            "contact_email": f"{slug}@example.com",
            "owner_full_name": f"Owner {slug}",
            "owner_email": f"owner-{slug}@example.com",
        },
        headers={"Idempotency-Key": f"iso-{slug}"},
    )
    assert response.status_code == 201, response.text
    return response.json()


def _create_user_for_tenant(tenant_id: str, slug: str) -> tuple[str, str]:
    db = SessionLocal()
    try:
        user_id = uuid.uuid4()
        email = f"iso-{slug}-{user_id}@example.com"
        db.add(
            User(
                id=user_id,
                email=email,
                password_hash=hash_password(PASSWORD),
                full_name=f"User {slug}",
                status="active",
            )
        )
        db.add(
            TenantMembership(
                id=uuid.uuid4(),
                tenant_id=uuid.UUID(tenant_id),
                user_id=user_id,
                role="owner",
                status="active",
            )
        )
        from app.platform.models import Tenant
        tenant = db.get(Tenant, uuid.UUID(tenant_id))
        if tenant is not None:
            tenant.status = "active"
        db.commit()
        return str(user_id), email
    finally:
        db.close()


def _login(client: TestClient, email: str, slug: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": PASSWORD, "tenant_slug": slug},
    )
    assert response.status_code == 200, response.text
    return response.cookies["lixus_session"]


@pytest.mark.integration
def test_products_are_isolated_between_tenants(client: TestClient):
    slug_a = f"isoa{uuid.uuid4().hex[:6]}"
    slug_b = f"isob{uuid.uuid4().hex[:6]}"

    tenant_a = _provision_tenant(client, slug_a)
    tenant_b = _provision_tenant(client, slug_b)

    _, email_a = _create_user_for_tenant(tenant_a["id"], slug_a)
    _, email_b = _create_user_for_tenant(tenant_b["id"], slug_b)

    cookie_a = _login(client, email_a, slug_a)
    cookie_b = _login(client, email_b, slug_b)

    # Crear categoría y producto en tenant A
    cat_resp = client.post(
        "/api/v1/tenant/menu/categories",
        json={"name": "CatA", "display_order": 0},
        cookies={"lixus_session": cookie_a},
    )
    assert cat_resp.status_code == 201
    cat_id = cat_resp.json()["id"]

    prod_resp = client.post(
        "/api/v1/tenant/menu/products",
        json={"category_id": cat_id, "name": "ProductoA", "price_cents": 1000},
        cookies={"lixus_session": cookie_a},
    )
    assert prod_resp.status_code == 201

    # Tenant B no debe ver el producto de A
    list_b = client.get(
        "/api/v1/tenant/menu/products",
        cookies={"lixus_session": cookie_b},
    )
    assert list_b.status_code == 200
    names_b = [p["name"] for p in list_b.json()]
    assert "ProductoA" not in names_b

    # Tenant A sí lo ve
    list_a = client.get(
        "/api/v1/tenant/menu/products",
        cookies={"lixus_session": cookie_a},
    )
    assert list_a.status_code == 200
    names_a = [p["name"] for p in list_a.json()]
    assert "ProductoA" in names_a


@pytest.mark.integration
def test_cross_tenant_login_is_rejected(client: TestClient):
    slug_a = f"crossa{uuid.uuid4().hex[:6]}"
    slug_b = f"crossb{uuid.uuid4().hex[:6]}"

    tenant_a = _provision_tenant(client, slug_a)
    _provision_tenant(client, slug_b)

    _, email_a = _create_user_for_tenant(tenant_a["id"], slug_a)

    # Usuario de A intenta entrar a B -> 401
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email_a, "password": PASSWORD, "tenant_slug": slug_b},
    )
    assert response.status_code == 401
