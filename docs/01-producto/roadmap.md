# Roadmap 6–12 meses

**Estado:** Borrador
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Producto
**Horizonte:** diciembre de 2026 a noviembre de 2027

El roadmap se organiza por resultados, no por lista de funciones. Cada fase tiene un criterio de salida. Si no se cumple, no se avanza.

**Foco actual (D-151):** se trabaja en el MVP, principalmente Fase 1. Las fases comerciales y de operación son planificación futura, no una actividad en marcha.

## Fase 0 — Cimientos comerciales (M1)

**Objetivo:** poder vender con claridad y sin inventar.

- Identidad, misión, visión y promesa cerradas (D-129).
- Definir mercado inicial, cliente ideal y competencia (PD-02 a PD-05).
- Definir planes, precios y política de cobro (PD-07 a PD-09).
- Definir jurisdicción, entidad y borradores legales (PD-14 a PD-17).
- Entrevistar a cinco restaurantes y registrar evidencia.

**Salida:** propuesta comercial de una página, contrato borrador y precio validado con al menos tres interesados.

## Fase 1 — Primer cliente que paga (M1–M2)

**Objetivo:** cerrar el ciclo operativo mínimo.

- Conectar el frontend a la API.
- Completar login, logout, guards y recuperación de acceso.
- CRUD completo de menú y publicación.
- Pedidos con líneas, total en servidor y estados.
- Mesas, QR y solicitudes.
- Página pública publicable.
- Onboarding asistido de un restaurante real.

**Salida:** un restaurante piloto opera un servicio completo sin hojas de cálculo.

## Fase 2 — Operación diaria (M3–M4)

**Objetivo:** que el restaurante use Lixus todos los días.

- Reservas con disponibilidad y no-show.
- Cobro de pedidos por pasarela del restaurante, comprobante y QR de descarga.
- Personal, roles y revocación de acceso.
- Resumen del día para el CEO.
- Correo transaccional para invitaciones y avisos.

**Salida:** el piloto renueva y acepta que su operación depende de Lixus.

## Fase 3 — Cobro y retención (M5–M6)

**Objetivo:** convertir el piloto en un negocio repetible.

- Suscripción, facturación y estados de cuenta.
- Onboarding semiautomático con verificación.
- Métricas de activación, uso y churn.
- Soporte con horario y registro de casos.
- Backups verificados y plan de continuidad.

**Salida:** tres clientes activos, cobro mensual y soporte documentado.

## Fase 4 — Escala (M7–M9)

**Objetivo:** reducir el costo de servir a cada restaurante.

- Mejoras en las pasarelas de suscripción y de pedidos, si el negocio lo justifica.
- Notificaciones y avisos automáticos.
- Reportes operativos y exportación.
- Integraciones acordadas con clientes.
- Mejoras de rendimiento y observabilidad.

**Salida:** diez clientes activos con soporte estándar y métricas estables.

## Fase 5 — Expansión (M10–M12)

**Objetivo:** abrir nuevas oportunidades sin romper el núcleo.

- Evaluar multi-sucursal.
- Evaluar segundo idioma.
- Evaluar IA con límites y permisos.
- Evaluar API para integraciones.
- Revisar precios con datos reales.

**Salida:** decisión documentada sobre qué se expande y qué se descarta.

## Riesgos del roadmap

| Riesgo | Mitigación |
|---|---|
| El frontend sigue desconectado | Es la prioridad P0; no se añaden módulos hasta cerrarlo |
| El piloto exige funciones fuera de alcance | Contrato de alcance cerrado y backlog explícito |
| El precio no se valida | Entrevistas antes de publicar tarifas |
| La operación consume al equipo | Onboarding repetible y documentación de soporte |
| La deuda técnica frena la venta | Reservar capacidad semanal para deuda P0 |

## Lo que no cambia

- Aislamiento por schema.
- Resolución de tenant en servidor.
- Cookie httpOnly.
- Lixus sin acceso a datos operativos.
- Sin directorio de restaurantes.
