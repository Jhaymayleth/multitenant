# Componentes y patrones

**Estado:** Borrador
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Enfoque

No hay biblioteca de componentes adoptada. Se propone construir un conjunto pequeño y consistente antes de multiplicar pantallas.

## 2. Componentes base

| Componente | Uso |
|---|---|
| `AppShell` | Layout con navegación y cabecera |
| `PageHeader` | Título, acciones y contexto |
| `DataTable` | Listados con paginación y acciones |
| `FormField` | Etiqueta, ayuda y error |
| `StatusBadge` | Estado de mesa, pedido, pago o tenant |
| `EmptyState` | Sin datos, con acción |
| `ErrorState` | Error con reintento |
| `LoadingState` | Esqueleto o spinner |
| `ConfirmDialog` | Acciones destructivas |
| `Toast` | Confirmación breve |
| `Money` | Formato de moneda |
| `DateTime` | Fecha y hora en zona del restaurante |
| `RoleGate` | Renderiza según permiso |
| `TenantGuard` | Verifica sesión y tenant |

## 3. Patrones

### Formularios

- Validación en cliente para rapidez; validación definitiva en servidor.
- Mensajes junto al campo, no solo un resumen.
- No se deshabilita el botón sin explicar por qué.
- Se conserva lo escrito si falla el envío.

### Listados

- Paginación o carga incremental.
- Filtro por estado.
- Acción principal visible.
- Estado vacío con “crear el primero”.

### Acciones destructivas

- Confirmación con el nombre del elemento.
- Explicar la consecuencia.
- No usar rojo para acciones normales.

### Errores

- Traducir el código del backend a lenguaje del restaurante.
- Incluir `request_id` en el detalle para soporte.
- No mostrar trazas ni SQL.

## 4. Tokens de diseño

- Espaciado en múltiplos de 4.
- Tipografía legible en móvil.
- Contraste mínimo AA.
- Bordes y sombras discretos.
- Color de estado, no solo texto.

## 5. Reglas

1. Un componente se crea cuando se repite tres veces.
2. No se copia estilo entre pantallas.
3. Todo componente interactivo es accesible por teclado.
4. Todo texto visible está en español.
5. Los componentes no conocen el tenant; lo reciben por contexto.
