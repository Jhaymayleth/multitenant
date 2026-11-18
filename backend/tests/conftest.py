"""Configuración global de fixtures para pytest."""

import os

import pytest

# La clave debe existir antes de importar la app (Settings se lee al cargar).
os.environ.setdefault("PLATFORM_ADMIN_KEY", "test-platform-admin-key")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

ADMIN_HEADERS = {"X-Platform-Admin-Key": os.environ["PLATFORM_ADMIN_KEY"]}


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        test_client.headers.update(ADMIN_HEADERS)
        yield test_client

