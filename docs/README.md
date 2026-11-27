# Documentación de Lixus

Lixus es una plataforma SaaS multitenant para restaurantes independientes. Cada restaurante administra su menú, personal, mesas, pedidos, reservas y su página pública, con datos aislados del resto.

Este directorio es la fuente de verdad del producto. El código, la operación y la documentación comercial deben poder leerse sin depender de conversaciones antiguas.

**Fase actual:** MVP de la aplicación (D-151). No hay operación de venta activa; la documentación de negocio, operación y legal es planificación futura.

## Por dónde empezar

| Si eres... | Empieza por |
|---|---|
| Dueño del producto o inversor | `01-producto/identidad.md`, `02-negocio/modelo-de-negocio.md`, `01-producto/roadmap.md` |
| Desarrollador nuevo | `00-gobierno/indice.md`, `03-arquitectura/sistema.md`, `04-backend/dominios.md`, `05-frontend/areas.md` |
| Implementando una feature | `04-backend/features/` y `05-frontend/features/` del mismo nombre |
| Operando producción | `06-infra-ops/despliegue.md`, `06-infra-ops/incidentes.md`, `06-infra-ops/backups.md` |
| Revisando riesgo legal | `08-legal/README.md` (todo está diferido y pendiente de abogado) |

## Reglas de lectura

1. **Una decisión aprobada manda sobre cualquier documento de área.** El registro está en `00-gobierno/decisiones.md`.
2. **Lo que no está decidido vive en** `00-gobierno/decisiones-por-definir.md`, no en el código ni en un documento de área como si fuera un hecho.
3. **El estado real manda sobre la intención.** `00-gobierno/estado-producto.md` describe qué existe hoy, no qué se planeó.
4. **La parte legal está diferida** hasta que la aplicación funcione; los documentos son borradores y requieren abogado.

## Estado de la documentación

- **Versión:** 2.0
- **Última revisión:** 26 de noviembre de 2026
- **Alcance:** producto, negocio, arquitectura, backend, frontend, infraestructura, calidad y legal.
- **Idioma:** español.
- **Documentos antiguos:** se conservan en `_legado/` solo como trazabilidad. No son fuente de verdad.

## Cómo se actualiza

- Todo cambio de producto entra primero en `decisiones.md` o `decisiones-por-definir.md`.
- Toda feature nueva actualiza su documento backend y su documento frontend.
- Todo cambio de infraestructura actualiza `06-infra-ops/` y `changelog.md`.
- Ningún secreto real se escribe aquí. Solo nombres de variables.
