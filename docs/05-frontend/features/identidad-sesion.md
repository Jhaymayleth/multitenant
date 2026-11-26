# Feature: identidad y sesión (frontend)

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/identidad-sesion.md`

## 1. Objetivo

Permitir que el CEO y el personal entren al panel con una sesión segura y que el sistema los lleve a su restaurante correcto.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Login | `/login` | Correo, contraseña y restaurante |
| Recuperar | `/recuperar` | Solicitar enlace |
| Restablecer | `/restablecer/{token}` | Nueva contraseña |
| Verificar | `/verificar` | Código de un solo uso |
| Cambio de tenant | modal | Elegir restaurante |

## 3. Flujos

### Login

1. El usuario ingresa correo, contraseña y slug del restaurante.
2. El frontend envía a `/auth/login`.
3. Si es correcto, redirige a `/admin`.
4. Si falla, muestra un mensaje genérico.

### Logout

1. Envía `/auth/logout`.
2. Limpia el estado local.
3. Redirige a `/login`.

### Guard

- Sin sesión, redirige a `/login`.
- Con sesión pero sin permiso, muestra “no autorizado”.
- Con tenant inactivo, muestra un mensaje y no permite operar.

## 4. Criterios de aceptación

- [ ] El formulario tiene `onSubmit` real.
- [ ] La cookie no se manipula desde JavaScript.
- [ ] `/admin` no se sirve sin sesión.
- [ ] El error de credenciales no revela si el correo existe.
- [ ] La recuperación funciona por correo.
- [ ] El cambio de tenant recarga el contexto.

## 5. Estado actual

El login es un formulario estático con botón `type="button"` y sin handler. El layout de `/admin` no tiene guard. No hay recuperación ni verificación.
