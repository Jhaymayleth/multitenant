# Feature: pedidos

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Decisiones:** D-110, D-113
**Documento frontend:** `05-frontend/features/pedidos.md`

## 1. Objetivo

Registrar lo que el cliente pidió, calcular el total correcto y que cocina y cobro trabajen sobre la misma información.

## 2. Alcance

- Pedido de mesa creado por el mesero.
- Líneas con producto, cantidad, precio congelado y notas.
- Estados de preparación y de pago independientes.
- Cola de cocina por mesa.
- Pedido a domicilio para cliente registrado, con zonas y tarifa fija (D-147).
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
| RN-159 | El domicilio usa zonas y tarifa fija del restaurante, con entrega propia y cobro por su pasarela (D-147). |

## 4. Estados

Preparación: `pending → preparing → ready → served`.
Pago: `unpaid → paid → refunded` (reembolso fuera de la versión inicial).

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
