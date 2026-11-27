# Feature: pedidos

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Decisiones:** D-110, D-113, D-155, D-156
**Documento frontend:** `05-frontend/features/pedidos.md`
**Especificación de la feature:** [`05-frontend/pedidos-api.md`](../../05-frontend/pedidos-api.md) (BL-04)

## 1. Objetivo

Registrar lo que el cliente pidió, calcular el total correcto y que cocina y cobro trabajen sobre la misma información.

## 2. Alcance

- Pedido de mesa creado por el mesero.
- Líneas con producto, cantidad, precio congelado y notas.
- Estados de preparación y de pago independientes.
- Cola de cocina por mesa.
- Registro simple de pedido a domicilio, sin zonas, tarifa ni seguimiento; la entrega la resuelve el restaurante fuera de Lixus (D-155).
- Trazabilidad de cambios.

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-151 | El pedido debe tener al menos una línea. |
| RN-152 | El precio se toma de la base de datos, no del cliente. |
| RN-153 | El total se calcula en el servidor. |
| RN-154 | El nombre y el precio se congelan en la línea. |
| RN-155 | La mesa y la sesión deben pertenecer al tenant. |
| RN-156 | Pedido de mesa y domicilio no se mezclan. |
| RN-157 | Un pedido pagado no se edita. |
| RN-158 | No se aplican impuestos, propinas ni descuentos. |
| RN-159 | El domicilio no tiene logística en Lixus: sin zonas, tarifa ni seguimiento. El restaurante lo resuelve con un servicio externo (D-155). |

## 4. Estados

Los valores de la columna `status` son `draft`, `confirmed`, `in_preparation`, `ready`, `served`, `out_for_delivery`, `delivered`, `closed` y `cancelled`. Los nombres «pendiente», «preparando», «listo» y «servido» son etiquetas de interfaz para esos valores. La transición detallada está en [`05-frontend/pedidos-api.md`](../../05-frontend/pedidos-api.md).

Pago: `unpaid`, `pending`, `paid`, `refunded` y `not_applicable` (reembolso fuera de la versión inicial).

## 5. API

| Método | Ruta | Estado |
|---|---|---|
| GET | `/tenant/orders` | Implementado |
| POST | `/tenant/orders` | Parcial |
| GET | `/tenant/orders/{id}` | Implementado |
| PATCH | `/tenant/orders/{id}/status` | No existe |
| POST | `/tenant/orders/{id}/items` | No existe |

## 6. Datos

- `tenant.orders`: mesa, sesión, estado, total, moneda, timestamps.
- `tenant.order_items`: producto, nombre, precio, cantidad, notas.

## 7. Criterios de aceptación

- [ ] Un pedido con dos líneas devuelve el total correcto.
- [ ] Cambiar el precio del producto no altera un pedido ya creado.
- [ ] Un pedido sin líneas se rechaza.
- [ ] Cocina ve mesa, líneas y notas, sin datos personales.
- [ ] El mesero cambia el estado y queda registrado.
- [ ] Un pedido de otro tenant responde 404/403.
- [ ] El pago confirmado no borra el pedido.

## 8. Brecha actual

El servicio crea la cabecera con `total_cents=0` e ignora las líneas. No hay endpoint de cambio de estado. Es el bloqueo P0 más importante después del frontend.
