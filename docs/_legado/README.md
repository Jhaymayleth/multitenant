# Documentos legados

Esta carpeta conserva la documentación anterior a la reorganización del 26 de noviembre de 2026. Se mantiene solo como trazabilidad histórica.

**No es fuente de verdad.** Las decisiones, el alcance, el estado y las fichas vigentes están en el árbol principal de `docs/`. Cuando un documento de esta carpeta contradiga al árbol vigente, manda el árbol vigente.

## Qué hay aquí

| Documento | Motivo de conservación |
|---|---|
| `00-INDICE.md` | Índice anterior |
| `01-REQUERIMIENTOS.md` | Requerimientos funcionales y no funcionales de origen |
| `02-DECISIONES.md` | Bloque de arquitectura anterior (incompleto) |
| `03-ARQUITECTURA.md` | Vista de arquitectura anterior |
| `04-MODULOS.md` | Módulos, permisos y reglas de origen |
| `05-PENDIENTES.md` | Pendientes de la etapa anterior |
| `06-HISTORIAL.md` | Historial de cambios anterior |
| `07-MODELO-DATOS.md` | Modelo de datos de origen |
| `08-SEGURIDAD-Y-ACCESO.md` | Seguridad y autorización de origen |
| `09-ROBUSTEZ.md` | Idempotencia, límites y concurrencia de origen |
| `10-ENTORNO-Y-DESPLIEGUE.md` | Entorno y despliegue anterior |
| `11-PLAN-DE-IMPLEMENTACION.md` | Plan de implementación anterior |
| `12-ENTREGABLES-Y-EVALUACION.md` | Entregables de la etapa anterior |
| `13-ROUTE-MVP.md` | Mapa de rutas anterior |
| `14-DESPLIEGUE-PRODUCCION.md` | Despliegue real al 24 de noviembre de 2026 |
| `AUDITORIA.md` | Auditoría técnica de origen |

## Equivalencias

| Legado | Vigente |
|---|---|
| `01-REQUERIMIENTOS.md` | `01-producto/alcance-producto.md`, `04-backend/features/` |
| `02-DECISIONES.md` | `00-gobierno/decisiones.md` |
| `03-ARQUITECTURA.md` | `03-arquitectura/` |
| `04-MODULOS.md` | `04-backend/dominios.md` y fichas de feature |
| `07-MODELO-DATOS.md` | `03-arquitectura/modelo-de-datos.md` |
| `08-SEGURIDAD-Y-ACCESO.md` | `03-arquitectura/seguridad.md` |
| `09-ROBUSTEZ.md` | `07-calidad/estrategia-pruebas.md`, `07-calidad/deuda-tecnica.md` |
| `10-ENTORNO-Y-DESPLIEGUE.md` | `06-infra-ops/` |
| `14-DESPLIEGUE-PRODUCCION.md` | `06-infra-ops/despliegue.md` |
| `AUDITORIA.md` | `07-calidad/deuda-tecnica.md` |

## Regla

No se edita un documento legado para “actualizarlo”. Si hace falta corregir algo, se corrige en el documento vigente y se deja el legado como estaba.
