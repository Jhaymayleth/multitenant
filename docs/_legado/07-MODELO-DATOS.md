# 07 — Modelo de datos

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Diseño inicial; validar con la PoC de migraciones antes de generar modelos definitivos
**Decisiones aplicadas:** D-042, D-045, D-046, D-053 a D-055, D-062
**Última actualización:** 22 de octubre de 2026

---

## 1. Principios del modelo

1. **Dos schemas:** `platform` (global) y un `tenant_<id>` por restaurante.
2. **Sin `tenant_id` dentro del schema del tenant:** el schema es el límite.
3. **Identidad global, perfil local:** `platform.users` es la identidad; el perfil del empleado o del cliente vive en el schema del tenant.
4. **Estados como `text` con `CHECK`**, no tipos `ENUM` de PostgreSQL: los enums obligan a replicar el tipo en cada schema y complican las migraciones.
5. **Dinero en enteros** (`*_cents`) con moneda ISO 4217 en la configuración del tenant.
6. **Fechas `timestamptz`**; la zona horaria del restaurante se guarda en su configuración.
7. **Borrado lógico** (`deleted_at`) en catálogo y personas; pedidos y pagos nunca se borran físicamente.
8. **Snapshots** de nombre y precio en las líneas de pedido.
9. **UUID** como clave primaria (`gen_random_uuid()`), excepto tablas de log que usan `bigserial`.

---

## 2. Schema `platform`

### 2.1 `users`

Identidad global de cualquier persona con cuenta.

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | `gen_random_uuid()` |
| `email` | citext UNIQUE NOT NULL | Normalizado a minúsculas |
| `email_verified_at` | timestamptz NULL | |
| `password_hash` | text NULL | NULL si solo usa Google |
| `google_sub` | text UNIQUE NULL | Identificador de Google |
| `full_name` | text NOT NULL | |
| `status` | text NOT NULL | `pending`, `active`, `disabled` + CHECK |
| `last_login_at` | timestamptz NULL | |
| `created_at` / `updated_at` | timestamptz | |

Índices: `unique(email)`, `unique(google_sub) where google_sub is not null`.

### 2.2 `tenants`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `slug` | citext UNIQUE NOT NULL | URL pública; validado `^[a-z0-9-]{3,40}$` |
| `name` | text NOT NULL | Nombre comercial |
| `legal_name` | text NULL | Razón social |
| `schema_name` | text UNIQUE NOT NULL | `tenant_<12 hex>` generado en servidor |
| `status` | text NOT NULL | `provisioning`, `provisioning_failed`, `pending_verification`, `active`, `suspended`, `cancelled` |
| `timezone` | text NOT NULL | Ej. `America/Bogota` |
| `currency` | char(3) NOT NULL | Ej. `COP` |
| `contact_email` | citext NULL | |
| `created_at` | timestamptz | |
| `activated_at` | timestamptz NULL | |
| `updated_at` | timestamptz | |

Índices: `unique(slug)`, `unique(schema_name)`, `(status)`.

### 2.3 `tenant_memberships`

Relación de acceso de una identidad con un tenant. **No** es una suscripción.

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `tenant_id` | uuid FK → tenants | `ON DELETE RESTRICT` |
| `user_id` | uuid FK → users | `ON DELETE CASCADE` |
| `role` | text NOT NULL | `owner`, `admin`, `waiter`, `cashier`, `cook` |
| `status` | text NOT NULL | `invited`, `active`, `disabled`, `revoked` |
| `created_by` | uuid NULL → users | |
| `created_at` / `updated_at` | timestamptz | |

Índices: `unique(tenant_id, user_id)`, `(user_id, status)`, `(tenant_id, role)`.

### 2.4 `platform_admins` (rol Lixus)

| Columna | Tipo | Notas |
|---|---|---|
| `user_id` | uuid PK FK → users | |
| `level` | text NOT NULL | `support`, `admin` |
| `mfa_enabled` | boolean NOT NULL DEFAULT false | MFA obligatorio en producción |
| `mfa_secret_encrypted` | text NULL | Cifrado en reposo |
| `last_access_at` | timestamptz NULL | |
| `created_at` | timestamptz | |

### 2.5 `plans`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `code` | text UNIQUE NOT NULL | `basic`, `intermediate`, `advanced` |
| `name` | text NOT NULL | |
| `capabilities` | jsonb NOT NULL | Funcionalidades habilitadas |
| `limits` | jsonb NOT NULL | Personal, almacenamiento, IA |
| `price_cents` | integer NOT NULL | 0 si aún no se define |
| `currency` | char(3) NOT NULL | |
| `is_active` | boolean NOT NULL DEFAULT true | |
| `created_at` / `updated_at` | timestamptz | |

### 2.6 `subscriptions`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `tenant_id` | uuid UNIQUE FK → tenants | Una suscripción vigente por tenant |
| `plan_id` | uuid FK → plans | |
| `status` | text NOT NULL | `pending`, `trialing`, `active`, `past_due`, `suspended`, `cancelled` |
| `started_at` | timestamptz | |
| `current_period_start` / `current_period_end` | timestamptz | |
| `grace_until` | timestamptz NULL | |
| `activated_by` | uuid NULL → users | Lixus que activó |
| `created_at` / `updated_at` | timestamptz | |

Índices: `(status)`, `(plan_id)`.

### 2.7 `subscription_invoices`

Registro del estado de cobro de la suscripción, **sin procesar dinero**.

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `subscription_id` | uuid FK | |
| `period_start` / `period_end` | timestamptz | |
| `amount_cents` | integer | |
| `status` | text | `pending`, `paid`, `void` |
| `method` | text NULL | `manual`, `transfer`, `card` |
| `reference` | text NULL | |
| `paid_at` | timestamptz NULL | |
| `registered_by` | uuid NULL → users | |
| `created_at` | timestamptz | |

### 2.8 `tenant_verifications`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `tenant_id` | uuid FK | |
| `status` | text | `pending`, `approved`, `rejected` |
| `business_name` | text | |
| `tax_id` | text NULL | |
| `contact_phone` | text NULL | |
| `documents` | jsonb NULL | Referencias a archivos en R2 |
| `submitted_by` | uuid → users | |
| `reviewed_by` | uuid NULL → users | Lixus |
| `reviewed_at` | timestamptz NULL | |
| `rejection_reason` | text NULL | |
| `created_at` | timestamptz | |

### 2.9 `verification_codes`

Códigos de un solo uso para activación de empleado, verificación de correo y recuperación.

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `user_id` | uuid FK → users | |
| `purpose` | text | `employee_activation`, `email_verification`, `password_reset` |
| `code_hash` | text NOT NULL | Nunca se guarda el código en claro |
| `expires_at` | timestamptz NOT NULL | |
| `attempts` | smallint DEFAULT 0 | |
| `consumed_at` | timestamptz NULL | |
| `created_at` | timestamptz | |

Índice: `(user_id, purpose, consumed_at)`.

### 2.10 `idempotency_keys` (global)

Se usa para operaciones de plataforma, como crear un tenant.

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `scope` | text NOT NULL | `platform:create_tenant` |
| `key` | text NOT NULL | Valor de `Idempotency-Key` |
| `request_hash` | text NOT NULL | sha256 del método + ruta + cuerpo canónico |
| `status` | text NOT NULL | `in_progress`, `completed`, `failed` |
| `response_status` | integer NULL | |
| `response_body` | jsonb NULL | Respuesta original |
| `created_at` | timestamptz | |
| `expires_at` | timestamptz NOT NULL | |

Índice: `unique(scope, key)`, `(expires_at)`.

### 2.11 `audit_log` (global)

| Columna | Tipo | Notas |
|---|---|---|
| `id` | bigserial PK | |
| `actor_user_id` | uuid NULL | |
| `actor_kind` | text | `user`, `platform_admin`, `system`, `ai` |
| `tenant_id` | uuid NULL | |
| `action` | text NOT NULL | Ej. `membership.role_changed` |
| `entity_type` / `entity_id` | text / uuid NULL | |
| `ip` | inet NULL | |
| `user_agent` | text NULL | |
| `metadata` | jsonb NULL | Sin secretos ni tokens |
| `created_at` | timestamptz | |

Índices: `(tenant_id, created_at desc)`, `(action, created_at desc)`.

---

## 3. Schema del tenant

### 3.1 `tenant_settings` (singleton)

| Columna | Tipo | Notas |
|---|---|---|
| `id` | boolean PK DEFAULT true | CHECK (`id = true`): fuerza una sola fila |
| `display_name` | text | |
| `tagline` | text NULL | |
| `description` | text NULL | |
| `logo_url` | text NULL | Clave en R2 |
| `hero_image_url` | text NULL | |
| `color_primary` | text NULL | Hex validado |
| `color_secondary` | text NULL | |
| `sections` | jsonb | `{hero:true, menu:true, gallery:false, ...}` |
| `contact` | jsonb | Teléfono, correo, redes |
| `address` | text NULL | |
| `hours` | jsonb NULL | Horarios por día |
| `is_published` | boolean DEFAULT false | |
| `updated_at` | timestamptz | |

### 3.2 `staff_profiles`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `user_id` | uuid UNIQUE NOT NULL | Referencia lógica a `platform.users` (sin FK entre schemas) |
| `full_name` | text NOT NULL | |
| `phone` | text NULL | |
| `position` | text NULL | Etiqueta libre |
| `status` | text | `active`, `inactive` |
| `hired_at` | date NULL | |
| `created_at` / `updated_at` | timestamptz | |

> **Nota:** PostgreSQL no permite claves foráneas entre schemas sin acoplar los datos. La integridad `user_id` se valida en la aplicación y con pruebas.

### 3.3 `customers` (clientes registrados del restaurante)

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `user_id` | uuid NULL UNIQUE | NULL si fue creado manualmente |
| `full_name` | text NOT NULL | |
| `email` | citext NULL | |
| `phone` | text NULL | |
| `notes` | text NULL | |
| `status` | text | `active`, `blocked` |
| `created_at` / `updated_at` | timestamptz | |
| `deleted_at` | timestamptz NULL | |

Índices: `(email)`, `(phone)`.

### 3.4 `menu_categories`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `name` | text NOT NULL | |
| `description` | text NULL | |
| `sort_order` | integer DEFAULT 0 | |
| `is_active` | boolean DEFAULT true | |
| `created_at` / `updated_at` | timestamptz | |
| `deleted_at` | timestamptz NULL | |

Índice: `(is_active, sort_order)`.

### 3.5 `menu_products`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `category_id` | uuid NULL FK → menu_categories | `ON DELETE SET NULL` |
| `name` | text NOT NULL | |
| `description` | text NULL | |
| `price_cents` | integer NOT NULL | CHECK `>= 0` |
| `image_url` | text NULL | |
| `is_available` | boolean DEFAULT true | |
| `is_published` | boolean DEFAULT false | |
| `sort_order` | integer DEFAULT 0 | |
| `created_at` / `updated_at` | timestamptz | |
| `deleted_at` | timestamptz NULL | |

Índices: `(category_id, sort_order)`, `(is_available, is_published)`.

### 3.6 `restaurant_tables`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `code` | text NOT NULL | Número o nombre visible |
| `zone` | text NULL | Salón, terraza |
| `seats` | smallint NULL | |
| `qr_token_hash` | text NOT NULL | Hash del token impreso en el QR |
| `status` | text NOT NULL DEFAULT 'available' | `available`, `occupied`, `pending_payment`, `reserved`, `inactive` |
| `status_updated_at` | timestamptz NULL | |
| `status_updated_by` | uuid NULL | `user_id` que hizo la última transición manual |
| `is_active` | boolean DEFAULT true | |
| `created_at` / `updated_at` | timestamptz | |

Índices: `unique(code)`, `(is_active)`, `(status)`.

### 3.7 `table_sessions`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `table_id` | uuid FK → restaurant_tables | |
| `session_token_hash` | text NOT NULL | Token anónimo del cliente |
| `status` | text | `open`, `closed` |
| `opened_at` | timestamptz | |
| `closed_at` | timestamptz NULL | |
| `closed_by` | uuid NULL | `user_id` del mesero |
| `close_reason` | text NULL | `payment_confirmed`, `cash_cancelled` |
| `token_expires_at` | timestamptz | Vigencia del token anónimo; la sesión no caduca por tiempo |

Índices: `partial unique (table_id) where status = 'open'`, `(token_expires_at)`.

La sesión termina por pago confirmado o por cancelación en efectivo, no por temporizador (D-068).

### 3.8 `service_requests`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `table_session_id` | uuid FK → table_sessions | |
| `type` | text | `complaint`, `missing_item`, `request`, `checkout` |
| `note` | text NULL | Opcional, sin datos personales obligatorios |
| `status` | text | `pending`, `attended`, `cancelled` |
| `created_at` | timestamptz | |
| `attended_by` / `attended_at` | uuid NULL / timestamptz NULL | |

Índices: `(status, created_at)`, `(table_session_id)`.

### 3.9 `orders`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `table_id` | uuid NULL FK | Pedido presencial |
| `table_session_id` | uuid NULL FK | |
| `customer_id` | uuid NULL FK → customers | Obligatorio en `delivery`; opcional en mesa |
| `reservation_id` | uuid NULL FK → reservations | |
| `channel` | text | `dine_in`, `delivery`, `takeaway` |
| `status` | text | `draft`, `confirmed`, `in_preparation`, `ready`, `served`, `out_for_delivery`, `delivered`, `closed`, `cancelled` |
| `delivery_address` | text NULL | Obligatoria en `delivery` |
| `delivery_phone` | text NULL | Obligatorio en `delivery` |
| `delivery_fee_cents` | integer DEFAULT 0 | Tarifa configurable (P-23) |
| `payment_status` | text | `unpaid`, `pending`, `paid`, `refunded`, `not_applicable` |
| `subtotal_cents` | integer | Calculado en servidor |
| `total_cents` | integer | `subtotal_cents + delivery_fee_cents`; sin impuestos ni propinas (D-072) |
| `notes` | text NULL | |
| `created_by` | uuid NULL | `user_id` |
| `created_at` / `confirmed_at` / `closed_at` | timestamptz | |
| `cancelled_reason` | text NULL | |

CHECK de canal:

- `dine_in` exige `table_id` y `table_session_id`.
- `delivery` exige `customer_id`, `delivery_address` y `delivery_phone`, y prohíbe `table_id`.

Índices: `(status, created_at)`, `(table_id, created_at)`, `(payment_status)`, `(customer_id)`, `(channel, status)`.

### 3.10 `order_items`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `order_id` | uuid FK → orders | `ON DELETE CASCADE` solo en borrador |
| `product_id` | uuid NULL | Referencia lógica |
| `product_name` | text NOT NULL | Snapshot |
| `unit_price_cents` | integer NOT NULL | Snapshot al confirmar |
| `quantity` | integer NOT NULL | CHECK `> 0` |
| `line_total_cents` | integer NOT NULL | `unit_price_cents * quantity` |
| `notes` | text NULL | |
| `status` | text | `pending`, `preparing`, `ready`, `served`, `cancelled` |

Índice: `(order_id)`.

### 3.11 `reservations`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `customer_id` | uuid NOT NULL FK → customers | Reservar exige cuenta en el tenant |
| `customer_name` | text NOT NULL | |
| `customer_email` | citext NULL | |
| `customer_phone` | text NULL | |
| `start_at` | timestamptz NOT NULL | |
| `duration_minutes` | smallint NOT NULL | |
| `party_size` | smallint NOT NULL | CHECK `> 0` |
| `table_id` | uuid NOT NULL FK → restaurant_tables | La reserva ocupa una mesa concreta |
| `status` | text | `requested`, `confirmed`, `seated`, `completed`, `cancelled`, `no_show` |
| `notes` | text NULL | |
| `created_by` | uuid NULL | |
| `created_at` / `updated_at` | timestamptz | |

Índices: `(start_at, status)`, `(table_id, start_at)`.
**Restricción de solapamiento:** ver `09-ROBUSTEZ.md` (exclusion constraint con `tstzrange`).

### 3.12 `payments`

Registro del estado del pago. **No** almacena datos de tarjeta ni procesa dinero.

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `order_id` | uuid NULL FK → orders | |
| `reservation_id` | uuid NULL FK → reservations | |
| `amount_cents` | integer NOT NULL | |
| `method` | text | `cash`, `card_external`, `online`, `transfer`, `other` |
| `provider` | text NULL | `sandbox`, `wompi`, `stripe` (según adaptador) |
| `status` | text | `registered`, `pending`, `paid`, `refunded` |
| `reference` | text NULL | Referencia externa o de pasarela |
| `registered_by` | uuid NULL | |
| `confirmed_by` | uuid NULL | `user_id` del mesero o cajero que confirma |
| `confirmed_at` | timestamptz NULL | Dispara el cierre de sesión y la liberación de mesa |
| `paid_at` | timestamptz NULL | |
| `notes` | text NULL | |
| `created_at` | timestamptz | |

CHECK: exactamente uno de `order_id` o `reservation_id` no nulo.
Índices: `(order_id)`, `(reservation_id)`, `(status)`.

### 3.13 `payment_events`

Registro de webhooks recibidos del proveedor de pago. Es la garantía de idempotencia del lado del proveedor.

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `payment_id` | uuid NULL FK → payments | |
| `provider` | text NOT NULL | `sandbox`, `wompi`, `stripe` |
| `provider_event_id` | text NOT NULL | Identificador único del evento |
| `event_type` | text | `payment.paid`, `payment.failed` |
| `payload_hash` | text | sha256 del cuerpo recibido |
| `status` | text | `received`, `processed`, `ignored`, `failed` |
| `error` | text NULL | |
| `received_at` / `processed_at` | timestamptz | |

Índices: `unique(provider, provider_event_id)`, `(payment_id)`.

### 3.14 `receipts`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `payment_id` | uuid UNIQUE FK → payments | |
| `number` | text NOT NULL | Consecutivo por tenant |
| `public_token_hash` | text NOT NULL | Token del QR de descarga |
| `issued_at` | timestamptz | |
| `emailed_at` | timestamptz NULL | |
| `download_count` | integer DEFAULT 0 | |

Índices: `unique(number)`, `unique(public_token_hash)`.
**Consecutivo:** secuencia creada por schema (`receipt_number_seq`), no una tabla global.

### 3.15 `ai_usage`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | |
| `user_id` | uuid NULL | |
| `feature` | text | `description`, `assistant`, `query` |
| `provider` | text | `groq`, `openrouter`, `gemini` |
| `model` | text | |
| `prompt_tokens` / `completion_tokens` | integer | |
| `latency_ms` | integer | |
| `status` | text | `success`, `rate_limited`, `error` |
| `created_at` | timestamptz | |

Índice: `(created_at)`, `(feature, created_at)`.

### 3.16 `idempotency_keys` (por tenant)

Misma estructura que la global, con `scope` como `order:create` o `reservation:create`. Vive en el schema del tenant porque las operaciones que protege son locales.

---

## 4. Relaciones principales

```
platform.users 1 ──── * platform.tenant_memberships * ──── 1 platform.tenants
platform.tenants 1 ──── 1 platform.subscriptions ──── 1 platform.plans
platform.tenants 1 ──── * platform.tenant_verifications
platform.users 1 ──── 0..1 platform.platform_admins

tenant_schema
staff_profiles        (user_id → platform.users, referencia lógica)
customers             (user_id → platform.users, referencia lógica)
menu_categories 1 ──── * menu_products
restaurant_tables 1 ──── * table_sessions 1 ──── * service_requests
restaurant_tables 1 ──── * orders ──── * order_items
customers 1 ──── * reservations
orders 1 ──── * payments
reservations 1 ──── * payments
payments 1 ──── 1 receipts
```

---

## 5. Convenciones

| Tema | Convención |
|---|---|
| Tablas | `snake_case`, plural |
| Claves | `id` uuid; FK `<entidad>_id` |
| Fechas | `timestamptz`; sufijos `_at` |
| Booleanos | prefijo `is_` / `has_` |
| Dinero | sufijo `_cents`, integer |
| JSON | `jsonb`, validado en aplicación |
| Estados | `text` + `CHECK` |
| Borrado | `deleted_at` en catálogo y personas |
| Índices | Sufijo `_idx`; únicos `_key` |

---

## 6. Migraciones

| Cadena | Contenido | Ejecución |
|---|---|---|
| `migrations/platform` | Schema global | Una vez por entorno |
| `migrations/tenant` | Tablas del restaurante | Una vez por schema de tenant |

- Cada schema de tenant tiene su propia tabla `alembic_version`.
- El aprovisionamiento ejecuta la cadena de tenant completa.
- Una migración nueva se aplica a todos los tenants activos con registro de resultado.
- Las migraciones deben ser **compatibles hacia atrás** durante un despliegue: primero expandir, luego migrar datos, luego contraer.
- Prohibido en migraciones: borrar columnas con datos en el mismo despliegue que deja de usarlas.

---

## 7. Datos iniciales (seed)

1. Planes `basic`, `intermediate`, `advanced` con capacidades mínimas.
2. Usuario Lixus inicial (creado por script, no por registro público).
3. Opcional en desarrollo: dos tenants de demostración (`demo-a`, `demo-b`) con usuarios y datos distintos para las pruebas de aislamiento.

Los seeds no se ejecutan automáticamente en producción.

---

## 8. Pendientes del modelo

| Tema | Pendiente |
|---|---|
| Canales de pedido | `delivery` aprobado; `takeaway` queda como evolución |
| Domicilios | Cobertura, costo de envío, estados y pago (P-23) |
| Estados de pedido | Validar `out_for_delivery` y `delivered` (P-23) |
| Solapamiento de reservas | Tolerancia y política de no-show (P-07) |
| Comprobantes | Numeración y formato simple definidos (D-070); sin validez fiscal |
| Pago en línea | Webhook firmado y proveedor simulado definidos (D-073); pasarela real al desplegar |
| Campos personalizados | Descartados en el MVP (D-034) |
| Retención | Política de purga de tokens, códigos e idempotencia |
| Impuestos | No se aplican en el MVP (D-072) |

---

**Fin de `07-MODELO-DATOS.md`.**
