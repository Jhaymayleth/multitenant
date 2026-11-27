# Feature: reservas (frontend)

**Estado:** NO INICIADO
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/reservas.md`
**Decisiones:** D-160, D-161
**Prioridad:** P1. Fuera del MVP mientras no se active el flag por tenant (D-160).

## 1. Objetivo

Que el comensal vea disponibilidad y reserve sin fricción, y que el restaurante gestione su día.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Reserva pública | `/r/{slug}/reservas` | Fecha, hora, personas |
| Mis reservas | `/r/{slug}/cuenta/reservas` | Historial del cliente |
| Agenda | `/admin/reservas` | Día, semana y estados |
| Detalle | `/admin/reservas/{id}` | Cliente, mesa y acciones |

## 3. Flujo público

1. Elegir fecha y número de personas.
2. Ver franjas disponibles.
3. Iniciar sesión o crear cuenta.
4. Confirmar.
5. Recibir confirmación.

## 4. Flujo del restaurante

1. Ver la agenda del día.
2. Confirmar, atender o marcar no-show.
3. Asignar mesa.
4. Ver ocupación.

## 5. Criterios de aceptación

- [ ] La disponibilidad se consulta sin cuenta.
- [ ] Reservar exige sesión.
- [ ] Una franja ocupada no se ofrece.
- [ ] El restaurante ve la reserva al instante.
- [ ] El no-show se registra con un toque.
- [ ] La hora se muestra en la zona del restaurante.
- [ ] La reserva pública solo aparece si el tenant activó el flag (D-160).
- [ ] La mesa reservada se ve en azul y no se ofrece en una franja ocupada (D-157, D-161).

## 6. Estado actual

La página es informativa. No hay calendario, disponibilidad ni gestión.
