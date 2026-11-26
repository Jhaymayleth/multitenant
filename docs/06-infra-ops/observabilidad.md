# Observabilidad

**Estado:** Parcial
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Qué se observa hoy

- Healthcheck del backend (`/health`).
- Healthcheck del frontend.
- Healthcheck de Redis.
- Logs de Docker con rotación.
- Estado de contenedores con `docker compose ps`.

## 2. Qué falta

| Capacidad | Estado | Prioridad |
|---|---|---|
| `request_id` en logs y respuestas | No | P0 |
| Logs estructurados | Parcial | P1 |
| Métricas de latencia y error | No | P1 |
| Alertas por caída | No | P0 |
| Alertas por 5xx | No | P1 |
| Alertas por backup fallido | No | P1 |
| Panel interno de salud | No | P2 |
| Trazas distribuidas | No | P2 |

## 3. Eventos que deben alertar

1. `/health` falla dos veces seguidas.
2. Error 5xx sostenido.
3. Backup no completado.
4. Certificado a menos de 15 días de vencer.
5. Disco o memoria por encima del 80 %.
6. Aprovisionamiento de tenant fallido.
7. Webhook rechazado por firma.

## 4. Logs

- No incluir contraseñas, tokens ni datos personales.
- Incluir `request_id`, ruta, estado, latencia y tenant cuando aplique.
- Retención por definir (PD-16).
- Acceso restringido al equipo.

## 5. Responsabilidad

- Ingeniería revisa salud y errores.
- Operación recibe reportes de clientes.
- El dueño recibe incidentes críticos.

## 6. Próximos pasos

1. Añadir `request_id` y logging uniforme.
2. Configurar alerta de caída y backup.
3. Medir latencia de endpoints críticos.
4. Documentar el panel de salud.
