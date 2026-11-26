# Feature: pagos y comprobantes (frontend)

**Estado:** NO INICIADO
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/pagos-comprobantes.md`

## 1. Objetivo

Que el cajero cierre la cuenta, registre el pago y entregue un comprobante sin salir del panel.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Caja | `/admin/caja` | Mesas pendientes de pago |
| Cobro | `/admin/caja/{orderId}` | Detalle, método y confirmación |
| Comprobante | `/r/{slug}/comprobante/{token}` | Vista pública |
| Historial | `/admin/caja/historial` | Pagos del día |

## 3. Flujo de cobro

1. Elegir mesa o pedido.
2. Revisar líneas y total.
3. Elegir efectivo o pago registrado.
4. Confirmar.
5. La mesa queda disponible.
6. Mostrar o enviar el comprobante.

## 4. Criterios de aceptación

- [ ] El total mostrado coincide con el pedido.
- [ ] No se puede cobrar dos veces.
- [ ] Al confirmar, la mesa se libera.
- [ ] El comprobante se descarga por QR.
- [ ] El comprobante muestra número, fecha, detalle y total.
- [ ] El historial se filtra por día.

## 5. Estado actual

La página es informativa. No hay cobro, confirmación ni comprobante.
