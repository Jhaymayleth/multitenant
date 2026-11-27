# Especificación técnica: BL-02 identidad y sesión

**Estado:** Especificación lista para implementar
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería
**Feature:** [`01-producto/backlog.md`](../01-producto/backlog.md) → BL-02
**Decisiones:** D-105 (cookie `httpOnly`), D-106 (tenant en servidor), D-117 (plataforma interina), D-123 (español), D-131 (accesibilidad en login), D-146 (roles), D-152 (contraseña de 8 caracteres), D-153 (código de 15 minutos)
**Fichas espejo:** [`04-backend/features/identidad-sesion.md`](../04-backend/features/identidad-sesion.md) · [`05-frontend/features/identidad-sesion.md`](features/identidad-sesion.md)

## 1. Objetivo

Cerrar el acceso al panel: login y logout reales, consulta del usuario con su restaurante y rol, cambio de tenant con nueva cookie, recuperación de contraseña y guards que impidan operar sin sesión o con un restaurante inactivo. La sesión se decide en el servidor y la cookie nunca se lee desde JavaScript.

## 2. Estado actual

- `POST /auth/login`, `POST /auth/logout` y `GET /auth/me` existen; `POST /auth/switch-tenant` devuelve una respuesta fija sin emitir token.
- La cookie `lixus_session` se emite con `httpOnly`, `SameSite=Lax`, `max_age=3600` y `secure=False` en código. En producción debe ir con `Secure` (RT-05).
- El login usa bcrypt, mensaje genérico en fallo y resuelve el tenant por `tenant_slug` o, si falta, por la primera membresía activa del usuario.
- `/auth/me` devuelve `full_name="Usuario Autenticado"` fijo (RT-09).
- `get_tenant_context` revalida en base de datos el tenant activo, la membresía activa y el schema antes de cada petición privada. El rol del token no se usa para autorizar: se toma de la membresía.
- `require_role` aplica los roles del tenant; no hay rol de cajero (D-145).
- No hay registro, recuperación, restablecimiento, verificación de correo ni revocación de token.
- No hay CSRF ni rate limiting (BL-16 y BL-18).
- El frontend tiene `/login` estático, con botón `type="button"` sin `onSubmit`; `/admin` y `/portal` no tienen guard.

## 3. Alcance de esta feature

Incluye:

1. Login y logout conectados a la API, con estados y errores comprensibles.
2. `/auth/me` con nombre real, tenant activo, rol y permisos derivados de la membresía.
3. Cambio de tenant que valida membresía y emite cookie nueva.
4. Recuperación y restablecimiento de contraseña con código de un solo uso por correo.
5. Cookie con `Secure` en producción y expiración coherente con la configuración.
6. Guards de `/admin` y `/portal`, incluido el mensaje de tenant inactivo.
7. Rechazo de empleados desactivados en cada petición privada.
8. Normalización de errores de autenticación en el cliente de BL-01.

Queda fuera:

- Registro público de clientes y verificación de correo para invitaciones de personal.
- Google como método de acceso (previsto, sin fecha).
- CSRF, rate limiting y revocación explícita por lista negra (BL-16 y BL-18). La desactivación de membresía ya corta el acceso.
- Sustituir la clave interina `X-Platform-Admin-Key` por JWT de plataforma (D-117 sigue vigente).
- Cambios en el contrato de menú, pedidos, mesas o sitio público.

## 4. Contrato

Base: `/api/v1`. Todas las rutas responden en español y usan `error.code`, `error.message` y `request_id` cuando exista. El cliente acepta también `detail` (RT-20).

### 4.1 Endpoints existentes

| Método | Ruta | Uso | Estado |
|---|---|---|---|
| POST | `/auth/login` | Inicia sesión, emite cookie | Implementado |
| POST | `/auth/logout` | Borra cookie | Implementado |
| GET | `/auth/me` | Usuario, tenant y rol | Parcial (nombre fijo) |
| POST | `/auth/switch-tenant` | Cambia de restaurante | Stub |

### 4.2 Endpoints a añadir

| Método | Ruta | Uso | Respuesta |
|---|---|---|---|
| POST | `/auth/forgot-password` | Envía código de restablecimiento | 202 sin revelar si el correo existe |
| POST | `/auth/reset-password` | Cambia contraseña con código | 200 + mensaje |

### 4.3 Cuerpos y respuesta de sesión

```text
Login:      { "email": string, "password": string, "tenant_slug": string | null }
Cambio:     { "tenant_id": uuid }
Olvidé:     { "email": string }
Restablecer:{ "code": string, "new_password": string }

/auth/me →
{
  "id": uuid,
  "email": string,
  "full_name": string,
  "active_tenant": { "id": uuid, "slug": string, "name": string, "status": string },
  "role": "owner" | "admin" | "waiter" | "cook",
  "permissions": string[]
}
```

Notas:

- `tenant_slug` sigue siendo opcional en login. Si se omite, se toma la primera membresía activa; si no hay ninguna, la respuesta es `403 NO_ACTIVE_TENANT`.
- `permissions` se calcula en servidor desde la matriz de D-146. El frontend solo lo usa para mostrar u ocultar acciones; la autoridad es el backend.
- Los nombres de roles son los del código (`waiter`, `cook`). La documentación puede decir «mesero» y «cocinero» como texto de interfaz.

### 4.4 Códigos de error de esta feature

`INVALID_CREDENTIALS`, `NO_ACTIVE_TENANT`, `TENANT_INACTIVE`, `INVALID_TOKEN`, `FORBIDDEN`, `MEMBERSHIP_INACTIVE`, `CODE_INVALID`, `CODE_EXPIRED`, `WEAK_PASSWORD`, `EMAIL_SEND_FAILED`.

`INVALID_CREDENTIALS` y `CODE_INVALID` no distinguen entre correo inexistente y correo existente (RN-111).

## 5. Diseño

### 5.1 Cadena de verificación

```text
Cookie lixus_session
  ├── firma JWT válida y no expirada → si no, 401
  ├── usuario activo en platform.users → si no, 401
  ├── tenant activo → si no, 403 TENANT_INACTIVE
  ├── membresía activa del usuario en ese tenant → si no, 403 MEMBERSHIP_INACTIVE
  ├── rol de la membresía → se toma de la base de datos, nunca del token
  └── set_config('search_path', tenant_schema, true) antes de consultar datos
```

Esta cadena ya existe en `get_tenant_context`; la feature la completa con el nombre real, el contexto de `/me` y el cambio de tenant.

### 5.2 Cookie y token

- Cookie: `httpOnly`, `SameSite=Lax`, `Secure` en producción, TTL de 60 minutos según `JWT_ACCESS_TOKEN_TTL_MINUTES`.
- El token incluye `sub`, `email`, `tenant_id` y `role` para trazabilidad; `role` se recalcula desde la membresía en cada petición.
- Logout borra la cookie. No se añade lista negra en esta feature (BL-18).
- Ningún token se guarda en `localStorage` (RN-115).

### 5.3 Cambio de tenant

1. El usuario elige un tenant entre sus membresías activas.
2. El backend comprueba que el tenant esté activo y que la membresía siga vigente.
3. Emite token nuevo con el `tenant_id` elegido y sobrescribe la cookie.
4. El frontend vuelve a pedir `/auth/me` y actualiza el contexto; no guarda el tenant en almacenamiento persistente.

### 5.4 Recuperación

- `forgot-password` crea un código de un solo uso en `platform.verification_codes`, guardado como hash, con caducidad de 15 minutos (D-153).
- El código viaja por `EmailProvider` (interfaz prevista en `03-arquitectura/integraciones.md`); el proveedor concreto está en PD-23 y no se fija aquí.
- `reset-password` valida el código, aplica bcrypt a la nueva contraseña e invalida el código.
- Longitud mínima: 8 caracteres para cualquier cuenta (D-152), igual que la regla vigente del schema.
- Respuesta de `forgot-password` siempre 202, sin decir si el correo existe.

## 6. Flujos

### 6.1 Login

1. El usuario escribe correo, contraseña y slug del restaurante.
2. `onSubmit` llama a `POST /auth/login`.
3. Con éxito se pide `/auth/me`, se guarda el contexto en memoria y se redirige a `/admin`.
4. Con fallo se muestra «No pudimos iniciar sesión. Revisa tus datos.»; no se revela si el correo existe.
5. Durante la petición el botón dice «Entrando…» y queda deshabilitado.

### 6.2 Guard de `/admin` y `/portal`

1. Al cargar el layout se consulta `/auth/me`.
2. Sin sesión (401) → `/login`.
3. Con tenant inactivo o membresía inactiva → pantalla «Restaurante no disponible», sin operación.
4. Con sesión válida pero rol sin permiso → «No tienes acceso a esta sección».
5. Con sesión válida → panel con el contexto del tenant.

El guard del portal usa la credencial de plataforma vigente (D-117). El portal no muestra datos operativos del restaurante.

### 6.3 Logout

1. `POST /auth/logout`.
2. Se limpia el contexto local.
3. Se redirige a `/login`.
4. Si falla la llamada, se limpia el contexto igualmente y se avisa.

### 6.4 Cambio de tenant

1. Desde el panel se abre la lista de restaurantes del usuario.
2. Se envía `POST /auth/switch-tenant` con `tenant_id`.
3. Se vuelve a pedir `/auth/me`; se recarga el panel con el nuevo contexto.
4. Si el tenant ya no está activo, se muestra el mensaje de tenant no disponible.

### 6.5 Recuperación

1. En `/recuperar` se pide el correo; siempre se muestra el mismo mensaje de confirmación.
2. El usuario recibe el código por correo.
3. En `/restablecer/{code}` escribe la nueva contraseña dos veces.
4. Con código válido se guarda y se redirige a `/login`; con código vencido se ofrece pedir uno nuevo.

## 7. Archivos a crear o modificar

| Archivo | Acción | Contenido |
|---|---|---|
| `backend/app/auth/router.py` | Modificar | `me` completo, `switch-tenant` real, forgot/reset |
| `backend/app/auth/service.py` | Modificar | Validación de membresía, emisión de token, códigos |
| `backend/app/auth/schemas.py` | Modificar | Contexto de `/me`, cuerpos nuevos |
| `backend/app/auth/repository.py` | Crear | Lectura y consumo de `verification_codes` |
| `backend/app/core/dependencies.py` | Modificar | Contexto con nombre, slug y permisos |
| `backend/app/core/config.py` | Modificar | Bandera `COOKIE_SECURE` derivada del entorno |
| `backend/tests/` | Crear | Pruebas de login, roles, switch y recuperación |
| `frontend/src/lib/auth.ts` | Crear o ampliar | Contexto de sesión, login, logout, switch, `me` |
| `frontend/src/app/(auth)/login/page.tsx` | Modificar | `onSubmit` y estados |
| `frontend/src/app/(auth)/recuperar/page.tsx` | Crear | Solicitud de código |
| `frontend/src/app/(auth)/restablecer/[code]/page.tsx` | Crear | Nueva contraseña |
| `frontend/src/app/(ceo-portal)/admin/layout.tsx` | Modificar | Guard de sesión, tenant y rol |
| `frontend/src/app/(lixus)/portal/layout.tsx` | Modificar | Guard de plataforma |

No se modifica el contrato de los dominios de negocio ni el middleware de `/r/{slug}` (BL-01).

## 8. Estados obligatorios por pantalla

| Pantalla | Cargando | Vacío | Error | Sin permiso |
|---|---|---|---|---|
| `/login` | «Entrando…» | No aplica | Credenciales genéricas | No aplica |
| `/admin` | Esqueleto del layout | No aplica | Reintento | «No tienes acceso a esta sección» |
| `/portal` | Esqueleto del layout | «Sin tenants» | Reintento | Mensaje claro |
| Cambio de tenant | «Cambiando…» | «No tienes otros restaurantes» | Reintento | No aplica |
| `/recuperar` | «Enviando…» | No aplica | Confirmación genérica | No aplica |
| `/restablecer/{code}` | «Guardando…» | No aplica | Código vencido o contraseña débil | No aplica |

Las etiquetas van en español y conservan foco visible para teclado (D-131).

## 9. Pruebas requeridas

1. Login correcto emite cookie `httpOnly`, `SameSite=Lax` y `Secure` en configuración de producción.
2. Login incorrecto devuelve `401 INVALID_CREDENTIALS` sin revelar si el correo existe.
3. Sin cookie, una ruta privada devuelve `401`.
4. Con cookie del tenant A, un recurso del tenant B devuelve `403` o `404`.
5. Un usuario sin membresía activa no entra; un empleado desactivado pierde el acceso.
6. `/me` devuelve nombre real, slug del tenant y rol de la membresía.
7. `switch-tenant` valida la membresía y emite cookie nueva; el token anterior deja de ser la sesión activa en el navegador.
8. `forgot-password` devuelve 202 tanto si el correo existe como si no.
9. Un código de restablecimiento se puede usar una sola vez y vence a los 15 minutos (D-153).
10. Una contraseña por debajo del mínimo vigente se rechaza con `WEAK_PASSWORD`.
11. Logout borra la cookie y limpia la sesión aunque falle la petición.
12. `/admin` sin sesión redirige a `/login`; con tenant inactivo bloquea la operación.
13. Ningún token aparece en `localStorage`, `sessionStorage` ni en la URL.
14. Un consumidor con rol `cook` no ve acciones de configuración; un `waiter` no ve acción de publicación del sitio.

## 10. Criterios de aceptación

- [ ] Login, logout y `/auth/me` funcionan con datos reales.
- [ ] `/me` ya no devuelve el nombre fijo.
- [ ] `switch-tenant` emite token nuevo y valida membresía.
- [ ] Recuperación y restablecimiento funcionan con código de un solo uso.
- [ ] La cookie es `Secure` en producción y sigue siendo `httpOnly`.
- [ ] La membresía y el tenant se revalidan en cada petición privada.
- [ ] Los guards de `/admin` y `/portal` cubren sesión, tenant y rol.
- [ ] El error de credenciales no filtra existencia del correo.
- [ ] No se guarda ningún token en el navegador.
- [ ] Los mensajes están en español y no muestran detalles internos.

## 11. Dependencias

- BL-01: `apiFetch` y `AppError`; sin ellos no hay cliente HTTP común.
- D-105, D-106 y D-146 cerrados; D-117 mantiene la credencial interina de plataforma.
- BL-14 define el proveedor de correo; PD-23 sigue abierto y el proveedor concreto no se inventa aquí.
- Configuración de entorno en [`06-infra-ops/variables-entorno.md`](../06-infra-ops/variables-entorno.md): `JWT_SECRET`, `JWT_ACCESS_TOKEN_TTL_MINUTES`, la variable propuesta `COOKIE_SECURE` y `EMAIL_*`.
- Deuda RT-05, RT-07, RT-09 y RT-20 en [`07-calidad/deuda-tecnica.md`](../07-calidad/deuda-tecnica.md).
- BL-16 y BL-18 cierran rate limiting, CSRF y revocación.

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Cookie sin `Secure` en producción | Derivar la bandera del entorno y comprobarlo en CI de producción |
| Token con rol desactualizado | Recalcular rol desde la membresía en cada petición |
| Empleado desactivado con sesión abierta | Rechazar la petición al comprobar membresía, sin depender del token |
| Cambio de tenant con membresía cancelada | Validar tenant y membresía antes de emitir cookie |
| Proveedor de correo sin definir | Encapsular en `EmailProvider`; en local usar Mailpit sin inventar proveedor |
| Códigos reutilizables | Guardar hash, marcar consumido y aplicar TTL |
| Errores con formatos distintos | Normalizar `detail` y `error` en `AppError` |
| Mensaje de recuperación que filtre cuentas | Respuesta 202 idéntica para correo existente y inexistente |

## 13. Definición de terminado

Se considera terminada cuando se cumplen los criterios de aceptación, pasan las pruebas del punto 9, CI pasa con lint, tests y build, y se verifica manualmente un ciclo completo: entrar con un tenant, consultar `/me`, cambiar a otro tenant donde el usuario tenga membresía, cerrar sesión, recuperar contraseña por correo local y volver a entrar con la nueva contraseña.
