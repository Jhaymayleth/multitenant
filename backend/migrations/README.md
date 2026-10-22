# Migraciones de Base de Datos Multitenant (Lixus)

Basado en:
- `docs/03-ARQUITECTURA.md` (Sección 2.6: Migraciones multi-schema)
- `docs/07-MODELO-DATOS.md`

## Estrategia de Dos Cadenas

1. **`platform/`**:
   - Cadena de migración para el schema global `platform`.
   - Controla: `users`, `tenants`, `tenant_memberships`, `plans`, `subscriptions`, `tenant_verifications`, `audit_log`, `idempotency_keys`.
   - Tabla de versión: `platform.alembic_version`.

2. **`tenant/`**:
   - Cadena de migración para los schemas de cada restaurante (`tenant_<id>`).
   - Controla: `restaurant_tables`, `table_sessions`, `service_requests`, `menu_categories`, `menu_products`, `orders`, `order_items`, `reservations`, `payments`, `receipts`, `tenant_settings`, `staff_profiles`.
   - Cada schema nuevo aplica esta cadena al aprovisionarse.
   - Tabla de versión: `alembic_version` dentro de cada schema (`version_table_schema = schema_name`).

