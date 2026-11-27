# Modelo de datos

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Principios

1. Dos tipos de schema: `platform` y `tenant_<id>`.
2. Sin `tenant_id` dentro del schema del tenant.
3. Identidad global en `platform.users`; perfil local en el schema del tenant.
4. Estados como texto con `CHECK`, no `ENUM` de PostgreSQL.
5. Dinero en enteros (`*_cents`) con moneda ISO 4217 en la configuración del tenant.
6. Fechas `timestamptz`; zona horaria del restaurante en su configuración.
7. Borrado lógico en catálogo y personas; pedidos y pagos no se borran físicamente.
8. Snapshot de nombre y precio en las líneas de pedido.
9. UUID como clave primaria, salvo tablas de log que usan `bigserial`.

## 2. Schema `platform`

| Tabla | Propósito |
|---|---|
| `users` | Identidad global de cualquier persona con cuenta |
| `tenants` | Restaurantes, slug, schema, estado y contacto |
| `tenant_memberships` | Relación usuario–tenant con rol y estado |
| `platform_admins` | Rol global Lixus (previsto) |
| `plans` | Catálogo de planes y capacidades |
| `subscriptions` | Suscripción comercial del tenant |
| `subscription_invoices` | Facturas de suscripción |
| `tenant_verifications` | Verificación del negocio |
| `verification_codes` | Códigos de un solo uso |
| `idempotency_keys` | Claves globales con TTL |
| `audit_log` | Auditoría de acciones de plataforma |

## 3. Schema del tenant

| Tabla | Propósito |
|---|---|
| `tenant_settings` | Configuración pública, marca, zonas de domicilio y tarifa (singleton) |
| `staff_profiles` | Perfil local del empleado |
| `customers` | Clientes registrados del restaurante |
| `menu_categories` | Categorías del menú |
| `menu_products` | Productos con precio, imagen y publicación |
| `restaurant_tables` | Mesas, zona y estado |
| `table_sessions` | Sesión anónima por mesa y QR |
| `service_requests` | Solicitudes del cliente desde la mesa |
| `orders` | Cabecera del pedido |
| `order_items` | Líneas con snapshot de nombre y precio |
| `reservations` | Reservas con fecha, mesa y estado |
| `payments` | Pagos registrados |
| `payment_events` | Eventos de proveedor o webhook |
| `receipts` | Comprobantes con token temporal |
| `ai_usage` | Consumo de IA por tenant (previsto) |
| `idempotency_keys` | Claves locales del tenant |

## 4. Relaciones principales

- `tenants` 1–N `tenant_memberships` N–1 `users`.
- `tenants` 1–N `subscriptions` N–1 `plans`.
- `menu_categories` 1–N `menu_products`.
- `restaurant_tables` 1–N `table_sessions` 1–N `service_requests`.
- `orders` 1–N `order_items`.
- `orders` 1–N `payments` 1–N `payment_events`.
- `payments` 1–1 `receipts`.
- `restaurant_tables` 1–N `reservations`.

## 5. Reglas de integridad

- Un pedido no se borra; cambia de estado.
- Un pago confirmado no se edita; se corrige con otro evento.
- Una mesa tiene una sola sesión activa.
- Una reserva no se solapa con otra en la misma mesa y franja.
- El total del pedido se calcula en el servidor a partir de las líneas.
- El comprobante usa numeración por tenant y token temporal.

## 6. Migraciones y seeds

- Dos cadenas Alembic independientes.
- La cadena de tenant se ejecuta por schema.
- Los seeds de planes y datos demo están pendientes.
- Toda migración debe probarse en un schema limpio y en uno existente.

## 7. Pendientes del modelo

- RLS y rol de aplicación con privilegios mínimos.
- Restricción de exclusión para reservas.
- Índices de búsqueda y paginación.
- Campos de publicación y orden del menú.
- Modelo de suscripción y facturación.
- Multi-sucursal (fuera de la versión inicial).

Ver `04-backend/datos.md` para el detalle de implementación.
