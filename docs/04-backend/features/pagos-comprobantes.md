# Feature: pagos y comprobantes

**Estado:** NO INICIADO
**Dueño:** Ingeniería
**Decisiones:** D-111, D-114, D-128
**Documento frontend:** `05-frontend/features/pagos-comprobantes.md`

## 1. Objetivo

Cerrar la cuenta de una mesa, registrar el pago y entregar un comprobante simple sin convertir a Lixus en un POS.

## 2. Alcance

- Registrar pago en efectivo o en línea (sin procesar dinero en la versión inicial).
- Confirmar pago y liberar la mesa.
- Comprobante con numeración por tenant.
- QR de descarga con token temporal.
- Envío por correo si el cliente lo pide.
- Historial de pagos.

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-171 | El pago corresponde a un pedido del mismo tenant. |
| RN-172 | El total del pago coincide con el total del pedido. |
| RN-173 | Un pedido no se paga dos veces. |
| RN-174 | Al confirmar el pago, la mesa queda disponible. |
| RN-175 | El comprobante no tiene validez fiscal. |
| RN-176 | No se almacenan datos de tarjeta. |
| RN-177 | El token del comprobante caduca. |
| RN-178 | La numeración es por tenant y no se reutiliza. |

## 4. API

| Método | Ruta | Estado |
|---|---|---|
| POST | `/tenant/payments` | Parcial |
| POST | `/tenant/payments/{id}/confirm` | Stub |
| GET | `/tenant/payments` | No existe |
| GET | `/public/receipts/{token}` | Stub |
| POST | `/webhooks/payments/{provider}` | Stub |

## 5. Datos

- `tenant.payments`: pedido, monto, método, estado, referencia.
- `tenant.payment_events`: evento, proveedor, payload, firma.
- `tenant.receipts`: número, token, expiración.

## 6. Criterios de aceptación

- [ ] El cajero registra el pago del pedido correcto.
- [ ] Al confirmar, la mesa queda disponible.
- [ ] El comprobante se descarga por QR.
- [ ] Un token vencido no abre el comprobante.
- [ ] Un webhook sin firma se rechaza.
- [ ] Un evento repetido no duplica el pago.
- [ ] El comprobante muestra el detalle y el total.

## 7. Brecha actual

El endpoint de confirmación no confirma, el comprobante siempre responde 404 y el webhook no valida firma. Es el bloqueo P1 más importante para operar.
