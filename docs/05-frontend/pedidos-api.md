# Especificación técnica: BL-04 pedidos con líneas y total

**Estado:** Especificación lista para implementar
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería
**Feature:** [`01-producto/backlog.md`](../01-producto/backlog.md) → BL-04
**Decisiones:** D-106 (tenant en servidor), D-110 (canales de pedido), D-113 (sin impuestos, propinas ni descuentos), D-123 (español), D-145 (sin cajero), D-146 (roles), D-155 (sin gestión de domicilio), D-156 (pedido en mesa)
**Fichas espejo:** [`04-backend/features/pedidos.md`](../04-backend/features/pedidos.md) · [`05-frontend/features/pedidos.md`](features/pedidos.md)

## 1. Objetivo

Que el pedido se registre una sola vez con sus líneas, que el total se calcule en el servidor y que cocina, mesero y cobro trabajen sobre la misma información. El precio se congela al crear el pedido, de modo que un cambio posterior en la carta no altere lo que el comensal pidió.

## 2. Estado actual

- `GET /tenant/orders`, `POST /tenant/orders` y `GET /tenant/orders/{id}` existen. No hay cambio de estado ni alta de líneas posterior.
- El modelo ya tiene `order_items` con `product_name`, `unit_price_cents`, `quantity` y `total_cents` para snapshot, y la cabecera ya tiene `total_cents` y `payment_status`.
- `OrderCreate` acepta `items` con `product_id`, `quantity` y `notes`, pero `OrderService.create_order` ignora la lista y guarda `total_cents=0` con estado `confirmed` (RT-02).
- El precio nunca se toma de la base de datos; el esquema de entrada no permite que el cliente envíe precios, lo cual se mantiene (RN-152).
- El router acepta `Idempotency-Key`, pero el servicio no la usa; un reintento puede crear dos pedidos (RT-04).
- Existe `OrderStatusUpdate` en esquemas, sin endpoint que lo consuma.
- Los estados reales de la columna `status` son `draft`, `confirmed`, `in_preparation`, `ready`, `served`, `out_for_delivery`, `delivered`, `closed` y `cancelled`. La ficha backend usa nombres descriptivos; esta especificación toma los valores del modelo como referencia.
- `/admin/pedidos` es una página informativa: sin carrito, total ni tablero de cocina.

## 3. Alcance de esta feature

Incluye:

1. Crear pedido con una o más líneas, tomando nombre y precio del catálogo del tenant.
2. Calcular el total en servidor y congelarlo en cabecera y líneas.
3. Rechazar pedido sin líneas, producto inexistente o producto inactivo.
4. Idempotencia por `Idempotency-Key` en la creación.
5. Cambio de estado con transiciones permitidas y registro de quién lo hace.
6. Vista de pedidos y detalle en `/admin/pedidos`, con carrito y tablero de cocina.
7. Pedido de mesa y registro simple de domicilio como tipos distintos, sin mezclarlos.
8. Registro de domicilio sin zonas, tarifa ni seguimiento; la entrega se resuelve fuera de Lixus (D-155).

Queda fuera:

- Generación de cobro, webhook y comprobante (BL-12).
- Gestión de domicilio: zonas, tarifas, flota, seguimiento y entrega; queda fuera del producto (D-155).
- Idempotencia en cobros (BL-17) y auditoría general (BL-19).
- Solicitudes desde QR: el QR no crea pedidos (D-110, BL-05).
- Impuestos, propinas y descuentos (D-113).
- Edición de pedidos cerrados o pagados (RN-157).

## 4. Contrato

Base: `/api/v1`, cookie `lixus_session`, tenant resuelto en servidor (D-106). El cliente no envía `tenant_id`, `precio`, `total` ni estado final.

### 4.1 Endpoints existentes

| Método | Ruta | Uso | Estado |
|---|---|---|---|
| GET | `/tenant/orders` | Lista por estado | Implementado |
| POST | `/tenant/orders` | Crea pedido | Parcial (ignora líneas) |
| GET | `/tenant/orders/{id}` | Detalle con líneas | Implementado |

### 4.2 Endpoints a añadir

| Método | Ruta | Uso | Respuesta |
|---|---|---|---|
| PATCH | `/tenant/orders/{id}/status` | Avanza el estado | 200 + pedido |
| GET | `/tenant/orders/kitchen` | Cola de preparación | 200 + lista |

### 4.3 Cuerpos

```text
POST /tenant/orders
Header: Idempotency-Key: <uuid>
{
  "table_session_id": uuid | null,
  "type": "dine_in" | "delivery",
  "items": [
    { "product_id": uuid, "quantity": int 1..100, "notes": string | null }
  ],
  "notes": string | null
}

PATCH /tenant/orders/{id}/status
{ "status": "confirmed" | "in_preparation" | "ready" | "served" | "closed" | "cancelled" }
```

`type = "delivery"` solo registra el pedido para llevar: no pide zona, tarifa ni datos de entrega. Los estados de seguimiento de domicilio no se usan (D-155).

### 4.4 Cálculo del total

```text
total_cents = Σ (precio del catálogo × cantidad) por línea
```

Sin impuestos, propinas ni descuentos (D-113). El total se calcula en servidor en una sola transacción; el frontend puede mostrar un total estimado usando el catálogo leído, pero el valor definitivo es el de la respuesta.

### 4.5 Códigos de error

`ORDER_EMPTY`, `PRODUCT_NOT_FOUND`, `PRODUCT_UNAVAILABLE`, `INVALID_QUANTITY`, `INVALID_STATUS_TRANSITION`, `ORDER_NOT_EDITABLE`, `FORBIDDEN`, `IDEMPOTENCY_CONFLICT`, `NOT_FOUND`.

Un pedido de otro tenant devuelve `404`, sin confirmar si existe.

## 5. Diseño

### 5.1 Servicio de pedidos

```text
create_order(data, idempotency_key)
  ├── valida Idempotency-Key y busca respuesta previa en tenant.idempotency_keys
  ├── exige al menos una línea
  ├── por cada línea:
  │     ├── lee MenuProduct del schema del tenant
  │     ├── verifica is_active = true
  │     ├── copia product_name y price_cents al momento
  │     └── calcula total_cents de la línea
  ├── suma las líneas y guarda total_cents
  ├── guarda cabecera en estado confirmed y payment_status unpaid
  └── guarda la respuesta asociada a la clave de idempotencia
```

La lectura de productos ocurre en el mismo `search_path` que el resto de la petición. Ningún precio viaja del navegador al servidor.

### 5.2 Idempotencia

- Misma clave y mismo cuerpo → misma respuesta, sin crear otro pedido.
- Misma clave y cuerpo distinto → `409 IDEMPOTENCY_CONFLICT`.
- TTL propuesto: 24 horas, según la convención de [`04-backend/api.md`](../04-backend/api.md).
- La clave se guarda en la tabla de idempotencia del tenant, nunca en `platform`.

### 5.3 Máquina de estados

| Desde | Acción | Hacia | Roles |
|---|---|---|---|
| `draft` | confirmar | `confirmed` | `owner`, `admin`, `waiter` |
| `confirmed` | enviar a cocina | `in_preparation` | `owner`, `admin`, `cook` |
| `in_preparation` | marcar listo | `ready` | `owner`, `admin`, `cook` |
| `ready` | servir | `served` | `owner`, `admin`, `waiter` |
| `served` | cerrar | `closed` | `owner`, `admin`, `waiter` |
| `confirmed`, `in_preparation` | cancelar | `cancelled` | `owner`, `admin` |

Los valores `out_for_delivery` y `delivered` siguen existiendo en el modelo, pero no se usan: Lixus no gestiona la entrega (D-155). Cualquier otra transición devuelve `422 INVALID_STATUS_TRANSITION`. `cook` ve mesas, líneas y notas, sin datos personales. Un pedido `closed` o `cancelled` no admite cambios de estado ni de líneas.

### 5.4 Snapshot y coherencia

- La línea guarda `product_id`, `product_name`, `unit_price_cents`, `quantity`, `total_cents` y `notes`.
- Cambiar o retirar un producto del catálogo no modifica pedidos existentes (depende de BL-03).
- `payment_status` es independiente de `status`: el pago se marca en BL-12, sin rol de cajero (D-145).

## 6. Flujos

### 6.1 Mesero toma el pedido de mesa

1. Elige mesa de `/admin/mesas` con sesión activa.
2. Busca productos del catálogo, ajusta cantidad y escribe notas.
3. Ve un total estimado que confirma con «Confirmar pedido».
4. El cliente envía una clave de idempotencia por pedido nuevo.
5. El backend guarda líneas, total y estado `confirmed`; el frontend muestra el número de pedido.
6. El pedido aparece en la cola de cocina sin datos personales.

### 6.2 Cocina trabaja la cola

1. `/admin/pedidos/cocina` lista pedidos `confirmed` y `in_preparation` por hora y mesa.
2. El cocinero marca «en preparación» y después «listo».
3. El cambio se refleja en el detalle sin recargar.

### 6.3 Servicio y cierre

1. El mesero marca «servido» cuando entrega en mesa.
2. Al confirmarse el cobro, BL-12 marcará el pedido como cerrado; en esta feature el cierre manual queda disponible con rol `owner` o `admin`.
3. Un pedido cerrado no se edita.

### 6.4 Registro simple de domicilio

1. El mesero elige `type = "delivery"` para dejar constancia del pedido para llevar.
2. El backend calcula el total solo con las líneas y deja `payment_status` en `unpaid`.
3. No se piden zonas, tarifas, dirección de entrega ni estados de seguimiento.
4. La entrega y el cobro los resuelve el restaurante por fuera de Lixus (D-155). El pedido no sigue la ruta de entrega porque esa gestión no está en el producto.

### 6.5 Reintento

1. Si la petición falla por red, el cliente reenvía la misma clave y el mismo cuerpo.
2. El backend devuelve el pedido ya creado, sin duplicarlo.
3. Si el cuerpo cambió con la misma clave, devuelve `409`.

## 7. Archivos a crear o modificar

| Archivo | Acción | Contenido |
|---|---|---|
| `backend/app/orders/service.py` | Modificar | Líneas, snapshots, total, idempotencia y transiciones |
| `backend/app/orders/repository.py` | Modificar | Consulta de cola de cocina y guard de idempotencia |
| `backend/app/orders/router.py` | Modificar | `PATCH /status`, `GET /kitchen`, roles por acción |
| `backend/app/orders/schemas.py` | Modificar | Cuerpo sin zona ni tarifa, errores y respuesta de cola |
| `backend/app/orders/models.py` | Modificar | Sin campos de zona ni tarifa; registrar cambio de estado si hace falta |
| `backend/migrations/versions/` (cadena tenant) | Crear | Índice de idempotencia y campos de control de estado |
| `backend/tests/` | Crear | Pruebas de líneas, total, idempotencia, estados y roles |
| `frontend/src/lib/orders.ts` | Crear | Funciones de pedidos sobre `apiFetch` |
| `frontend/src/app/(ceo-portal)/admin/pedidos/page.tsx` | Modificar | Lista por estado y acceso al detalle |
| `frontend/src/app/(ceo-portal)/admin/pedidos/nuevo/page.tsx` | Crear | Mesa, productos, cantidades y total |
| `frontend/src/app/(ceo-portal)/admin/pedidos/[id]/page.tsx` | Crear | Líneas, total e historial de estados |
| `frontend/src/app/(ceo-portal)/admin/pedidos/cocina/page.tsx` | Crear | Cola de preparación |
| `docs/04-backend/api.md` | Modificar | Endpoints nuevos |
| `docs/04-backend/features/pedidos.md` | Modificar | Estados reales y enlace a esta especificación |
| `docs/05-frontend/features/pedidos.md` | Modificar | Estado de pantallas y enlace a esta especificación |

No se modifica el contrato de cobro ni el de pagos.

## 8. Estados obligatorios por pantalla

| Pantalla | Cargando | Vacío | Error | Sin permiso |
|---|---|---|---|---|
| `/admin/pedidos` | Esqueleto de lista | «No hay pedidos todavía.» | Reintento | «No tienes acceso a esta sección» |
| `/admin/pedidos/nuevo` | «Cargando carta…» | «El menú no tiene productos publicados.» | Producto sin precio o sin categoría | No aplica |
| Detalle del pedido | Esqueleto de líneas | No aplica | Reintento | «No tienes acceso a este pedido» |
| Cocina | «Cargando cola…» | «No hay pedidos pendientes.» | Reintento | «Solo cocina y administración» |
| Confirmación | «Guardando…» | No aplica | `IDEMPOTENCY_CONFLICT` con acción clara | No aplica |

El total se muestra con la moneda del tenant tomada de su configuración; nunca se inventa un símbolo.

## 9. Pruebas requeridas

1. Un pedido con dos líneas devuelve el total correcto calculado en servidor.
2. El precio de las líneas es el del catálogo al crear el pedido, aunque el cliente envíe otro valor.
3. Cambiar el precio del producto después no altera el pedido existente.
4. Un pedido sin líneas se rechaza con `ORDER_EMPTY`.
5. Un producto inexistente, inactivo o de otro tenant se rechaza.
6. Misma clave de idempotencia y mismo cuerpo devuelve el mismo pedido.
7. Misma clave con cuerpo distinto devuelve `409 IDEMPOTENCY_CONFLICT`.
8. Un pedido `delivery` se crea sin zona, tarifa ni datos de entrega.
9. El total del pedido `delivery` es solo la suma de las líneas, sin cargos adicionales.
10. Las transiciones permitidas funcionan por rol; una transición inválida devuelve `422`.
11. Un cocinero no puede cambiar un pedido a `served` ni ver datos personales.
12. Un pedido `closed` o `cancelled` no admite cambios.
13. Un pedido de otro tenant devuelve `404`.
14. La cola de cocina muestra mesa, líneas y notas, sin correos ni nombres de comensales.

## 10. Criterios de aceptación

- [ ] Toda línea guarda nombre y precio congelados.
- [ ] El total de cabecera y la suma de líneas coinciden.
- [ ] El pedido sin líneas o con producto inactivo se rechaza.
- [ ] La creación es idempotente por `Idempotency-Key`.
- [ ] El cambio de estado respeta la tabla de transiciones y los roles de D-146.
- [ ] `payment_status` se mantiene separado de `status`.
- [ ] No se aplican impuestos, propinas ni descuentos.
- [ ] El domicilio se registra sin zonas, tarifa ni logística (D-155).
- [ ] `/admin/pedidos` y la cola de cocina consumen la API real.
- [ ] Los pedidos de otro tenant no se pueden leer ni modificar.

## 11. Dependencias

- BL-03: el catálogo con precio, disponibilidad y publicación; sin él no hay productos que congelar.
- BL-01: `apiFetch` y `AppError` para las pantallas.
- BL-02: sesión y roles para los guards.
- D-106: resolución de tenant en servidor; el cliente no elige schema.
- D-110 y D-156: mesero crea pedidos de mesa; el QR solo solicita atención; el cliente registrado reserva, no pide a domicilio.
- D-113, D-145, D-155 y D-156: sin cargos extra, sin cajero y sin gestión de domicilio.
- BL-05: sesión de mesa real para asociar `table_session_id`.
- BL-06: enlace de domicilio configurable en la página pública; no hay zonas ni tarifas.
- BL-12: cobro, cierre de mesa y comprobante.
- Deuda RT-02 y RT-04 en [`07-calidad/deuda-tecnica.md`](../07-calidad/deuda-tecnica.md).

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Total calculado en el navegador | El servidor recalcula y es la única fuente del total |
| Cambio de carta altera pedidos antiguos | Snapshot de nombre y precio en cada línea |
| Doble pedido por reintento | Idempotencia con clave por pedido y TTL |
| Concurrencia al cambiar estado | Validar transición dentro de la misma transacción |
| Cocinero ve datos personales | Respuesta de cocina con campos explícitos, sin customer_id ni correos |
| Pedido de otro tenant por UUID conocido | El `search_path` del schema activo lo deja fuera; devolver `404` |
| Domicilio fuera de Lixus | Registro simple y enlace configurable; sin zonas, estimaciones ni seguimiento |
| Cobro y estado mezclados | `payment_status` independiente; BL-12 es el único que lo escribe |

## 13. Definición de terminado

Se considera terminada cuando se cumplen los criterios de aceptación, pasan las pruebas del punto 9, CI pasa con lint, tests y build, y se verifica manualmente un ciclo completo: entrar como mesero, crear un pedido de mesa con dos líneas, verlo en cocina, avanzar a «listo» y «servido» con roles distintos, reintentar la creación con la misma clave sin duplicarlo y confirmar que cambiar el precio de la carta no modifica el pedido.
