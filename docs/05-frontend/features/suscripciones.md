# Feature: suscripciones (frontend)

**Estado:** NO INICIADO
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/suscripciones.md`

## 1. Objetivo

Que el restaurante entienda su plan, su consumo y su estado de cuenta sin llamar a soporte.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Mi plan | `/admin/cuenta` | Plan, límites y renovación |
| Facturas | `/admin/cuenta/facturas` | Historial |
| Planes | `/portal/planes` | Catálogo interno |

## 3. Contenido

- Plan actual.
- Fecha de renovación.
- Límites usados (mesas, personal, almacenamiento).
- Estado: activo, en gracia, vencido.
- Botón de contacto para cambiar de plan.

## 4. Criterios de aceptación

- [ ] El restaurante ve su plan y su fecha de renovación.
- [ ] Los límites se muestran en lenguaje claro.
- [ ] Una factura se puede descargar.
- [ ] El estado vencido se explica sin bloquear la lectura.
- [ ] El cambio de plan se solicita, no se autogestiona en la versión inicial.

## 5. Estado actual

No existe pantalla de cuenta ni facturación. El portal solo muestra un catálogo informativo.
