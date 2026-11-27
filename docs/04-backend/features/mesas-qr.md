# Feature: mesas y QR

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Decisiones:** D-110, D-157, D-158, D-159
**Documento frontend:** `05-frontend/features/mesas-qr.md`
**Especificación de la feature:** [`05-frontend/mesas-qr-api.md`](../../05-frontend/mesas-qr-api.md) (BL-05)

## 1. Objetivo

Dar al mesero una vista clara del salón y al cliente una forma simple de pedir atención desde la mesa sin instalar una app.

## 2. Alcance

- Mesas con etiqueta visible generada por el backend, piso y zona opcionales, y estado con color.
- Panel de selección con dos botones: ocupar y liberar.
- QR por mesa con token opaco.
- Sesión anónima por mesa.
- Solicitudes: llamar al mesero, falta algo, pedir la cuenta.
- Estados de mesa: disponible, ocupada, pendiente de pago, reservada, inactiva.
- Cierre por pago o cancelación en efectivo.

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-141 | Una mesa tiene una sola sesión activa. |
| RN-142 | El QR identifica la mesa; no crea pedidos. |
| RN-143 | Un QR antiguo no reabre una sesión cerrada. |
| RN-144 | La sesión no caduca por tiempo; se cierra por pago o cancelación. |
| RN-145 | El cliente anónimo no ve datos de otros clientes. |
| RN-146 | El mesero puede liberar la mesa solo con motivo y sin sesión activa ni pedido sin cobrar; si fuerza, queda registrado (D-159). |
| RN-147 | La etiqueta visible se genera en el backend desde la configuración de piso, zona y número; no se edita a mano (D-158). |
| RN-148 | El color de la mesa refleja su estado: verde libre, rojo ocupada o pendiente de pago, azul reservada solo si el tenant activó reservas (D-157, D-160). |

## 4. API

| Método | Ruta | Estado |
|---|---|---|
| GET | `/tenant/tables` | Implementado |
| POST | `/tenant/tables` | Implementado |
| PATCH | `/tenant/tables/{id}` | No existe |
| POST | `/tenant/tables/{id}/qr` | No existe |
| GET | `/public/table/{token}` | Stub |
| POST | `/public/table/{token}/requests` | Stub |

## 5. Datos

- `tenant.restaurant_tables`: número, piso, zona, etiqueta visible, estado, token y registro de cierre.
- `tenant.table_sessions`: mesa, inicio, fin, motivo de cierre.
- `tenant.service_requests`: tipo, estado, hora.

## 6. Criterios de aceptación

- [ ] Se crea una mesa, se genera su QR y se calcula su etiqueta visible.
- [ ] El panel muestra las mesas agrupadas por piso/zona con colores y dos botones.
- [ ] No se puede liberar una mesa con pedido sin cobrar salvo cierre forzado registrado.
- [ ] El cliente escanea y ve la mesa correcta.
- [ ] La solicitud aparece en el panel del mesero.
- [ ] Una segunda sesión sobre la misma mesa se rechaza o reanuda.
- [ ] Al confirmar el pago, la mesa queda disponible.
- [ ] Un token inválido responde 404.
- [ ] El QR no permite crear un pedido.

## 7. Brecha actual

Los endpoints públicos devuelven un mensaje fijo y no consultan la base de datos. No hay sesión ni solicitudes persistidas.
