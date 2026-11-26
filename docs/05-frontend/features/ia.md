# Feature: IA (frontend)

**Estado:** NO INICIADO
**Dueño:** Producto / Ingeniería
**Documento backend:** `04-backend/features/ia.md`

## 1. Objetivo

Ayudar al restaurante a escribir y consultar sin que la IA opere el negocio por su cuenta.

## 2. Pantallas previstas

| Pantalla | Ruta | Función |
|---|---|---|
| Asistente de menú | `/admin/menu/asistente` | Mejorar descripciones |
| Asistente de configuración | `/admin/configuracion/asistente` | Sugerir textos |
| Consumo | `/admin/cuenta/ia` | Tokens y límites |

## 3. Reglas de interfaz

- La respuesta se marca como generada por IA.
- El usuario confirma antes de guardar.
- Se muestra qué datos se usaron.
- No se envía información de otros tenants.
- El botón se desactiva si se agotó la cuota.

## 4. Criterios de aceptación

- [ ] El usuario revisa y confirma antes de escribir.
- [ ] La IA no cambia precios sin confirmación.
- [ ] El consumo es visible.
- [ ] Un error de proveedor no rompe la pantalla.
- [ ] La interfaz explica que la IA puede equivocarse.

## 5. Estado actual

Fuera de la versión que se vende. No hay pantalla ni integración.
