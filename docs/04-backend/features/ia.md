# Feature: IA

**Estado:** NO INICIADO
**Dueño:** Producto / Ingeniería
**Decisión abierta:** PD-26
**Documento frontend:** `05-frontend/features/ia.md`

## 1. Objetivo

Asistir al restaurante en tareas concretas sin que la IA decida por él ni acceda a datos de otros tenants.

## 2. Alcance previsto

- Mejorar descripciones de productos y del restaurante.
- Asistir en la configuración inicial.
- Responder consultas sobre datos a los que el usuario ya tiene acceso.
- Registrar consumo por tenant.

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-201 | La IA usa los permisos del usuario que la invoca. |
| RN-202 | Nunca devuelve datos de otro tenant. |
| RN-203 | No escribe directo en la base de datos. |
| RN-204 | Toda escritura pasa por una herramienta del backend con validación. |
| RN-205 | El consumo se mide y se limita por plan. |
| RN-206 | El usuario sabe cuándo la respuesta es generada por IA. |

## 4. API prevista

| Método | Ruta | Estado |
|---|---|---|
| POST | `/tenant/ai/describe` | No existe |
| POST | `/tenant/ai/assist` | No existe |
| GET | `/tenant/ai/usage` | No existe |

## 5. Datos

- `tenant.ai_usage`: proveedor, modelo, tokens, latencia, operación.

## 6. Criterios de aceptación

- [ ] Una consulta maliciosa no devuelve datos de otro tenant.
- [ ] La IA no puede cambiar precios sin confirmación.
- [ ] El consumo queda registrado.
- [ ] El plan limita el uso.
- [ ] La respuesta se puede auditar.

## 7. Estado

Fuera de la versión que se vende. Se evalúa después de estabilizar la operación y el cobro.
