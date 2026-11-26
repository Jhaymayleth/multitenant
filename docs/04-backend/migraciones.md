# Migraciones

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Cadenas

| Cadena | Ruta | Alcance |
|---|---|---|
| Plataforma | `backend/migrations/platform` | Schema `platform` |
| Tenant | `backend/migrations/tenant` | Un schema `tenant_<id>` |

Cada cadena tiene su `alembic.ini` y su `env.py`.

## 2. Comandos

### Plataforma

```bash
cd backend
python -m alembic -c migrations/platform/alembic.ini upgrade head
```

### Tenant

```bash
cd backend
python -m alembic -c migrations/tenant/alembic.ini -x schema=tenant_<id> upgrade head
```

## 3. Aprovisionamiento

El servicio de plataforma ejecuta la cadena del tenant después de `CREATE SCHEMA`. Si la migración falla, el tenant queda en `provisioning_failed` y no se activa.

## 4. Nueva migración de tenant

1. Crear la revisión en la cadena de tenant.
2. Probarla en un schema limpio.
3. Probarla en un schema con datos.
4. Definir el orden de aplicación a los tenants existentes.
5. Documentar el impacto y el rollback.
6. Ejecutar en producción con backup previo.

## 5. Rollback

- `alembic downgrade` debe dejar el schema en el estado anterior.
- La migración inicial del tenant tiene un downgrade incorrecto conocido: crea `alembic_version` en vez de eliminarla.
- No se hace rollback en producción sin backup y ventana.

## 6. Reglas

1. Una migración no borra datos sin decisión explícita.
2. Los cambios de estado usan `CHECK`, no `ENUM`.
3. Las migraciones son idempotentes cuando sea posible.
4. No se edita una migración ya aplicada en producción.
5. Toda migración nueva actualiza `03-arquitectura/modelo-de-datos.md`.

## 7. Riesgos

| Riesgo | Control |
|---|---|
| Migración aplicada a un tenant y no a otro | Registro por tenant y verificación |
| Bloqueo de tabla en hora pico | Ventana y migración en pasos |
| Pérdida de datos | Backup y prueba de restauración |
| Deriva entre cadenas | Revisión en CI |
