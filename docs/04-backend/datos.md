# Datos y persistencia

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Motores y roles

- PostgreSQL 16.
- SQLAlchemy como ORM.
- Alembic para migraciones.
- Redis para límites, sesión y caché.
- R2 para archivos (previsto).

## 2. Separación

- `platform`: datos globales.
- `tenant_<id>`: datos del restaurante.
- Sin `tenant_id` en tablas del tenant.
- Toda consulta privada fija `search_path` en la transacción.

## 3. Transacciones

- Una petición, una transacción lógica.
- `set_config('search_path', ..., true)` al inicio.
- Listener `after_begin` para reaplicar tras commit.
- No se deja una conexión del pool con el schema de un tenant.

## 4. Dinero

- Enteros en centavos.
- Moneda ISO 4217 en `tenant_settings` o en el tenant.
- El total se calcula en el servidor.
- El precio del producto se congela en la línea del pedido.
- No se usan floats.

## 5. Fechas

- `timestamptz` en base de datos.
- Zona horaria del restaurante en su configuración.
- Las reservas se interpretan en la zona del restaurante.
- Los reportes agrupan por la zona del restaurante, no por UTC.

## 6. Borrado

- Catálogo y personas: borrado lógico con `deleted_at`.
- Pedidos, pagos y comprobantes: no se borran físicamente.
- Un tenant desactivado conserva sus datos.
- La eliminación definitiva requiere proceso y contrato.

## 7. Integridad

- Claves foráneas dentro del schema del tenant.
- `CHECK` para estados.
- Índices por claves de búsqueda: slug, email, token, fecha.
- Restricción de exclusión para reservas (pendiente).
- Una sola sesión activa por mesa (pendiente).

## 8. Idempotencia

- Tabla global y tabla por tenant.
- Clave, alcance, hash del cuerpo, estado, respuesta y expiración.
- TTL propuesto: 24 horas.
- Limpieza periódica.

## 9. Seeds

- Planes base.
- Tenant demo para pruebas.
- Datos de menú y mesas de ejemplo.
- Estado: pendiente.

## 10. Riesgos

| Riesgo | Mitigación |
|---|---|
| Fuga de `search_path` en el pool | `SET LOCAL` + listener + prueba concurrente |
| Consulta sin tenant | Revisión de repositorios y pruebas negativas |
| Crecimiento de un schema | Índices y paginación |
| Migración fallida en un tenant | Prueba por schema y rollback documentado |
| Backup no restaurado | Prueba mensual de restauración |
