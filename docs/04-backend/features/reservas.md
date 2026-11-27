# Feature: reservas

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Decisiones:** D-110, D-160, D-161
**Prioridad:** P1. Fuera del MVP mientras no se active el flag por tenant (D-160).
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
- Activación por tenant con flag; desactivadas por defecto (D-160).
- Ventana configurable de antelación, con valores por defecto propuestos de 2 horas y 30 días (D-161).

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-161 | Reservar exige cuenta en ese restaurante. |
| RN-162 | La mesa pertenece al tenant. |
| RN-163 | No se solapan reservas en la misma mesa y franja, ni con ocupación manual (D-161). |
| RN-164 | La duración y la tolerancia son configurables. |
| RN-165 | Una mesa reservada no se libera por QR. |
| RN-166 | El no-show se registra manualmente. |
| RN-167 | La reserva se interpreta en la zona horaria del restaurante. |
| RN-168 | La antelación se valida al crear la reserva y al ocupar la mesa; el mesero puede forzar con motivo registrado (D-161). |
| RN-169 | Sin el flag activo, no se ofrece reserva pública ni se muestra el color azul (D-160). |

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
- [ ] Ocupar manualmente una mesa en una franja reservada se bloquea o se registra como forzado.
- [ ] La ventana de antelación se valida al reservar y al ocupar.
- [ ] Sin el flag activo, no hay reserva pública.

## 7. Brecha actual

No hay consulta de conflicto, disponibilidad pública ni cambio de estado. El servicio solo crea y lista.
