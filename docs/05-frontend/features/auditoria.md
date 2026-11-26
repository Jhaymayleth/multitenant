# Feature: auditoría (frontend)

**Estado:** NO INICIADO
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/auditoria.md`

## 1. Objetivo

Que el equipo Lixus pueda revisar acciones privilegiadas y responder a un incidente con evidencia.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Auditoría | `/portal/auditoria` | Lista filtrable de eventos |
| Detalle | `/portal/auditoria/{id}` | Actor, acción y contexto |

## 3. Filtros

- Fecha.
- Actor.
- Tenant.
- Acción.
- Resultado.

## 4. Criterios de aceptación

- [ ] La lista muestra fecha, actor, tenant y acción.
- [ ] Se puede filtrar por tenant y fecha.
- [ ] El detalle no muestra secretos.
- [ ] La exportación es posible para soporte.
- [ ] El acceso está restringido al rol Lixus.

## 5. Estado actual

No existe pantalla. El endpoint de lectura no tiene datos porque nada escribe en la tabla.
