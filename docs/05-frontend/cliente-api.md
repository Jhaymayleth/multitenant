# Especificación técnica: BL-01 frontend conectado

**Estado:** Especificación lista para implementar
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería
**Feature:** [`01-producto/backlog.md`](../01-producto/backlog.md) → BL-01
**Decisiones:** D-105 (cookie `httpOnly`), D-106 (tenant en servidor), D-124 (`/r/{slug}`)

## 1. Objetivo

Que el frontend deje de ser una maqueta y consuma la API real: login funcional, sesión mantenida por cookie, guards de rutas privadas y errores comprensibles. Es la condición para que cualquier otra pantalla tenga datos reales.

## 2. Estado actual

- Las páginas son estáticas; no hay `fetch` ni cliente HTTP.
- No existe `frontend/src/lib/api.ts`.
- El login tiene botón `type="button"` sin `onSubmit`.
- `/admin` no tiene guard de sesión ni de rol.
- No hay estados de carga, error ni vacío.
- El middleware actual resuelve subdominios; la decisión vigente es `/r/{slug}` (D-124).

## 3. Alcance de esta feature

Incluye:

1. Cliente HTTP único para todas las llamadas.
2. Login y logout conectados.
3. Consulta de usuario actual (`/auth/me`) y contexto de tenant.
4. Guard de sesión en `/admin` y `/portal`.
5. Manejo uniforme de errores y estados de carga.
6. Ajuste del middleware a rutas por slug, sin subdominios.

Queda fuera:

- Recuperación de contraseña, verificación de correo y cambio de tenant (BL-02).
- CSRF, revocación de sesión y rate limiting (deuda P0/P1, ver `07-calidad/deuda-tecnica.md`).
- Conexión de menú, pedidos, mesas, reservas y página pública (BL-03 a BL-06).
- Cualquier cambio en el backend.

## 4. Contrato consumido

Base: `NEXT_PUBLIC_API_URL` (definida en build; ver `06-infra-ops/variables-entorno.md`).

| Método | Ruta | Uso en el frontend | Respuesta |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Iniciar sesión | 200 + cookie `lixus_session` |
| POST | `/api/v1/auth/logout` | Cerrar sesión | 204 |
| GET | `/api/v1/auth/me` | Contexto del usuario | `{ id, email, role, tenant: { id, slug, status } }` |
| GET | `/api/v1/health` | Comprobación de salud | `{ status, app, version, environment }` |

Notas:

- El frontend **no guarda tokens** en `localStorage` ni en memoria persistente. La cookie la maneja el navegador (D-105).
- Toda petición privada usa `credentials: 'include'`.
- El backend aún devuelve `{"detail": "..."}` en algunos errores; el cliente debe aceptar tanto `detail` como `error.code` + `error.message`.
- `/auth/me` devuelve hoy un nombre genérico (deuda RT-09); esta feature no lo corrige, solo consume `role`, `tenant` y `status`.

## 5. Diseño del cliente HTTP

Archivo propuesto: `frontend/src/lib/api.ts`.

```text
apiFetch(path, options)
  ├── URL = NEXT_PUBLIC_API_URL + path
  ├── headers: Content-Type: application/json (si hay body)
  ├── credentials: 'include'
  ├── timeout configurable (propuesto: 10 s)
  ├── parsea JSON cuando existe
  ├── si status >= 400 → lanza AppError
  └── si la respuesta no es JSON → lanza AppError con código PARSE_ERROR
```

`AppError` propuesto:

```text
{
  code: string,        // INVALID_CREDENTIALS | TENANT_INACTIVE | FORBIDDEN | NETWORK_ERROR ...
  message: string,     // texto para el usuario, en español
  status: number,
  requestId?: string   // cuando el backend lo devuelva
}
```

Reglas:

- Los códigos anteriores son propuestos; si el backend no los envía, se derivan del `status`.
- El mensaje al usuario nunca muestra trazas, SQL ni URLs internas.
- `requestId` se muestra como detalle de soporte, no en el texto principal.

## 6. Flujos

### 6.1 Login

1. El usuario escribe correo, contraseña y slug del restaurante.
2. `onSubmit` llama a `POST /auth/login`.
3. Si es correcto: se llama a `/auth/me`, se guarda el contexto en el estado de la sesión y se redirige a `/admin`.
4. Si falla: mensaje genérico («No pudimos iniciar sesión. Revisa tus datos.»). No se revela si el correo existe.
5. Durante la petición: botón deshabilitado y estado «Entrando…».

### 6.2 Logout

1. `POST /auth/logout`.
2. Se limpia el estado local de sesión.
3. Se redirige a `/login`.
4. Si la llamada falla, se limpia el estado local de todos modos y se avisa.

### 6.3 Guard de `/admin`

1. Al cargar el layout, se consulta `/auth/me`.
2. Sin sesión (401) → redirección a `/login`.
3. Con sesión pero tenant inactivo → pantalla de «Restaurante no disponible», sin operación.
4. Con sesión y tenant activo → se renderiza el panel con el contexto del tenant.
5. Si el rol no permite el área, se muestra «No tienes acceso a esta sección», no un error técnico.

### 6.4 Guard de `/portal`

Igual flujo, con la credencial de plataforma vigente (`X-Platform-Admin-Key` interino, D-117). El portal no debe enlazar a datos operativos del restaurante.

### 6.5 Middleware

- Eliminar la resolución por subdominio.
- La página pública se sirve bajo `/r/{slug}` (D-124).
- El middleware no decide permisos; solo normaliza la ruta. La autoridad es el backend.

## 7. Archivos a crear o modificar

| Archivo | Acción | Contenido |
|---|---|---|
| `frontend/src/lib/api.ts` | Crear | `apiFetch` y `AppError` |
| `frontend/src/lib/auth.ts` | Crear | Contexto de sesión, `login`, `logout`, `refresh` |
| `frontend/src/app/(auth)/login/page.tsx` | Modificar | `onSubmit`, estados y redirección |
| `frontend/src/app/(ceo-portal)/admin/layout.tsx` | Modificar | Guard de sesión y tenant |
| `frontend/src/app/(lixus)/portal/layout.tsx` | Modificar | Guard de plataforma |
| `frontend/src/middleware.ts` | Modificar | Rutas `/r/{slug}`; sin subdominios |

No se crea `lib/api.ts` en el backend ni se cambia el contrato de la API.

## 8. Estados obligatorios por pantalla

| Pantalla | Cargando | Vacío | Error | Sin permiso |
|---|---|---|---|---|
| Login | Botón con «Entrando…» | No aplica | Mensaje genérico + reintento | No aplica |
| `/admin` | Esqueleto del layout | No aplica | Error con reintento | Mensaje claro |
| `/portal` | Esqueleto del layout | «Sin tenants» | Error con reintento | Mensaje claro |

## 9. Pruebas requeridas

1. Login correcto redirige a `/admin` y muestra el contexto del tenant.
2. Login incorrecto muestra mensaje genérico.
3. Sin sesión, `/admin` redirige a `/login`.
4. Con sesión de otro tenant, no se muestran datos del primero.
5. Tenant inactivo bloquea la operación.
6. Logout limpia la sesión aunque falle la llamada.
7. Un error 500 del backend se convierte en mensaje comprensible.
8. Ningún token aparece en `localStorage`.
9. La ruta pública funciona con `/r/{slug}` y no con subdominio.
10. La cookie de sesión viaja en todas las peticiones privadas.

## 10. Criterios de aceptación

- [ ] Existe `frontend/src/lib/api.ts` y lo usan login, logout y `/me`.
- [ ] El formulario de login tiene `onSubmit` real.
- [ ] `/admin` no se sirve sin sesión válida.
- [ ] El error de credenciales no filtra existencia del correo.
- [ ] Los mensajes de error están en español y no muestran internos.
- [ ] Hay estados de carga, error y sin permiso.
- [ ] El middleware usa `/r/{slug}`.
- [ ] No se guarda ningún token en el navegador.
- [ ] La feature tiene al menos una prueba automatizada o verificación manual documentada.

## 11. Dependencias

- Backend: `/auth/login`, `/auth/logout`, `/auth/me` ya existen.
- `NEXT_PUBLIC_API_URL` definida antes del build.
- Deuda RT-01, RT-05, RT-06 y RT-09 en `07-calidad/deuda-tecnica.md`.
- BL-02 completa recuperación, verificación y cambio de tenant.

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| El backend devuelve formatos de error distintos | Normalizar `detail` y `error` en el cliente |
| `/auth/me` devuelve nombre genérico | No mostrar nombre hasta BL-02 |
| CSRF aún no existe | Documentar como deuda; no bloquear el login |
| Middleware con lógica de subdominio | Ajustar en esta feature, no en otra posterior |
| Cookie `Secure=False` en producción | Corregir en backend (RT-05); el frontend no puede resolverlo |

## 13. Definición de terminado

Se considera terminada cuando se cumple el criterio 10, pasa CI con lint y build, y se verifica manualmente un ciclo completo: abrir `/login`, entrar, ver `/admin`, salir y volver a `/login`.
