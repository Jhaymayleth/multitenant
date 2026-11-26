# Feature: identidad y sesión

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Decisiones:** D-105, D-106
**Documento frontend:** `05-frontend/features/identidad-sesion.md`

## 1. Objetivo

Dar acceso seguro al panel del restaurante y a la administración de Lixus, con sesión en cookie `httpOnly` y tenant resuelto en el servidor.

## 2. Alcance

- Login con correo y contraseña.
- Logout.
- Consulta del usuario actual.
- Cambio de tenant.
- Recuperación de contraseña (pendiente).
- Registro de cliente (pendiente).
- Verificación de correo (pendiente).
- Google para clientes (previsto).

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-111 | El login falla con mensaje genérico. |
| RN-112 | El tenant y la membresía se revalidan en cada petición. |
| RN-113 | Un empleado desactivado no puede operar. |
| RN-114 | Cambiar de tenant emite un token nuevo. |
| RN-115 | El token no se guarda en `localStorage`. |
| RN-116 | La cookie es `httpOnly` y `Secure` en producción. |

## 4. API

| Método | Ruta | Estado |
|---|---|---|
| POST | `/auth/login` | Implementado |
| POST | `/auth/logout` | Implementado |
| GET | `/auth/me` | Parcial (nombre genérico) |
| POST | `/auth/switch-tenant` | Stub |
| POST | `/auth/register` | No existe |
| POST | `/auth/forgot-password` | No existe |
| POST | `/auth/reset-password` | No existe |

## 5. Datos

- `platform.users`: identidad global, hash y estado.
- `platform.tenant_memberships`: rol y estado.
- `platform.verification_codes`: códigos de un solo uso.
- Redis: revocación y rate limiting (pendiente).

## 6. Criterios de aceptación

- [ ] Login correcto emite cookie y permite acceder al panel.
- [ ] Login incorrecto no revela si el correo existe.
- [ ] Sin cookie, una ruta privada responde 401.
- [ ] Con cookie de A, una ruta de B responde 403.
- [ ] Logout invalida la sesión de verdad.
- [ ] Un empleado desactivado pierde acceso.
- [ ] Cambio de tenant emite cookie nueva y valida membresía.
- [ ] Recuperación de contraseña funciona por correo.

## 7. Brechas actuales

- `secure=False` en el código.
- Sin CSRF.
- Sin revocación de JWT.
- `switch-tenant` no hace nada.
- `/me` devuelve nombre genérico.
- Sin registro ni recuperación.

## 8. Dependencias

- Correo transaccional.
- Rate limiting.
- Auditoría.
