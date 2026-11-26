# Convenciones de documentación

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026

## 1. Nombres de archivo

- Minúsculas, sin acentos y con guiones: `planes-y-precios.md`.
- Un tema por archivo. Si un documento necesita explicar otro tema, enlaza.
- Las features usan el mismo slug en backend y frontend: `pedidos.md` en ambas carpetas.

## 2. Cabecera mínima

Todo documento empieza con:

```text
# Título
**Estado:** Vigente | Borrador | Por definir
**Última revisión:** AAAA-MM-DD
**Dueño:** Producto | Ingeniería | Operación | Legal
```

## 3. Identificadores

| Prefijo | Uso | Dónde vive |
|---|---|---|
| `D-###` | Decisión | `decisiones.md` |
| `PD-##` | Decisión por definir | `decisiones-por-definir.md` |
| `RF-##` | Requisito funcional de producto | Documento de feature |
| `RNF-##` | Requisito no funcional | `07-calidad/` o arquitectura |
| `RN-##` | Regla de negocio | Documento de feature |
| `RT-##` | Riesgo técnico | `deuda-tecnica.md` |
| `INC-##` | Incidente | `incidentes.md` |

La numeración nueva de decisiones empieza en `D-101`. Los identificadores `D-001` a `D-076` del material antiguo son referencia histórica y no se reabren sin una decisión nueva.

## 4. Estados

### Decisión

- `PROPUESTA`: recomendación del PO, pendiente de aprobación del dueño.
- `APROBADA`: decisión vigente.
- `POR DEFINIR`: existe la pregunta, no la respuesta.
- `SUSTITUIDA`: reemplazada por otra decisión; se conserva para trazabilidad.

### Feature

- `EN PRODUCCIÓN`: funciona y se usa.
- `PARCIAL`: existe una parte, pero no cumple el criterio de aceptación.
- `NO INICIADO`: está en el alcance, no hay implementación.
- `PLANIFICADO`: está en el roadmap, fuera de la versión actual.
- `DESCARTADO`: se evaluó y no se hará.

## 5. Reglas de escritura

1. No se usa lenguaje de evaluación, docencia ni entrega académica.
2. No se inventan precios, clientes, cifras, jurisdicciones ni datos legales.
3. Si falta un dato, se escribe `POR DEFINIR` y se propone un default explícitamente marcado como propuesta.
4. No se duplica contenido: se enlaza al documento dueño.
5. No se escriben secretos, claves ni datos personales reales.
6. Los documentos legales llevan la advertencia de revisión por abogado.
7. Toda afirmación de estado debe poder verificarse en el repositorio o en producción.

## 6. Enlaces

- Usa enlaces relativos entre documentos.
- Al mover un documento, actualiza el índice maestro y los enlaces entrantes.
- Los documentos de `_legado/` no se enlazan desde la documentación vigente.
