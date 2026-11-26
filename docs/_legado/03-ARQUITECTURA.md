# 03 — Arquitectura del proyecto Lixus

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes  
**Versión:** 0.2  
**Estado:** Diseño base para implementación; los puntos marcados como *PoC* deben validarse antes de cerrar el código  
**Decisiones aplicadas:** D-042 a D-046, D-052, D-061, D-065, D-074, D-075, D-076  
**Última actualización:** 22 de octubre de 2026

---

## 1. Vista general

Lixus es un **monolito modular** con dos aplicaciones desplegables y servicios de apoyo.

## 1.1 Mapa documental

| Documento | Contenido | Cuándo leerlo |
|---|---|---|
| `00-INDICE.md` | Este índice: navegación, estado y convenciones. | Primero, siempre |
| `01-REQUERIMIENTOS.md` | Requisitos académicos, funcionales, no funcionales, reglas y criterios de aceptación. | Antes de planificar o implementar |
| `02-DECISIONES.md` | Registro D-001 a D-076 con estado, motivo y consecuencias. | Antes de proponer un cambio |
| `03-ARQUITECTURA.md` | Componentes, multitenencia, resolución del tenant, migraciones, renderizado. | Antes de escribir código |
| `04-MODULOS.md` | Módulos funcionales, permisos, endpoints y reglas de negocio. | Al implementar cada módulo |
| `05-PENDIENTES.md` | Decisiones abiertas, contradicciones y riesgos con recomendación. | En cada reunión de avance |
| `06-HISTORIAL.md` | Cómo evolucionó la documentación y qué decisiones cambiaron. | Para entender el porqué |
| `07-MODELO-DATOS.md` | Tablas globales y por tenant, relaciones, índices y migraciones. | Al crear modelos y migraciones |
| `08-SEGURIDAD-Y-ACCESO.md` | Autenticación, sesión, autorización, CSRF, QR anónimo, IA y pruebas. | Al implementar auth y permisos |
| `09-ROBUSTEZ.md` | Idempotencia, rate limiting y concurrencia con pruebas. | Antes de la fase de robustez |
| `10-ENTORNO-Y-DESPLIEGUE.md` | Docker Compose, variables, CI/CD, R2 y despliegue. | Al montar el entorno |
| `11-PLAN-DE-IMPLEMENTACION.md` | Fases, orden de trabajo, definición de terminado y recortes. | Al planificar la semana |
| `12-ENTREGABLES-Y-EVALUACION.md` | Rúbrica, README, guion de sustentación y preguntas. | Antes de la entrega |
| `13-ROUTE-MVP.md` | Ruta de desarrollo orientada al enunciado y al cumplimiento del MVP. | Antes de arrancar la primera fase |

---



```
┌──────────────────────────────────────────────────────────────────────┐
│                        Navegador del usuario                         │
│   Sitio público · Panel del restaurante · Portal de tenants (Lixus)  │
│   Sitio de solicitud de nuevos tenants (Lixus)                       │
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

## 2. Resolución del tenant desde el servidor

El tenant nunca se decide desde el cliente. El backend siempre lo resuelve desde el contexto válido de la petición: subdominio, slug, sesión o token, según el caso.

Esto quiere decir que:

- la web pública del restaurante carga los datos correctos porque el backend se fija en el subdominio o en el contexto válido que llega;
- el panel del CEO solo funciona si la sesión del usuario es del CEO de ese tenant;
- la solicitud de nuevo tenant es solo la entrada al flujo de Lixus, no un tenant creado automáticamente.

Esta regla es más importante que la forma del subdominio o de la ruta.

## 3. Modelo multitenant

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

La API never corre como superusuario ni como dueño de los schemas. Esto convierte un error de `search_path` en un error de permisos visible, no en una fuga silenciosa.

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

### 3.1 Organización por dominio

El backend se organiza por dominio, con un paquete por responsabilidad principal:

```
backend/
├── app/
│   ├── core/                # configuración, seguridad, base de datos, errores
│   ├── platform/            # tenants, membresías, planes, solicitudes, Lixus
│   ├── auth/                # login, tokens, cookies, verificación, recuperación
│   ├── menus/               # categorías y productos del menú
│   ├── sites/               # configuración de la web pública del restaurante
│   ├── orders/              # pedidos y líneas
│   ├── reservations/        # reservas
│   ├── payments/            # estados de pago y comprobantes
│   ├── webhooks/            # eventos entrantes del proveedor de pago
│   ├── public/              # datos públicos del tenant, si se separa
│   ├── audit/               # eventos
│   └── shared/              # utilidades, paginación, validaciones
├── migrations/
│   ├── platform/
│   └── tenant/
└── tests/
    ├── unit/
    ├── integration/
    └── security/            # aislamiento, IDOR, autorización
```

Cada dominio expone sus responsabilidades y se integra desde el router principal cuando está listo. Las reglas de negocio viven en la capa de servicio del dominio, no en el router ni en el ORM.

### 3.2 Capas y responsabilidades

| Capa | Hace | No hace |
|---|---|---|
| Router | Valida entrada HTTP, aplica dependencias, devuelve códigos | Reglas de negocio |
| Service | Orquesta reglas, transacciones, permisos de negocio | SQL directo |
| Repository | Consultas y persistencia | Decidir permisos |
| Modelos | Estructura de datos | Lógica de negocio |### 3.3 Subdominios y rutas

- **Web pública del restaurante:** subdominio por restaurante como `restaurante1.tudominio.com`.
- **Panel del CEO:** ruta privada dentro del mismo subdominio, como `restaurante1.tudominio.com/app` o `restaurante1.tudominio.com/admin`.
- **Sitio de solicitud de Lixus:** sitio separado como `solicita.tudominio.com`.
- **Panel de Lixus:** área privada de Lixus, separada conceptualmente del resto.

### 3.4 Resolución del tenant en el frontend

El frontend no decide el tenant. El tenant se resuelve desde la petición que llega al backend: por subdominio, por slug, por sesión o por token, según el caso. Lo que el frontend envía es solo entrada; lo que importa es lo que el backend verifica.

La web pública del restaurante carga los datos correctos porque el backend se fija en el subdominio o en el contexto válido que llega.

El panel del CEO solo funciona si la sesión del usuario es del CEO de ese tenant.

### 3.5 Seguridad de la arquitectura

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


## 4. Fronteras entre las tres caras del proyecto

### 4.1 Web pública del restaurante

- Subdominio del restaurante.
- Datos del tenant visibles.
- Sin login obligatorio.
- Plantilla común, datos distintos por tenant.

### 4.2 Panel del CEO del restaurante

- Ruta privada dentro del mismo subdominio.
- Sesión y permisos.
- Solo el CEO del tenant.
- Lo que el CEO administra del restaurante.

### 4.3 Sitio y panel de Lixus

- Sitio separado para la solicitud.
- Panel privado para la gestión del SaaS.
- Lixus controla:
  - solicitudes
  - tenants
  - membresías
  - pagos de membresía
  - creación de tenant
  - contraseña inicial
  - notificaciones al futuro CEO

---

## 5. Decisiones de arquitectura todavía abiertas

| Tema | Estado | Documento |
|---|---|---|
| Modalidad académica A/B | Por confirmar con el docente | `05-PENDIENTES.md` P-01 |
| Caja ligera y comprobantes | Definido (D-070) | — |
| URL pública: subdominio o ruta | Definido: subdominio público | — |
| Panel del CEO: ruta privada | Definido | — |
| Sitio de solicitud de Lixus | Definido: sitio separado | — |
| Reservas: tolerancia y no-show | Por definir | P-07 |
| Domicilios: cobertura, costo y entrega | Por definir | P-23 |
| Proveedor de correo | Por definir | P-11 |
| Pasarela de suscripciones | Por definir | P-09 |
| Arquitectura AWS concreta | Por definir | P-14 |

---

## 6. Pruebas de arquitectura obligatorias (PoC)

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
