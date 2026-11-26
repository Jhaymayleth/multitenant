# Feature: plataforma y tenants (frontend)

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/plataforma-tenants.md`

## 1. Objetivo

Que el equipo Lixus pueda ver, verificar y administrar restaurantes desde el portal sin usar la API a mano.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Resumen | `/portal` | Contadores y estado del servicio |
| Tenants | `/portal/tenants` | Lista, filtro y búsqueda |
| Detalle | `/portal/tenants/{id}` | Datos, estado y verificación |
| Planes | `/portal/planes` | Catálogo y capacidades |

## 3. Flujos

### Verificar un restaurante

1. Abrir el detalle.
2. Revisar datos del negocio y contacto.
3. Aprobar o cancelar con motivo.
4. Confirmar la acción.
5. Ver el estado actualizado y el registro de auditoría.

### Alta asistida

1. Recibir la solicitud.
2. Crear el tenant desde el portal.
3. Verificar.
4. Enviar acceso al CEO.
5. Confirmar que puede iniciar sesión.

## 4. Componentes

- `TenantTable`.
- `StatusBadge` para `provisioning`, `pending_verification`, `active`, `cancelled`.
- `ConfirmDialog` para aprobar o cancelar.
- `EmptyState` cuando no hay solicitudes.

## 5. Estados

- Cargando lista.
- Sin tenants.
- Error de clave de plataforma.
- Tenant en provisión.
- Verificación fallida.

## 6. Criterios de aceptación

- [ ] La lista muestra nombre, slug, estado y fecha.
- [ ] El detalle muestra el schema sin exponer datos operativos.
- [ ] Aprobar cambia el estado a activo.
- [ ] Cancelar pide motivo.
- [ ] Sin clave, el portal muestra un error claro.
- [ ] La acción queda auditada.

## 7. Estado actual

El portal muestra contadores en cero y páginas informativas. No consume la API ni tiene formulario de verificación.
