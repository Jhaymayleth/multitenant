# Feature: cobro de pedidos y comprobantes (frontend)

**Estado:** NO INICIADO
**Dueño:** Ingeniería
**Decisiones:** D-140, D-145
**Documento backend:** `04-backend/features/pagos-comprobantes.md`

## 1. Objetivo

Que el restaurante cobre el pedido con su propia pasarela y entregue un comprobante, sin una pantalla de caja ni un rol de cajero.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Configuración de cobro | `/admin/configuracion/cobro` | Conectar la pasarela del restaurante |
| Cobro del pedido | `/admin/pedidos/{id}/pagar` | Botón de pago y estado |
| Pago del cliente | `/r/{slug}/pedido/{id}/pagar` | Pasarela del restaurante |
| Comprobante | `/r/{slug}/comprobante/{token}` | Vista pública |
| Historial | `/admin/pedidos/cobros` | Cobros del día |

No hay pantalla `/admin/caja` ni acción de “registrar pago en efectivo”.

## 3. Flujo de cobro

1. El mesero o el cliente abre el pedido.
2. Lixus muestra el total calculado en el servidor.
3. El botón “Pagar” envía al cobro de la pasarela del restaurante.
4. El cliente elige el método de pago en esa pasarela.
5. El dinero llega a la cuenta del restaurante.
6. El webhook confirma y Lixus libera la mesa.
7. Se muestra o envía el comprobante operativo.

## 4. Reglas de interfaz

- Lixus nunca pide datos de tarjeta.
- El texto dice que el pago se procesa con la pasarela del restaurante.
- El comprobante indica que no es factura fiscal.
- El estado de pago se actualiza solo por webhook, no por un botón manual.
- La suscripción se gestiona en otra pantalla, con otra pasarela (D-140).

## 5. Criterios de aceptación

- [ ] El total mostrado coincide con el pedido.
- [ ] El botón de pago abre la pasarela del restaurante.
- [ ] No se puede iniciar un segundo cobro del mismo pedido.
- [ ] Al confirmar, la mesa aparece disponible.
- [ ] El comprobante se descarga por QR.
- [ ] El comprobante muestra número, fecha, detalle y total, con aviso de no validez fiscal.
- [ ] No existe opción de cajero ni de pago en efectivo registrado por Lixus.

## 6. Estado actual

La página de caja es informativa. No hay cobro, confirmación ni comprobante. El modelo actual debe rediseñarse según D-145.
