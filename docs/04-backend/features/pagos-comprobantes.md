# Feature: cobro de pedidos y comprobantes

**Estado:** NO INICIADO
**Dueño:** Ingeniería
**Decisiones:** D-128, D-140, D-145
**Documento frontend:** `05-frontend/features/pagos-comprobantes.md`

## 1. Objetivo

Permitir que el restaurante cobre el total de un pedido con **su propia pasarela**, sin que Lixus reciba ese dinero ni mantenga un rol de cajero. Lixus genera el cobro, confirma el pago por webhook, libera la mesa y entrega un comprobante operativo.

## 2. Los dos flujos de pago

| Flujo | Quién paga | Quién recibe | Pasarela | Decisión |
|---|---|---|---|---|
| Suscripción | El restaurante | Lixus | Pasarela de Lixus | D-140 |
| Pedido | El comensal | Cuenta del restaurante | Pasarela configurada por el tenant | D-145 |

No se mezclan. El dinero de la venta nunca entra en una cuenta de Lixus.

## 3. Alcance

- Configurar la pasarela del restaurante por tenant (credenciales cifradas, nunca expuestas al cliente).
- Generar un enlace o botón de cobro por el total del pedido.
- El cliente o el mesero inicia el pago y elige el método en la pasarela del restaurante.
- Confirmación por webhook firmado.
- Mesa disponible al confirmar.
- Comprobante operativo con numeración por tenant y QR de descarga.
- Envío por correo si el cliente lo pide.
- Historial de cobros.

## 4. Reglas de negocio

| ID | Regla |
|---|---|
| RN-171 | El cobro corresponde a un pedido del mismo tenant. |
| RN-172 | El total del cobro coincide con el total calculado en el servidor. |
| RN-173 | Un pedido no se cobra dos veces. |
| RN-174 | Al confirmar el webhook, la mesa queda disponible. |
| RN-175 | El comprobante de Lixus no tiene validez fiscal; la factura al comensal la emite el restaurante. |
| RN-176 | Lixus no almacena datos de tarjeta. |
| RN-177 | El token del comprobante caduca. |
| RN-178 | La numeración es por tenant y no se reutiliza. |
| RN-179 | Lixus no recibe dinero de los pedidos (D-145). |
| RN-180 | Cada tenant configura su propia pasarela; no hay pasarela global de pedidos. |
| RN-181 | El webhook se valida con firma, timestamp y `event_id` único. |
| RN-182 | La suscripción se cobra por la pasarela de Lixus, separada de la del pedido (D-140). |

## 5. API prevista

| Método | Ruta | Estado |
|---|---|---|
| GET | `/tenant/payment-settings` | No existe |
| PUT | `/tenant/payment-settings` | No existe |
| POST | `/tenant/orders/{id}/payment-link` | No existe |
| POST | `/webhooks/orders/{provider}` | Stub (sin firma) |
| GET | `/tenant/payments` | No existe |
| GET | `/public/receipts/{token}` | Stub |

Los endpoints actuales `/tenant/payments` y `/tenant/payments/{id}/confirm` se rediseñan: ya no registran pagos manuales de caja, sino enlaces de cobro y eventos de pasarela.

## 6. Datos

- `tenant.payment_settings`: proveedor, credenciales cifradas, cuenta destino, estado.
- `tenant.payments`: pedido, monto, proveedor, referencia, estado.
- `tenant.payment_events`: evento, proveedor, payload, firma, `event_id`.
- `tenant.receipts`: número, token, expiración.
- `platform.subscriptions`: cobro de la suscripción, separado de estos datos.

## 7. Criterios de aceptación

- [ ] El restaurante configura su pasarela y el destino del dinero es su cuenta.
- [ ] El mesero o el cliente genera el botón de pago del pedido.
- [ ] La pasarela muestra el método de pago; Lixus no pide datos de tarjeta.
- [ ] Un webhook firmado marca el pedido pagado y libera la mesa.
- [ ] Un webhook sin firma se rechaza.
- [ ] Un evento repetido no duplica el cobro.
- [ ] El comprobante se descarga por QR y expira.
- [ ] El comprobante dice explícitamente que no factura al comensal.
- [ ] El cobro de la suscripción no aparece mezclado con los cobros de pedidos.

## 8. Brecha actual

El endpoint de confirmación no confirma, el comprobante siempre responde 404 y el webhook no valida firma. Además, el modelo actual asume caja y registro manual, incompatible con D-145. Es el bloqueo P1 más importante para operar.
