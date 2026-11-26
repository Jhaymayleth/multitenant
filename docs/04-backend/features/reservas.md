# Feature: reservas

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Decisiones:** D-110
**Documento frontend:** `05-frontend/features/reservas.md`

## 1. Objetivo

Permitir que un cliente reserve una mesa con disponibilidad real y que el restaurante evite dobles reservas.

## 2. Alcance

- Consulta de disponibilidad sin cuenta.
- Reserva con cuenta en el restaurante.
- Fecha, hora, duración, personas y mesa.
- Estados: solicitada, confirmada, atendida, completada, cancelada, no presentada.
- Gestión por el personal según rol.
- Política de tolerancia y no-show.

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-161 | Reservar exige cuenta en ese restaurante. |
| RN-162 | La mesa pertenece al tenant. |
| RN-163 | No se solapan reservas en la misma mesa y franja. |
| RN-164 | La duración y la tolerancia son configurables. |
| RN-165 | Una mesa reservada no se libera por QR. |
| RN-166 | El no-show se registra manualmente. |
| RN-167 | La reserva se interpreta en la zona horaria del restaurante. |

## 4. API

| Método | Ruta | Estado |
|---|---|---|
| GET | `/tenant/reservations` | Implementado |
| POST | `/tenant/reservations` | Parcial |
| PATCH | `/tenant/reservations/{id}/status` | No existe |
| GET | `/public/{slug}/availability` | No existe |
| POST | `/public/{slug}/reservations` | No existe |

## 5. Datos

- `tenant.reservations`: cliente, mesa, fecha, duración, personas, estado.
- `tenant.restaurant_tables`: mesa reservable.
- `tenant.customers`: cuenta del cliente.

## 6. Criterios de aceptación

- [ ] La disponibilidad se consulta sin cuenta.
- [ ] Una reserva sin sesión se rechaza.
- [ ] Dos reservas en la misma mesa y hora devuelven 409.
- [ ] El personal confirma, atiende o marca no-show.
- [ ] La reserva aparece en el panel del día.
- [ ] Una mesa reservada no se abre por QR antes de la hora.

## 7. Brecha actual

No hay consulta de conflicto, disponibilidad pública ni cambio de estado. El servicio solo crea y lista.
