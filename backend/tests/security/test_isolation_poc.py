"""Esqueleto de pruebas de aislamiento multitenant obligatorias (PoC).

Basado en docs/03-ARQUITECTURA.md (Sección 6: Pruebas de arquitectura obligatorias).
Casos a validar:
1. Un usuario del tenant A intenta acceder a recursos del tenant B -> 403 o 404.
2. Inyección o manipulación de schema_name o tenant_id -> la API lo rechaza.
3. El search_path no se filtra entre peticiones concurrentes en el connection pool.
"""

def test_tenant_context_requires_authentication(client):
    # Intentar acceder a endpoints del tenant sin sesión debe responder 401
    response = client.get("/api/v1/tenant/menu/products")
    assert response.status_code == 401

