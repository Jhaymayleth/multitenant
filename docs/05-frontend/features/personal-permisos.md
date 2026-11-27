# Feature: personal y permisos (frontend)

**Estado:** NO INICIADO
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/personal-permisos.md`

## 1. Objetivo

Que el CEO vea quién trabaja en el restaurante, qué rol tiene y pueda dar o quitar acceso sin compartir contraseñas.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Personal | `/admin/personal` | Lista de empleados |
| Invitar | modal | Correo y rol |
| Detalle | `/admin/personal/{id}` | Rol, estado e historial |

## 3. Contenido de la lista

- Nombre.
- Correo.
- Rol.
- Estado (activo, pendiente, inactivo).
- Último acceso.
- Acciones: cambiar rol, desactivar.

## 4. Flujos

### Invitar

1. El CEO escribe el correo.
2. Elige un rol entre administrador, mesero y cocinero; no existe el rol de cajero (D-145).
3. El backend crea la membresía y envía el código.
4. El empleado verifica y entra.

### Desactivar

1. Confirmar con el nombre.
2. Explicar que se revoca el acceso.
3. Conservar el historial.

## 5. Criterios de aceptación

- [ ] El CEO ve solo el personal de su restaurante.
- [ ] No puede asignar el rol owner a otro.
- [ ] El rol cliente no aparece como opción de empleado.
- [ ] Desactivar pide confirmación.
- [ ] El empleado desactivado no puede entrar.
- [ ] La interfaz respeta la matriz de permisos y no ofrece el rol de cajero (D-145).

## 6. Estado actual

No existe pantalla de personal. El backend solo lista y pre-registra con un usuario huérfano.
