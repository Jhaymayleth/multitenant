# Auditoría técnica — Lixus (SaaS multitenant para restaurantes)

**Fecha:** 2026-11-18
**Rama auditada:** `develop`
**Commit auditado:** `3eddc6d` — *ci: inicializar base antes de las pruebas y construir imágenes Docker* (2026-10-23; 15 commits en total)
**Alcance:** revisión estática de código, migraciones, documentación, Docker, CI y frontend. Sin modificaciones de código, sin instalación de dependencias, sin builds ni escrituras en base de datos.
**Fuentes normativas:** `Enunciado Proyecto Integrador SaaS Multitenant.pdf`, `docs/01-REQUERIMIENTOS.md`, `docs/09-ROBUSTEZ.md`, `docs/13-ROUTE-MVP.md`.

---

## 1. Resumen ejecutivo

Lixus tiene un **esqueleto arquitectónico correcto y bien documentado**: schema por tenant (`platform` + `tenant_<12hex>`), aprovisionamiento automático con Alembic, resolución autoritativa de tenant en el servidor, `search_path` con `SET LOCAL` por transacción, JWT en cookie `httpOnly` y un test de aislamiento entre dos tenants. Eso cubre la parte más valiosa del enunciado (25 puntos de multitenancy).

Sin embargo, **la entrega no está lista para sustentar como proyecto completo**:

- **Idempotencia y rate limiting, 30 puntos directos, no están implementados.** Solo existe idempotencia para crear tenant; pedidos y pagos reciben la cabecera y la ignoran. No hay ningún middleware, dependencia ni código de rate limiting (solo dos variables en `config.py`).
- **El flujo de alta de tenant queda en un callejón sin salida:** el CEO se crea con `password_hash=None`, el endpoint `/verify` es un esqueleto y el tenant nunca pasa a `active`; como `get_tenant_context` y las rutas públicas exigen `active`, **no se puede iniciar sesión ni operar un tenant recién creado por API**. El test de integración lo sortea activando el tenant por SQL directo.
- **El CRUD obligatorio está incompleto:** menú solo tiene `GET`/`POST` (sin update ni delete); pedidos no guardan líneas ni calculan el total (`total_cents=0`); no hay endpoint para cambiar estado de pedido.
- **El frontend es maqueta estática:** 0 llamadas a la API, login sin `onSubmit`, `/admin` sin guard, y no hay CSR ni SSR: todas las pantallas son contenido estático. RAC-09 (dos estrategias de renderizado) no se cumple.
- **Seguridad:** `/api/v1/platform/*` y `/api/v1/audit` son públicos. Cualquiera puede listar todos los tenants (incluido su `schema_name`), crear tenants (DDL + subprocess de Alembic) y leer la auditoría. Viola RN-03 del propio diseño.
- **Docker no cumple “un solo comando”:** el arranque no aplica migraciones de plataforma; el README obliga a ejecutar Alembic a mano (`README.md:267-271`).

**Juicio de cumplimiento de los 9 RAC evaluables en código:** 1 cumple (RAC-07), 5 parciales (RAC-01, RAC-02, RAC-03, RAC-06, RAC-08) y 3 no cumplen (RAC-04, RAC-05, RAC-09). RAC-10 (sustentación) no es verificable estáticamente.

---

## 2. Alcance exigido por el enunciado

| Bloque | Exigencia | Peso |
|---|---|---|
| Multitenancy | PostgreSQL, schema compartido + schema por tenant, creación automática, resolución por petición, aislamiento demostrable | 25 |
| Autenticación | Registro y login, JWT en cookie `httpOnly`, rutas protegidas backend/frontend, tenant resoluble desde el token | 15 |
| Idempotencia | ≥2 escrituras idempotentes con `Idempotency-Key`, resultado original en repetición, prueba de un solo registro, explicar almacenamiento y TTL | 15 |
| Rate limiting | Login y creaciones, 429 + `Retry-After`, estrategia justificada, ideal por usuario/tenant | 15 |
| Arquitectura | Organización, buenas prácticas, ORM y validación | 10 |
| Docker + CI/CD | `docker-compose.yml` funcional, `.env.example`, pipeline que falle ante lint/build/test | 10 |
| Documentación | README con nicho, arquitectura, arranque, resolución de tenant, idempotencia y rate limiting | 10 |
| Renderizado | Opción B: ≥2 estrategias (SSR/CSR/SSG) justificadas; Opción A: CSR | — |
| Opcionales | IA (+10), automatización n8n (+10), roles por tenant, pruebas de aislamiento, despliegue | — |

> Ambigüedad ya documentada: Next.js + FastAPI independiente no encaja literalmente en Opción A ni B (`docs/01-REQUERIMIENTOS.md:131`, pendiente P-01). Debe declararse al docente.

---

## 3. Arquitectura real y multi-tenancy

**Lo que sí está implementado y es verificable:**

- Schema global `platform` con usuarios, tenants, membresías, planes, suscripciones, verificaciones, claves de idempotencia y auditoría (`backend/app/platform/models.py:35-256`).
- Schema por tenant con 13 tablas de dominio creadas por la cadena Alembic de tenant (`backend/migrations/tenant/versions/d6a072ef02e3_initial_tenant_schema.py:24-190`).
- Nombre de schema generado en servidor con patrón estricto `tenant_[a-f0-9]{12}` y validación previa (`backend/app/platform/service.py:41-50`, `backend/app/core/database.py:23`).
- Resolución autoritativa: el JWT aporta `sub`/`tenant_id`, pero el backend **vuelve a consultar** tenant y membresía activos en base de datos (`backend/app/core/dependencies.py:111-139`).
- Aislamiento por transacción con `set_config('search_path', ..., true)` y listener `after_begin` para reaplicarlo tras cada commit (`backend/app/core/database.py:40-77`).
- Aprovisionamiento real: `CREATE SCHEMA`, migraciones del tenant, usuario CEO, membresía `owner`, `tenant_settings` y grants (`backend/app/platform/service.py:82-257`).
- Test de aislamiento entre dos tenants y login cruzado rechazado (`backend/tests/integration/test_tenant_isolation.py:76-139`).

**Límites del aislamiento:** no hay RLS ni `SET ROLE`; la aplicación conecta con el usuario dueño de la base (`DB_USER=lixus`, `docker-compose.yml:65-66`), no con `lixus_app` (`infra/docker/postgres/init/01-init.sql:21-22`). La separación depende exclusivamente de que el código fije bien `search_path`; una inyección SQL o un error de sesión podría cruzar schemas. Es aceptable para el enunciado, pero es el riesgo técnico principal.

---

## 4. Estado por módulo

| Módulo | Backend | Frontend | Estado | Evidencia |
|---|---|---|---|---|
| Plataforma / tenants | Crear, listar, detalle, planes. Verificación es esqueleto | Portal con contadores en 0 | 🟡 Parcial | `platform/router.py:25-99`; `platform/router.py:85-86` |
| Auth / sesión | Login/logout/me/switch. Sin registro ni recuperación | Formulario sin handler | 🟡 Parcial | `auth/router.py:22-74`; `login/page.tsx:19-41` |
| RBAC | `require_role` sobre membresía; roles `owner/admin/waiter/cashier/cook` | Sin uso | 🟡 Parcial | `dependencies.py:153-165`; `platform/models.py:96-100` |
| Menú | Listar/crear categorías y productos | Página informativa | 🟡 Parcial | `menus/router.py:22-76` |
| Mesas / QR | Listar/crear mesa con token; sesión QR no implementada | Página informativa | 🔴 Stub | `tables/router.py:16-37`; `public/router.py:72-74` |
| Pedidos | Crear/listar/detalle; sin líneas, total 0, sin cambio de estado | Página informativa | 🔴 Incompleto | `orders/service.py:19-30`; `orders/router.py:18-54` |
| Reservas | Crear/listar; sin solapamientos ni disponibilidad | Página informativa | 🔴 Incompleto | `reservations/service.py:17-31` |
| Pagos / comprobantes | Registrar pago; confirmar no confirma; sin recibo | Página informativa | 🔴 Stub | `payments/router.py:34-48`; `public/router.py:96` |
| Sitio público | GET settings/menú por slug; publicación imposible | Menú/reservas estáticos | 🟡 Parcial | `public/router.py:43-65`; `sites/service.py:17-45` |
| Personal | Listar/pre-registrar con `uuid4` huérfano | Sin UI | 🔴 Stub | `staff/router.py:34-49` |
| Auditoría | Solo lectura global y sin auth; nada escribe | Sin UI | 🔴 Stub | `audit/router.py:16-19` |
| Webhooks | Recibe y responde sin validar firma | No aplica | 🔴 Stub | `webhooks/router.py:18-33` |
| Idempotencia | Solo alta de tenant; pedidos/pagos ignoran la clave | No aplica | 🔴 Incompleto | `platform/service.py:96-136`; `orders/service.py:17` |
| Rate limiting | Solo variables de configuración | No aplica | 🔴 Ausente | `core/config.py:69-70` |
| Migraciones / seeds | 2 cadenas Alembic; sin seeds | — | 🟡 Parcial | `backend/migrations/**`; no hay `seed*` |
| Docker | Compose con 4 servicios; sin migración al arrancar | Next en modo dev | 🟡 Parcial | `docker-compose.yml:48-96`; `backend/Dockerfile:22` |
| CI | Ruff + pytest; lint + build Next; build Docker | — | ✅ Implementado | `.github/workflows/ci.yml:47-103` |
| Pruebas | 4 tests (2 integración, 1 seguridad, 1 smoke) | 0 tests | 🔴 Insuficiente | `pytest --collect-only` |

---

## 5. Requisitos faltantes o incompletos vs enunciado

| ID | Requisito | Estado | Evidencia | Prioridad |
|---|---|---|---|---|
| RAC-01 | Schema por tenant + creación automática + aislamiento | 🟡 Implementado, flujo muerto | `platform/service.py:167-230`; activación inexistente `platform/router.py:85-86` | P0 |
| RAC-02 | Registro e inicio de sesión | 🔴 Sin registro; login inutilizable tras alta | No existe `/auth/register` (27 paths OpenAPI); `platform/service.py:184` | P0 |
| RAC-02 | Cookie `httpOnly` | ✅ | `auth/router.py:37-44` | — |
| RAC-02 | Rutas protegidas en frontend | 🔴 | `middleware.ts:35-56` solo inyecta cabeceras; `admin/layout.tsx:11-57` sin guard | P0 |
| RAC-03 | 2-3 entidades con CRUD completo | 🔴 Sin update/delete | `menus/router.py:22-76`; `orders/router.py:18-54` | P0 |
| RAC-03 | Validación backend | 🟡 Parcial | `menus/schemas.py:104-124`; pedidos aceptan `items` vacío y precio 0 (`orders/schemas.py:155-159`) | P1 |
| RAC-04 | ≥2 escrituras idempotentes | 🔴 Solo 1 | `platform/service.py:82`; `orders/service.py:17` ignora clave; `payments/router.py:26-31` no la pasa | P0 |
| RAC-04 | Repetición devuelve resultado original y detecta body distinto | 🟡 | `request_hash` se calcula y nunca se compara (`platform/service.py:99-115`) | P1 |
| RAC-04 | Almacenamiento/TTL explicados | ✅ Documentado, incompleto en código | `docs/09-ROBUSTEZ.md:50-118`; TTL no se filtra en consulta (`service.py:102-107`) | P2 |
| RAC-05 | Rate limiting login + creaciones, 429 + `Retry-After` | 🔴 Ausente | `core/config.py:69-70`; sin middleware en `main.py:20-52` | P0 |
| RAC-06 | `docker compose up` levanta todo | 🟡 Requiere migración manual | `backend/Dockerfile:22`; `README.md:267-271` | P1 |
| RAC-06 | `.env.example` sin secretos | ✅ | `.env.example`; `.env` ignorado y sin historial | — |
| RAC-07 | CI instala, lint/build y falla si algo está mal | ✅ | `.github/workflows/ci.yml:54-103` | — |
| RAC-08 | README con los 5 puntos | 🟡 Idempotencia/rate limiting no implementados | `README.md:276-290` los marca “Pendiente (Fase 4)” | P1 |
| RAC-09 | ≥2 estrategias de renderizado | 🔴 Solo contenido estático | 0 `use client`, 0 `fetch` en páginas; `grep` en `frontend/src` | P0 |
| RF-01 | CEO puede iniciar sesión tras alta | 🔴 | `platform/service.py:184` (`password_hash=None`); `TenantCreateRequest` sin contraseña (`platform/schemas.py:14-22`) | P0 |
| RF-01 | Verificación/activación de tenant | 🔴 Stub | `platform/router.py:76-86` devuelve el tenant sin cambios | P0 |
| RF-05 | Menú publicado vs no publicado | 🔴 Sin campo de publicación ni endpoint | `public/router.py:62-65` filtra solo `is_active` | P1 |
| RF-06 | Sesión QR, solicitudes y estados de mesa | 🔴 Stub | `public/router.py:72-86`; `tables/service.py:19-31` | P1 |
| RF-07 | Pedidos con líneas, snapshot, total en servidor, estados | 🔴 | `orders/service.py:19-30` (`total_cents=0`, no usa `items`) | P0 |
| RF-08 | Reservas sin solapamiento + disponibilidad | 🔴 | `reservations/service.py:1-31` (docstring promete validación que no existe) | P1 |
| RF-09 | Pago confirma, libera mesa y emite comprobante | 🔴 | `payments/router.py:44-48`; `public/router.py:89-96` | P1 |
| RF-10 | Publicar/despublicar sitio | 🔴 Imposible | `sites/schemas.py:10-17` no incluye `is_published`; `sites/service.py:32-41` no lo actualiza | P1 |
| RF-13 | Auditoría de acciones | 🔴 Sin escrituras | `audit/models.py:20`; `grep "AuditLog("` solo encuentra la clase | P1 |
| RN-03 | Un tenant no descubre a otros | 🔴 | `GET /api/v1/platform/tenants` público (`platform/router.py:46-52`) | P0 |

---

## 6. Errores, riesgos y deuda técnica

### 6.1 Bloqueantes funcionales

1. **El tenant nunca se activa.** `provision_tenant` termina en `pending_verification` (`platform/service.py:228`); `verify_tenant` no cambia estado (`platform/router.py:85-86`); `get_tenant_context` exige `status == "active"` (`dependencies.py:113`) y las rutas públicas también (`public/router.py:32`). El único camino de activación es SQL manual, como hace el test (`tests/integration/test_tenant_isolation.py:58-60`).
2. **El owner no tiene contraseña.** Se crea con `password_hash=None` (`platform/service.py:184`) y el request de alta no acepta contraseña (`platform/schemas.py:14-22`). `authenticate_user` rechaza usuarios sin hash (`auth/service.py:31-32`): el login del CEO es imposible.
3. **Pedidos sin contenido ni total.** El servicio crea la cabecera con `total_cents=0` y descarta `data.items` (`orders/service.py:19-30`), violando “el total se calcula en el servidor” y el snapshot de precios (RF-07, RN-12).
4. **Frontend desconectado.** `apiClient` existe (`frontend/src/lib/api.ts:18`) pero ninguna página lo usa; el botón de login es `type="button"` sin handler (`login/page.tsx:36-41`); `/admin` se sirve a cualquiera.

### 6.2 Bugs y comportamientos incorrectos

1. **`switch-tenant` no hace nada:** devuelve `TokenResponse` sin emitir token ni fijar cookie (`auth/router.py:66-74`).
2. **`/auth/me` miente:** `full_name` hardcodeado como “Usuario Autenticado” (`auth/router.py:60`).
3. **Logout sin revocación:** solo borra la cookie; el JWT sigue válido hasta expirar (`auth/router.py:49-52`; `core/security.py:48-64` no usa `jti` ni versión de token).
4. **Idempotencia no compara payload:** misma clave con body distinto devuelve el tenant original en vez de 409 (`platform/service.py:99-115`).
5. **Claves expiradas siguen vivas:** la consulta no filtra `expires_at` (`platform/service.py:102-107`), aunque la doc dice TTL de 24 h (`docs/09-ROBUSTEZ.md:116-118`).
6. **Fuga de `search_path` en el pool:** el aprovisionamiento usa `SET search_path TO "<schema>"` a nivel de sesión (`platform/service.py:201`) y solo lo restaura en el camino feliz (`platform/service.py:215`). Si falla entre ambos puntos, la conexión vuelve al pool apuntando al schema del tenant.
7. **Publicación imposible:** `tenant_settings.is_published` nace `False` (`platform/service.py:209`) y el update nunca lo cambia (`sites/service.py:32-41`), por lo que el sitio público siempre responde 404 (`public/router.py:50-53`).
8. **Personal huérfano:** `StaffProfile.user_id=uuid.uuid4()` no corresponde a `platform.users` ni crea membresía (`staff/router.py:40`); el empleado no puede autenticarse.
9. **Reservas sin control de solapamiento:** no hay consulta de conflicto ni constraint de exclusión, pese a tener `btree_gist` disponible (`infra/docker/postgres/init/01-init.sql:10`; `reservations/service.py:17-31`).
10. **`ReceiptResponse` nunca se sirve:** el endpoint público lanza 404 fijo (`public/router.py:94-96`).
11. **Webhook sin firma:** lee el body y lo descarta; no valida `X-Signature` (`webhooks/router.py:24-33`), contradiciendo D-073.
12. **Downgrade de migración tenant incorrecto:** crea `alembic_version` en vez de eliminarla (`migrations/tenant/versions/d6a072ef02e3_initial_tenant_schema.py:195`).
13. **Health duplicado:** se monta en `/health` y otra vez bajo `/api/v1` (`main.py:47`; `api/router.py:32`); OpenAPI expone ambos.

### 6.3 Endpoints sin UI / UI sin endpoint

- **Backend:** 27 paths OpenAPI; **0 consumidos por el frontend**. No hay UI para staff, auditoría, webhooks, pagos/confirmación, receipts ni verificación de tenants.
- **UI sin soporte real:** `/admin/caja` no tiene endpoint que confirme pago y libere mesa; `/admin/pedidos` no tiene endpoint de cambio de estado; `/public-site/reservas` no tiene consulta de disponibilidad; `/solicita` no tiene endpoint de solicitud (solo alta directa de tenant); `/mesa/[token]` apunta a un stub que devuelve el token sin consultar la BD.
- **Cabeceras muertas:** `middleware.ts:35-39` inyecta `x-tenant-slug`, pero el backend nunca las lee; la resolución real es JWT (privado) y `{slug}` de path (público).

### 6.4 Validaciones y manejo de errores

- Pedido acepta `items: []` y no valida que `table_session_id` pertenezca al tenant (`orders/schemas.py:155-159`, `orders/service.py:19-26`).
- `limit`/`offset` de plataforma sin cota (`platform/router.py:47-52`); el resto de listados no pagina.
- `price_cents` admite 0 (`menus/schemas.py:123`); no se valida categoría existente antes de crear producto (`menus/service.py:28-40`).
- El frontend espera `{error:{code,message}}` (`frontend/src/lib/api.ts:30-41`), pero los `HTTPException` de FastAPI devuelven `{detail}` (p. ej. `auth/router.py:28-31`): los mensajes de error se pierden.
- El handler global 500 no registra el error ni un `request_id` (`core/errors.py:11-23`): no hay trazabilidad.
- No hay CSRF: la doc define `lixus_csrf` y doble envío (`docs/08-SEGURIDAD-Y-ACCESO.md:152-157`), pero no existe código (`grep` sin coincidencias en `backend/app` y `frontend/src`).

### 6.5 Código muerto y deuda

- Sin uso: `AuditEvent` (`core/events.py:20`), `constant_time_compare` y `random_hex` (`core/security.py:34,44`), `OrderStatusUpdate` (`orders/schemas.py:188`), `TableSessionResponse`/`ServiceRequestResponse` (`tables/schemas.py:31,45`), `pagination.py`, y los modelos `PlatformAdmin`, `SubscriptionInvoice`, `TenantVerification`, `VerificationCode` (`platform/models.py:115-233`).
- Dependencias declaradas sin import en `app/`: `passlib`, `python-magic`, `redis` (`backend/requirements.txt:25,31,39`); `mypy` configurado pero ausente del CI.
- `provision_tenant` es un método de ~175 líneas que mezcla DDL, subprocess de Alembic, ORM, permisos y estado (`platform/service.py:82-257`); un `except Exception` amplio convierte cualquier fallo en 500 y deja schema/tenant parciales sin limpieza (`platform/service.py:240-257`).
- Sin seeds: no hay planes ni tenants demo; `/platform/plans` devuelve vacío en una base nueva (`platform/router.py:89-98`).
- `README.md:278` dice “Fase 1 en curso” mientras `docs/06-HISTORIAL.md:106-121` registra Fase 2; la sección 5 del README marca rate limiting como pendiente pero el diagrama de arquitectura (`README.md:24`) lo presenta como implementado.

---

## 7. Seguridad y multitenancy

| Hallazgo | Severidad | Evidencia |
|---|---|---|
| `/platform/tenants` (GET/POST), `/platform/tenants/{id}`, `/verify`, `/plans` y `/audit` sin autenticación ni rol Lixus | **Crítica** | `platform/router.py:25-99`; `audit/router.py:16-19` |
| Cualquiera puede enumerar todos los tenants y sus `schema_name` (rompe RN-03 y la privacidad comercial) | **Crítica** | `platform/router.py:41-52`; `platform/schemas.py:25-37` |
| Alta de tenant pública: DDL + migraciones por request, sin rate limit → agotamiento de recursos | **Alta** | `platform/router.py:25-38`; `platform/service.py:55-80` |
| `Secure=False` hardcodeado en la cookie de sesión | **Alta** | `auth/router.py:42` |
| Sin CSRF y `SameSite=Lax` como única defensa | **Alta** | `auth/router.py:37-44`; doc `08:152-157` |
| Sin revocación de JWT; empleado desactivado conserva token válido | **Media** | `auth/router.py:49-52`; `core/security.py:48-64` |
| App conecta como dueño de la BD; `lixus_app` se crea y se granta pero no se usa; sin RLS | **Media** | `docker-compose.yml:65-66`; `01-init.sql:21-29`; `platform/service.py:218-224` |
| CORS incluye `localhost` siempre, incluso en producción | **Media** | `main.py:32-39` |
| Secretos JWT con defaults y sin guardia de arranque en producción | **Media** | `core/config.py:57`; `docker-compose.yml:69` |
| Contraseñas de roles de BD hardcodeadas en SQL de init (dev) | **Baja** | `01-init.sql:19,22` |
| `guia.md` (sin trackear) contiene IP pública, VPC y account ID de AWS | **Baja** | `guia.md:6-15` |

**Lo correcto:** bcrypt directo con salt (`core/security.py:23-31`), mensaje genérico de login (`auth/router.py:27-31`), cookie `httpOnly` + `SameSite=Lax`, validación de `schema_name` con regex en todos los puntos de entrada (`database.py:23,50,69`; `dependencies.py:135`), y autorización por membresía resuelta en servidor, no por datos del cliente (`dependencies.py:111-150`).

**Secretos:** `.env` está ignorado por `.gitignore:48-51`, es idéntico a `.env.example` y no aparece en el historial (`git log --all -- .env` vacío). No se detectaron claves reales versionadas.

---

## 8. Calidad, pruebas y repositorio

- **Tests backend:** 4 recogidos (`pytest --collect-only`): 2 de integración, 1 de seguridad y 1 smoke. El de seguridad solo comprueba 401 sin sesión (`tests/security/test_isolation_poc.py:10-13`); no hay pruebas de idempotencia, rate limiting, concurrencia del pool ni inyección de `schema_name`, pese a que `docs/09-ROBUSTEZ.md:158` cita `tests/security/test_idempotency.py`, que no existe.
- **Cobertura:** no medida; no hay umbral ni ejecución con `pytest-cov` en CI. Funcionalmente, la mayor parte de routers está sin cubrir.
- **Tests frontend:** no existen (`find` sin `*.test.*` ni `*.spec.*`); `package.json` no tiene script `test`.
- **Lint:** `ruff check .` pasa; `npm run lint` pasa. No se ejecutaron los tests ni builds (fuera del alcance de lectura).
- **CI:** instala dependencias, inicializa BD, migra plataforma, ejecuta Ruff y pytest; en frontend `npm ci`, lint y build; job Docker con `docker compose build` (`.github/workflows/ci.yml:47-103`). No ejecuta mypy, cobertura ni tests frontend.
- **Contenedores:** backend corre Uvicorn con `--reload` y como root (`backend/Dockerfile:22`); frontend corre `npm run dev` (`frontend/Dockerfile:16`). No son imágenes de producción.
- **Git:** rama `develop`, 15 commits, último `3eddc6d` (2026-10-23). Único archivo sin seguimiento: `guia.md`; los PDF están ignorados por `*.pdf` (`.gitignore:2,69`). Historial coherente por fases, pero sin commits de pruebas de robustez porque esa funcionalidad no existe.

---

## 9. Plan priorizado

### P0 — Imprescindible para aprobar y sustentar

| # | Acción | Criterio de aceptación |
|---|---|---|
| P0-1 | Implementar rate limiting con Redis (token bucket o ventana deslizante) en login y escrituras, por IP+email y por tenant+usuario | 7º intento de login en 1 min → 429 con `Retry-After`; test automatizado que lo demuestre; Redis deja de estar muerto |
| P0-2 | Completar idempotencia en pedidos y pagos, comparar `request_hash`, filtrar `expires_at`, documentar TTL | Misma petición 2 veces → un solo registro y misma respuesta; misma clave con body distinto → 409; tests para ambas operaciones |
| P0-3 | Cerrar el flujo de alta: contraseña/invitación del owner y endpoint `/verify` real que active el tenant y audite | Un tenant creado por API puede iniciar sesión y operar sin tocar SQL; dos tenants activos para la demo |
| P0-4 | CRUD completo de menú (PUT/DELETE) y pedidos con líneas, snapshot de precio y total calculado en servidor; endpoint de cambio de estado | Crear/editar/borrar categoría y producto; pedido con 2 líneas devuelve total correcto; tests de validación |
| P0-5 | Proteger `/platform/*` y `/audit` con rol Lixus; eliminar el listado público de tenants | Sin sesión Lixus → 401/403; un owner de tenant no puede listar otros tenants |
| P0-6 | Conectar el frontend: login real, guard de `/admin`, consumo de API; añadir una pantalla CSR y una SSR/ISR con datos | Login end-to-end con cookie; `/admin` redirige sin sesión; build de Next con al menos 2 estrategias justificadas |
| P0-7 | Migraciones automáticas al arrancar el backend (entrypoint) y healthchecks | `docker compose up` en volumen limpio deja API y web operativas sin comandos manuales |

### P1 — Necesario para una entrega sólida

| # | Acción | Criterio de aceptación |
|---|---|---|
| P1-1 | CSRF (doble envío) y cookie `Secure` según entorno | POST sin `X-CSRF-Token` → 403; en producción `Secure=true` |
| P1-2 | Revocación de sesión (jti/token version) y `switch-tenant` real | Logout invalida el token; cambio de tenant emite cookie nueva y valida membresía |
| P1-3 | Resetear `search_path` en `finally` y no usar `SET` de sesión en provisioning | Prueba de fallo de aprovisionamiento no contamina el pool |
| P1-4 | Usar rol `lixus_app` con privilegios mínimos (o RLS) | La app no conecta como dueño; acceso cruzado a schema denegado por BD |
| P1-5 | Pagos: confirmar, liberar mesa, generar comprobante y token QR | Pago confirmado → mesa `available`; `GET /public/receipts/{token}` devuelve el recibo |
| P1-6 | Reservas: solapamiento, disponibilidad pública y reserva autenticada | Dos reservas en la misma mesa/hora → 409; disponibilidad sin cuenta |
| P1-7 | Personal: usuario global + membresía + rol; invitación | Empleado creado puede iniciar sesión con su rol; desactivarlo revoca acceso |
| P1-8 | QR: lookup real de mesa, sesión única y solicitudes persistidas | Token inválido → 404; solicitud visible para el mesero; mesa con una sola sesión activa |
| P1-9 | Seeds de planes y datos demo | `GET /platform/plans` devuelve 3 planes; demo reproducible |
| P1-10 | Tests de idempotencia, rate limit, aislamiento concurrente y cobertura mínima; mypy en CI | CI falla si baja la cobertura o hay error de tipos; pruebas citadas en docs existen |
| P1-11 | Envolvente de error única (`{error:{code,message}}`) y logging con `request_id` | Frontend muestra el mensaje del backend; los 500 quedan logueados sin filtrar secretos |

### P2 — Calidad y cierre

| # | Acción | Criterio de aceptación |
|---|---|---|
| P2-1 | Limpiar código muerto y modelos sin uso; unificar health | Sin imports/símbolos huérfanos; un solo `/health` |
| P2-2 | Corregir downgrade de migración tenant y añadir prueba de upgrade/downgrade | `alembic downgrade` no crea `alembic_version` |
| P2-3 | Paginación y cotas en listados | `limit` acotado; respuestas paginadas |
| P2-4 | Endurecer imágenes: Next en modo producción, Uvicorn sin `--reload`, usuario no root | `docker compose build` produce imágenes de producción |
| P2-5 | Sincronizar README/docs con el estado real y decidir destino de `guia.md` | README sin afirmaciones falsas; `guia.md` versionado o eliminado con justificación |
| P2-6 | Opcionales: IA con caché/rate limit propio, n8n por webhook, cabeceras CSP/HSTS | Funcionalidad demostrable sin romper el núcleo |

---

## 10. Verificaciones realizadas y límites

**Ejecutado (solo lectura):** `git status`, `git log --oneline -10`, `git ls-files`, `git check-ignore`; lectura de PDFs con `pdftotext`; `ruff check .`; `npm run lint`; `pytest --collect-only`; introspección de `app.openapi()` (27 paths); `grep` de rate limiting, idempotencia, CSRF, RLS, auditoría, seeds y código muerto.

**No ejecutado:** tests de integración (escriben tenants/schemas en la BD), builds de Docker/Next, levantamiento de servicios y migraciones. Las conclusiones sobre esos puntos son lectura estática y se indican como tales.

**Conclusión:** la base multitenant es rescatable y está bien orientada; el esfuerzo debe concentrarse en P0 (robustez obligatoria, flujo de alta, CRUD y frontend) antes de añadir módulos o extras.
