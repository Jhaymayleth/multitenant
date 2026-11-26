# Multitenancy

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería
**Decisiones:** D-103, D-106

## 1. Modelo de aislamiento

Cada restaurante es un tenant con un schema propio:

- `platform`: datos globales del SaaS.
- `tenant_<12 hex>`: datos del restaurante.

No hay columna `tenant_id` dentro de las tablas del tenant. El schema es el límite.

## 2. Nombres de schema

- Generados en el servidor con `secrets.token_hex(6)`.
- Formato validado: `tenant_[a-f0-9]{12}`.
- Nunca se acepta un nombre de schema enviado por el cliente.
- Se valida antes de cualquier `SET search_path` o DDL.

## 3. Aprovisionamiento

1. Validar slug único y datos del restaurante.
2. Insertar el tenant en estado `provisioning`.
3. `CREATE SCHEMA`.
4. Aplicar la cadena Alembic del tenant.
5. Crear el usuario CEO y la membresía `owner`.
6. Crear `tenant_settings` inicial.
7. Otorgar permisos al rol de aplicación.
8. Cambiar el estado a `pending_verification`.
9. Lixus verifica y activa.

El alta es idempotente con `Idempotency-Key` en el alcance `platform:create_tenant`.

## 4. Resolución del tenant

- En rutas privadas: desde el JWT y la membresía, revalidando en base de datos.
- En rutas públicas: desde el slug de la URL.
- En ningún caso desde un header `X-Tenant` ni desde el body.

Si el tenant no está activo o la membresía no existe, la petición se rechaza.

## 5. `search_path`

Cada transacción fija el schema con `set_config('search_path', :schema, true)` y un listener `after_begin` lo reaplica tras cada commit. Esto evita que una conexión del pool conserve el schema de otro tenant.

Regla: ninguna consulta de tenant se ejecuta sin `search_path` fijado en la transacción.

## 6. Migraciones

- `backend/migrations/platform`: schema global.
- `backend/migrations/tenant`: se aplica a cada schema de tenant con `-x schema=...`.

Una migración nueva del tenant debe poder aplicarse a todos los tenants existentes sin intervención manual. El procedimiento está en `04-backend/migraciones.md`.

## 7. Roles de base de datos

- La aplicación debe conectarse con un rol de privilegios mínimos (`lixus_app`).
- El rol dueño se reserva para migraciones y tareas administrativas.
- RLS es una defensa adicional, no un sustituto del schema.

Estado actual: la aplicación conecta con el usuario dueño en algunos entornos. Es deuda P1.

## 8. Pruebas de aislamiento

Debe existir evidencia de:

1. Un usuario de A no puede leer datos de B cambiando la URL o el body.
2. Un token de A no abre una ruta de B.
3. El `search_path` no se filtra entre peticiones concurrentes.
4. Un schema inválido se rechaza antes de ejecutar SQL.
5. Una ruta pública solo devuelve el tenant del slug.

## 9. Límites conocidos

- No hay RLS activo.
- No hay `SET ROLE` por petición.
- La separación depende de que el código fije bien el `search_path`.
- El rol de aplicación aún tiene privilegios amplios.

Estos límites están en `07-calidad/deuda-tecnica.md` y deben cerrarse antes de escalar clientes.
