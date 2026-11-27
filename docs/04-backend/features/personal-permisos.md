# Feature: personal y permisos

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Decisión:** D-146
**Documento frontend:** `05-frontend/features/personal-permisos.md`

## 1. Objetivo

Permitir que el CEO cree empleados, les asigne un rol y controle su acceso sin compartir credenciales.

## 2. Alcance

- Listar personal.
- Pre-registrar empleado por correo.
- Asignar rol.
- Activar y desactivar.
- Revocar sesiones al desactivar.
- Matriz de permisos por rol.

## 3. Matriz aprobada (sin rol de cajero, D-145 y D-146)

| Capacidad | Owner | Admin | Mesero | Cocinero |
|---|---|---|---|---|
| Configurar restaurante | Sí | Delegado | No | No |
| Gestionar plan | Sí | No | No | No |
| Gestionar personal | Sí | Sí, sin owner | No | No |
| Editar menú | Sí | Sí | No | No |
| Gestionar mesas | Sí | Sí | Sí | No |
| Crear pedidos | Sí | Sí | Sí | No |
| Cambiar estado de cocina | Sí | Sí | Sí | Sí |
| Generar cobro del pedido | Sí | Sí | Sí | No |
| Consultar estado de pago | Sí | Sí | Sí | No |
| Gestionar reservas | Sí | Sí | Sí | No |
| Ver datos de clientes | Sí | Sí | Limitado | No |
| Ver reportes | Sí | Sí | No | No |

El pago se confirma por webhook de la pasarela del restaurante, no con una acción manual de caja.

## 4. Reglas de negocio

| ID | Regla |
|---|---|
| RN-121 | Solo el owner gestiona el plan y el rol owner. |
| RN-122 | El rol cliente no se asigna como empleado. |
| RN-123 | Un empleado se verifica con código en su primer acceso. |
| RN-124 | Desactivar revoca sesiones y conserva historial. |
| RN-125 | Los permisos no se heredan entre tenants. |
| RN-126 | El cocinero no ve datos personales ni precios. |
| RN-127 | No existe rol de cajero: Lixus no recibe dinero de los pedidos (D-145). |

## 5. API

| Método | Ruta | Estado |
|---|---|---|
| GET | `/tenant/staff` | Implementado |
| POST | `/tenant/staff` | Parcial |
| PATCH | `/tenant/staff/{id}` | No existe |
| POST | `/tenant/staff/{id}/deactivate` | No existe |

## 6. Datos

- `platform.users`: identidad.
- `platform.tenant_memberships`: rol y estado.
- `tenant.staff_profiles`: perfil local.

## 7. Criterios de aceptación

- [ ] El CEO crea un empleado y este puede iniciar sesión con su rol.
- [ ] El empleado solo ve las áreas permitidas.
- [ ] Desactivarlo impide el acceso de inmediato.
- [ ] El historial de pedidos y pagos se conserva.
- [ ] Un admin no puede ascenderse a owner.
- [ ] Un cocinero no ve datos personales.

## 8. Brecha actual

`POST /tenant/staff` genera un `user_id` huérfano y no crea membresía. El empleado no puede autenticarse.
