# 03 — Arquitectura del proyecto Lixus

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Diseño base para implementación; los puntos marcados como *PoC* deben validarse antes de cerrar el código
**Decisiones aplicadas:** D-042 a D-046, D-052, D-061, D-065
**Última actualización:** 22 de octubre de 2026

---

## 1. Vista general

Lixus es un **monolito modular** con dos aplicaciones desplegables y servicios de apoyo:

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Navegador del usuario                         │
│   Sitio público · Panel del restaurante · Portal de tenants (Lixus)  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │ HTTPS + cookie httpOnly
┌───────────────────────────────▼──────────────────────────────────────┐
│                    Next.js + TypeScript (frontend)                   │
│   SSG/ISR para páginas públicas · CSR para paneles privados          │
└───────────────────────────────┬──────────────────────────────────────┘
                                │ REST/JSON (misma sesión por cookie)
┌───────────────────────────────▼──────────────────────────────────────┐
│                       FastAPI + Python (API)                         │
│  Auth · Autorización · Resolución de tenant · Validación · Reglas    │
│  Rate limiting · Idempotencia · Herramientas de IA · Auditoría       │
└───────┬───────────────────────┬──────────────────────┬───────────────┘
        │                       │                      │
┌───────▼────────┐   ┌──────────▼─────────┐   ┌────────▼──────────────┐
│  PostgreSQL 16 │   │       Redis        │   │   Cloudflare R2       │
│ platform       │   │ rate limit         │   │   imágenes y archivos │
│ tenant_xxx ... │   │ caché / idempot.   │   │   bucket privado      │
└────────────────┘   └────────────────────┘   └───────────────────────┘
                                                       │
                                              ┌────────▼──────────────┐
                                              │ Servicio de IA        │
                                              │ Groq → OpenRouter →   │
                                              │ Gemini (failover)     │
                                              └───────────────────────┘
```

**Fronteras de confianza**

| Componente | Confianza | Responsabilidad |
|---|---|---|
| Navegador | No confiable | Presenta datos; nunca decide permisos ni tenant |
| API FastAPI | Fuente de autoridad | Autentica, autoriza, valida y selecciona el schema |
| PostgreSQL | Fuente de verdad | Datos y aislamiento estructural |
| Redis | Apoyo | Límites y caché; su caída no debe filtrar datos |
| R2 | Almacenamiento | Archivos privados con URL firmada |

---

## 2. Modelo multitenant

### 2.1 Dos tipos de schema

| Schema | Contenido | ¿Compartido? |
|---|---|---|
| `platform` | Usuarios globales, tenants, membresías, planes, suscripciones, verificaciones, auditoría, claves de idempotencia globales | Sí |
| `tenant_<id>` | Personal, clientes del restaurante, menú, mesas, sesiones, pedidos, reservas, pagos, comprobantes, configuración, consumo de IA | No: uno por restaurante |

**Regla clave:** las tablas del tenant **no llevan columna `tenant_id`**. El propio schema es el tenant. Añadir `tenant_id` dentro del schema del tenant duplicaría el mecanismo de aislamiento y abriría la puerta a errores por filtros olvidados.

### 2.2 Nombres de schema

- Se generan en el servidor: `tenant_` + 12 caracteres hexadecimales derivados del UUID del tenant.
- Se validan con `^tenant_[a-f0-9]{12}$` antes de usarse en cualquier DDL.
- El usuario nunca propone el nombre del schema.
- El nombre se guarda en `platform.tenants.schema_name`.

**Motivo:** evita inyección de identificadores y colisiones; el `slug` público del restaurante es un dato de negocio distinto del schema.

### 2.3 Aprovisionamiento de un tenant

```
POST /platform/tenants  (Lixus)  + Idempotency-Key
   │
   ├─ 1. Validar identidad, permiso global e idempotencia
   ├─ 2. Insertar tenant en estado 'provisioning' (platform)
   ├─ 3. CREATE SCHEMA tenant_<id> con el rol de migraciones
   ├─ 4. Aplicar migraciones del tenant con Alembic (version_table_schema = schema)
   ├─ 5. Insertar configuración inicial y usuario CEO con membresía 'owner'
   ├─ 6. Otorgar permisos al rol de aplicación sobre el schema nuevo
   ├─ 7. Estado 'pending_verification' o 'active'
   └─ 8. Guardar respuesta en la tabla de idempotencia
```

**Fallo a mitad:** el tenant queda en `provisioning_failed` con el error registrado. Un reintento con la misma `Idempotency-Key` no crea un segundo schema: reanuda o devuelve el error de forma controlada. Un job de mantenimiento puede limpiar schemas huérfanos.

**Activación:** la creación técnica y la activación comercial se separan (D-031). Un tenant puede estar provisionado y aún no activo.

### 2.4 Resolución del tenant en cada petición

```
Cookie httpOnly ──► JWT ──► sub (usuario) + tenant_id + role
                              │
                              ├─ Verificar firma, expiración, emisor y audiencia
                              ├─ Cargar membresía en platform.tenant_memberships
                              │   (user_id, tenant_id, status = active)
                              ├─ Cargar tenant en platform.tenants (status válido)
                              ├─ Verificar permiso del rol para la operación
                              ├─ Obtener schema_name desde la BD (no del cliente)
                              └─ Abrir transacción y fijar search_path
```

Dependencia de FastAPI (pseudocódigo):

```python
async def tenant_context(request: Request, user=Depends(current_user)) -> TenantCtx:
    tenant_id = user.tenant_id            # viene del JWT firmado
    membership = await memberships.get_active(user.id, tenant_id)
    if membership is None:
        raise HTTPException(403, "Sin acceso a este restaurante")
    tenant = await tenants.get_active(tenant_id)
    schema = tenant.schema_name           # generado por el servidor
    assert SAFE_SCHEMA.match(schema)
    return TenantCtx(tenant=tenant, schema=schema, role=membership.role)
```

Apertura de transacción:

```python
async with session.begin():
    await session.execute(
        text("SELECT set_config('search_path', :sp, true)"),
        {"sp": f'"{schema}", platform, public'},
    )
    ...
```

`set_config(..., true)` equivale a `SET LOCAL`: el cambio vive solo en la transacción y **no contamina** la conexión que el pool reutilizará.

**Alternativas evaluadas**

| Estrategia | Ventaja | Riesgo | Uso |
|---|---|---|---|
| `search_path` por transacción | Una sola conexión, sencilla de razonar | Un `SET` fuera de transacción contamina el pool | **Elegida** |
| Un engine por tenant | Aislamiento explícito | Explosión de conexiones con cientos de tenants | Descartada para el MVP |
| Nombre de schema dinámico en cada consulta | Sin estado de sesión | Fácil de olvidar en una consulta | Descartada |

**PoC obligatoria:** dos tenants, dos usuarios, peticiones concurrentes y verificación de que el `search_path` no se filtra. Si falla, se cambia a engine por tenant con pool pequeño.

### 2.5 Roles de base de datos

| Rol | Uso | Permisos |
|---|---|---|
| `lixus_migrator` | Migraciones y aprovisionamiento | Dueño de schemas; puede DDL |
| `lixus_app` | API en ejecución | `USAGE` en schemas; DML sobre tablas; sin DDL; sin `BYPASSRLS` |

La API nunca corre como superusuario ni como dueño de los schemas. Esto convierte un error de `search_path` en un error de permisos visible, no en una fuga silenciosa.

### 2.6 Migraciones multi-schema

- **Dos cadenas de migración:** `migrations/platform` y `migrations/tenant`.
- La cadena de tenant se aplica a cada schema con su propia tabla `alembic_version` (`version_table_schema`).
- Al crear un tenant se ejecuta la cadena completa.
- Al añadir una tabla o columna se recorre `platform.tenants` y se aplica a cada schema.
- El proceso es idempotente y registra el resultado por tenant.
- **PoC:** crear dos tenants, aplicar una migración nueva a ambos, verificar versión y rollback en uno de prueba.

> Alembic no gestiona schemas de forma transparente en todos los casos: hay que configurar `include_schemas=True`, `version_table_schema` y un `search_path` explícito en `env.py`. Validar antes de escribir los modelos definitivos.

---

## 3. Backend (FastAPI)

### 3.1 Organización modular

```
backend/
├── app/
│   ├── core/            # configuración, seguridad, base de datos, errores
│   ├── auth/            # login, tokens, cookies, verificación, recuperación
│   ├── platform/        # tenants, verificación, planes, suscripciones, Lixus
│   ├── access/          # membresías, roles, permisos
│   ├── menu/            # categorías y productos
│   ├── staff/           # perfiles de empleados
│   ├── customers/       # clientes registrados del tenant
│   ├── tables/          # mesas y sesiones QR
│   ├── orders/          # pedidos y líneas
│   ├── reservations/    # reservas
│   ├── payments/        # estados de pago y comprobantes
│   ├── public_site/     # configuración y datos de la página pública
│   ├── ai/              # proveedores, prompts, herramientas, consumo
│   ├── audit/           # eventos
│   └── shared/          # utilidades, paginación, validaciones
├── migrations/
│   ├── platform/
│   └── tenant/
└── tests/
    ├── unit/
    ├── integration/
    └── security/        # aislamiento, IDOR, autorización
```

Cada módulo expone `router.py`, `service.py`, `repository.py`, `schemas.py` y `models.py`. Las reglas de negocio viven en `service.py`, no en el router ni en el ORM.

### 3.2 Capas y responsabilidades

| Capa | Hace | No hace |
|---|---|---|
| Router | Valida entrada HTTP, aplica dependencias, devuelve códigos | Reglas de negocio |
| Service | Orquesta reglas, transacciones, permisos de negocio | SQL directo |
| Repository | Consultas y persistencia | Decidir permisos |
| Modelos | Estructura de datos | Lógica de negocio |

### 3.3 Validación y errores

- Pydantic v2 para validar cuerpos, query y path.
- Formato de error uniforme: `{"error": {"code", "message", "details"}}`.
- Códigos: 400 validación, 401 sin sesión, 403 sin permiso, 404 no existe **o no pertenece al tenant**, 409 conflicto, 422 regla de negocio, 429 límite, 500 error interno.
- Los 404 de recursos ajenos no revelan su existencia.

### 3.4 Auditoría

Eventos mínimos: `tenant.created`, `tenant.activated`, `tenant.verification_rejected`, `membership.created`, `membership.role_changed`, `membership.revoked`, `auth.login_failed`, `auth.login_succeeded`, `auth.password_reset`, `table_session.opened`, `table_session.closed`, `order.created`, `order.status_changed`, `payment.registered`, `plan.changed`, `ai.tool_invoked`, `lixus.data_accessed`.

---

## 4. Frontend (Next.js)

### 4.1 Áreas

| Ruta | Área | Audiencia | Render |
|---|---|---|---|
| `/` | Landing de Lixus | Público | SSG |
| `/r/[slug]` | Página pública del restaurante | Público | SSG + ISR |
| `/r/[slug]/menu` | Menú público | Público | SSG + ISR |
| `/r/[slug]/reserva` | Reserva pública (requiere cuenta) | Cliente registrado | CSR |
| `/r/[slug]/cuenta` | Reservas y domicilios del cliente | Cliente registrado | CSR |
| `/t/[token]` | Sesión anónima de mesa (QR) | Cliente anónimo | CSR |
| `/app/*` | Panel del restaurante | Personal | CSR |
| `/lixus/*` | Portal de plataforma | Lixus | CSR |
| `/login`, `/registro` | Autenticación | Todos | CSR |

### 4.2 Estrategias de renderizado (D-065 / RAC-09)

| Estrategia | Dónde | Por qué |
|---|---|---|
| **SSG + ISR** | Página pública y menú | Contenido cambia poco, debe indexarse y cargar rápido; revalidación por tiempo o bajo demanda al publicar cambios. |
| **CSR** | Panel, portal de Lixus, sesión QR, reservas | Datos privados, dependen de la sesión y cambian en tiempo real; no necesitan SEO. |

**Justificación para la sustentación:** las páginas públicas se benefician de HTML pre-renderizado (SEO, primera pintura, tráfico sin sesión), mientras que los paneles privados no deben cachearse ni indexarse y requieren datos frescos por usuario.

**Advertencia:** la modalidad académica debe declararse (P-01). Con un backend FastAPI independiente, el proyecto no es "Next.js fullstack" en sentido estricto; si se declara Opción A, el frontend debe poder explicarse como React con CSR, y el uso de SSG/ISR se presenta como valor agregado.

### 4.3 Comunicación con la API

- `fetch` con `credentials: 'include'`; la cookie viaja en la misma eTLD+1.
- Si frontend y API quedan en dominios distintos, se usa un proxy/BFF en Next.js para evitar problemas de cookie de terceros.
- En SSR/ISR, el servidor de Next.js consume los endpoints **públicos** sin credenciales; para datos privados se usa la cookie del usuario, no un token de servicio.
- Nunca se expone una clave de API ni un token interno al navegador.

### 4.4 Rutas protegidas

- Backend: dependencia de sesión + membresía + permiso.
- Frontend: el layout privado verifica sesión y redirige; **es solo experiencia de usuario**, no seguridad.
- El menú del panel se construye según permisos devueltos por la API, pero cada endpoint revalida.

---

## 5. Datos y archivos

- PostgreSQL 16, `citext` para correos, `pgcrypto` para `gen_random_uuid`, `btree_gist` para solapamientos de reservas.
- Dinero en enteros (`*_cents`) y moneda del tenant (ISO 4217).
- Fechas en `timestamptz`; zona horaria del restaurante en su configuración.
- Configuración visual y capacidades de plan en `jsonb` con validación de esquema en la aplicación.
- Archivos en R2 con bucket privado, nombre UUID, tipo validado por magic bytes, tamaño máximo configurable y URL firmada de corta duración.

---

## 6. Seguridad de la arquitectura

| Riesgo | Control |
|---|---|
| Acceso cruzado por identificador | Contexto de tenant del JWT + membresía + búsqueda en el schema autorizado |
| Inyección de nombre de schema | Nombre generado y validado; nunca proviene del cliente |
| Fuga por pool de conexiones | `SET LOCAL` por transacción + prueba de concurrencia |
| Escalada de rol | Permisos comprobados en servidor; el rol del token no basta |
| Robo de cookie | `HttpOnly`, `Secure`, `SameSite`, expiración corta, rotación |
| CSRF | `SameSite` + header personalizado obligatorio en escrituras |
| Abuso de endpoints | Rate limiting por usuario/tenant/IP |
| Duplicados por reintento | Idempotencia en escrituras críticas |
| Fuga por IA | Herramientas con permisos del usuario y contexto del tenant |
| Enlaces de comprobante adivinables | Token aleatorio de 256 bits y caducidad |
| Archivos maliciosos | Validación en servidor y re-codificación de imágenes |

Detalle en `08-SEGURIDAD-Y-ACCESO.md` y `09-ROBUSTEZ.md`.

---

## 7. Entornos

| Entorno | Base de datos | Archivos | Objetivo |
|---|---|---|---|
| Local | PostgreSQL y Redis en Docker | R2 real o MinIO local | Desarrollo y pruebas |
| CI | Servicios de PostgreSQL y Redis en el runner | No aplica | Lint, tests, build |
| Producción | Gestionada o contenedor con respaldo | R2 | Operación real (pendiente P-14) |

---

## 8. Decisiones de arquitectura todavía abiertas

| Tema | Estado | Documento |
|---|---|---|
| Modalidad académica A/B | Por confirmar con el docente | `05-PENDIENTES.md` P-01 |
| Caja ligera y comprobantes | Definido (D-070) | — |
| URL pública: subdominio o ruta | Por decidir | P-06 |
| Reservas: tolerancia y no-show | Por definir | P-07 |
| Domicilios: cobertura, costo y entrega | Por definir | P-23 |
| Proveedor de correo | Por definir | P-11 |
| Pasarela de suscripciones | Por definir | P-09 |
| Arquitectura AWS concreta | Por definir | P-14 |

---

## 9. Pruebas de arquitectura obligatorias (PoC)

Antes de construir módulos funcionales:

1. Crear dos tenants con schemas distintos y un usuario en cada uno.
2. Un usuario con acceso a ambos cambia de tenant y recibe un token nuevo.
3. Un usuario de A intenta leer, editar y borrar por ID un recurso de B → 403/404.
4. Se aplica una migración nueva a ambos schemas y ambos quedan en la misma versión.
5. Peticiones concurrentes a A y B con el mismo pool → cada una ve solo su schema.
6. Se revoca una membresía y el token anterior deja de servir.
7. Se envía un `tenant_id` o `schema` manipulado → la API lo ignora o rechaza.

Si estas pruebas no pasan, no se avanza al CRUD de negocio.

---

**Fin de `03-ARQUITECTURA.md`.**
