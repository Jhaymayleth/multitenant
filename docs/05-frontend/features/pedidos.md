# Feature: pedidos (frontend)

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/pedidos.md`

## 1. Objetivo

Que el mesero tome el pedido una vez y que cocina y caja trabajen con la misma información.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Pedidos | `/admin/pedidos` | Lista por estado |
| Nuevo pedido | `/admin/pedidos/nuevo` | Mesa, productos y notas |
| Detalle | `/admin/pedidos/{id}` | Líneas, total e historial |
| Cocina | `/admin/pedidos/cocina` | Cola de preparación |

## 3. Flujo del mesero

1. Elegir mesa.
2. Buscar producto.
3. Ajustar cantidad y notas.
4. Ver el total calculado.
5. Confirmar y enviar a cocina.

## 4. Flujo de cocina

1. Ver pedidos pendientes por hora y mesa.
2. Marcar “en preparación”.
3. Marcar “listo”.
4. El mesero marca “servido”.

## 5. Criterios de aceptación

- [ ] El pedido no se envía sin líneas.
- [ ] El total coincide con el backend.
- [ ] El precio no se edita desde el cliente.
- [ ] Cocina no ve datos personales.
- [ ] El cambio de estado se refleja sin recargar.
- [ ] Un pedido pagado no se edita.
- [ ] El pedido se ve bien en tablet.

## 6. Estado actual

La página es informativa. No hay formulario, carrito, total ni tablero de cocina.
