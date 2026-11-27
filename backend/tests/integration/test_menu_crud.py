"""Prueba de integración del CRUD y la publicación del menú (BL-03)."""

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.platform.models import Tenant, TenantMembership, User

PASSWORD = "clave-prueba-123"


def _provision(client: TestClient, slug: str) -> dict:
    response = client.post(
        "/api/v1/platform/tenants",
        json={
            "name": f"Restaurante {slug}",
            "slug": slug,
            "contact_email": f"{slug}@example.com",
            "owner_full_name": "Dueño de prueba",
            "owner_email": f"owner-{slug}@example.com",
            "owner_password": PASSWORD,
        },
        headers={"Idempotency-Key": f"menu-{slug}"},
    )
    assert response.status_code == 201, response.text
    return response.json()


def _activate_owner(db: Session, tenant_id: str, slug: str) -> str:
    user_id = uuid.uuid4()
    email = f"menu-{slug}-{user_id.hex[:6]}@example.com"
    db.add(User(id=user_id, email=email, password_hash=hash_password(PASSWORD), full_name="Dueño", status="active"))
    db.add(TenantMembership(id=uuid.uuid4(), tenant_id=uuid.UUID(tenant_id), user_id=user_id, role="owner", status="active"))
    tenant = db.get(Tenant, uuid.UUID(tenant_id))
    if tenant:
        tenant.status = "active"
    db.commit()
    return email


@pytest.mark.integration
def test_menu_crud_and_publication(client: TestClient):
    slug = f"menu{uuid.uuid4().hex[:6]}"
    tenant = _provision(client, slug)

    db = SessionLocal()
    try:
        email = _activate_owner(db, tenant["id"], slug)
    finally:
        db.close()

    login = client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD, "tenant_slug": slug})
    assert login.status_code == 200, login.text
    cookies = {"lixus_session": login.cookies["lixus_session"]}

    category = client.post(
        "/api/v1/tenant/menu/categories",
        json={"name": "Bebidas", "display_order": 0},
        cookies=cookies,
    )
    assert category.status_code == 201, category.text
    category_id = category.json()["id"]

    product = client.post(
        "/api/v1/tenant/menu/products",
        json={"category_id": category_id, "name": "Café", "price_cents": 1500, "is_published": False},
        cookies=cookies,
    )
    assert product.status_code == 201, product.text
    product_id = product.json()["id"]

    public_before = client.get(f"/api/v1/public/{slug}/menu")
    assert public_before.status_code == 200
    assert all(item["id"] != product_id for item in public_before.json())

    published = client.patch(
        f"/api/v1/tenant/menu/products/{product_id}/publication",
        json={"is_published": True},
        cookies=cookies,
    )
    assert published.status_code == 200, published.text

    public_after = client.get(f"/api/v1/public/{slug}/menu")
    assert any(item["id"] == product_id for item in public_after.json())

    in_use = client.delete(f"/api/v1/tenant/menu/categories/{category_id}", cookies=cookies)
    assert in_use.status_code == 409
    assert in_use.json()["error"]["code"] == "CATEGORY_IN_USE"

    removed = client.delete(f"/api/v1/tenant/menu/products/{product_id}", cookies=cookies)
    assert removed.status_code == 204
    deleted_category = client.delete(f"/api/v1/tenant/menu/categories/{category_id}", cookies=cookies)
    assert deleted_category.status_code == 204
