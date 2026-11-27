# Especificación técnica: BL-05 mesas y QR

**Estado:** Especificación lista para implementar
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería
**Feature:** [`01-producto/backlog.md`](../01-producto/backlog.md) → BL-05
**Decisiones:** D-106 (tenant en servidor), D-110 (QR solo solicitudes), D-123 (español), D-131 (accesibilidad en flujo público), D-145 (sin cajero), D-146 (roles), D-157 (panel con colores), D-158 (etiqueta generada), D-159 (liberar con motivo), D-160 (reservas en P1), D-161 (ventana y solape)
**Fichas espejo:** [`04-backend/features/mesas-qr.md`](../04-backend/features/mesas-qr.md) · [`05-frontend/features/mesas-qr.md`](features/mesas-qr.md)

## 1. Objetivo

Que el mesero vea el salón de un vistazo, con colores y etiquetas claras, y que el comensal pueda pedir atención desde su mesa con un QR, sin cuenta ni descarga. La sesión de mesa y las solicitudes deben persistirse, no devolver mensajes fijos.

## 2. Estado actual

- `GET /tenant/tables` y `POST /tenant/tables` existen. La creación genera `qr_token` con `secrets.token_urlsafe(32)` y estado `available`.
- Los modelos ya contienen `restaurant_tables`, `table_sessions` y `service_requests`, con estados definidos por `CHECK`.
- No hay endpoints para abrir, cerrar ni consultar la sesión de una mesa, ni para listar o atender solicitudes.
- `GET /public/table/{token}` y `POST /public/table/{token}/requests` son stubs: devuelven textos fijos y no consultan la base de datos (RT-13).
- La tabla permite `number` único, `capacity` entre 1 y 50 y estados `available`, `occupied`, `pending_payment`, `reserved` e `inactive`. No hay campos de piso, zona, etiqueta visible ni motivo de cierre en el modelo.
- No hay restricción en base de datos que garantice una sola sesión activa por mesa.
- `/admin/mesas` es informativa; `/r/{slug}/mesa/{token}` no consume la API.

## 3. Alcance de esta feature

Incluye:

1. Resolver el token del QR contra la mesa del tenant correcto y devolver una sesión real.
2. Crear o reanudar una sola sesión activa por mesa.
3. Persistir solicitudes de atención con tipo, hora y estado.
4. Listar y atender solicitudes desde el panel del restaurante.
5. Abrir y liberar mesa con los dos botones definidos (D-157), con roles.
6. Cierre de sesión por pago confirmado (gancho para BL-12) o por decisión del mesero con motivo y sin pedido pendiente (D-159).
7. Pantallas de salón y de mesa del comensal conectadas a la API.
8. Panel de selección por piso y zona con colores: libre en verde, ocupada en rojo y reservada en azul (D-157).
9. Etiqueta visible generada por el backend desde la configuración: numérico o número con zona (D-158).

Queda fuera:

- Cobro, pasarela y comprobante (BL-12). Esta feature solo expone el gancho de cierre por pago.
- Creación de pedidos desde el QR: el QR únicamente permite solicitudes (D-110).
- Esquema de piso, grupo con nombre y mesa (`#2BA-02`): evolución sin fecha (D-158).
- Reservas y disponibilidad: siguen en P1 con BL-11 (D-160). El color azul se prepara, pero no se activa hasta que exista el flag por tenant.
- Rate limiting en las solicitudes públicas (BL-16).

## 4. Contrato

Base: `/api/v1`. Las rutas `/tenant/*` usan cookie y tenant resuelto en servidor (D-106). Las rutas `/public/table/*` usan solo el token opaco del QR, sin cookie y sin `tenant_id` del cliente.

### 4.1 Endpoints existentes

| Método | Ruta | Uso | Estado |
|---|---|---|---|
| GET | `/tenant/tables` | Lista mesas y estado | Implementado |
| POST | `/tenant/tables` | Crea mesa y token QR | Implementado |

### 4.2 Endpoints a añadir o completar

| Método | Ruta | Uso | Respuesta |
|---|---|---|---|
| GET | `/tenant/tables/{id}` | Detalle de mesa y sesión | 200 + mesa |
| PATCH | `/tenant/tables/{id}` | Cambiar número, capacidad o estado | 200 + mesa |
| POST | `/tenant/tables/{id}/sessions` | Abrir o reanudar sesión | 200 + sesión |
| POST | `/tenant/tables/{id}/close` | Cerrar sesión y liberar mesa | 200 + sesión cerrada |
| GET | `/tenant/service-requests` | Listar solicitudes pendientes | 200 + lista |
| PATCH | `/tenant/service-requests/{id}/attend` | Marcar solicitud atendida | 200 + solicitud |
| GET | `/public/table/{token}` | Resolver QR y sesión | 200 + mesa y sesión |
| POST | `/public/table/{token}/requests` | Enviar solicitud | 201 + solicitud |

### 4.3 Cuerpos

```text
PATCH mesa:        { "number": int > 0, "capacity": int 1..50, "floor": string | null, "zone_name": string | null, "status": string }
Cerrar mesa:       { "reason": string, "force": bool }
Solicitud pública: { "type": "waiter" | "bill" | "assistance" }
```

Los estados de mesa son `available`, `occupied`, `pending_payment`, `reserved` e `inactive`. `floor` y `zone_name` son opcionales: si el restaurante no los configura, la mesa se muestra en una lista plana. La etiqueta visible (`display_label`) la genera el backend y el cliente nunca la envía (D-158). Un comensal nunca envía estado, motivo ni identificador de mesa.

### 4.4 Respuesta pública

```text
{
  "table": { "display_label": string, "status": string },
  "session": { "id": uuid, "status": "active" | "closed", "opened_at": datetime }
}
```

La respuesta pública no incluye `qr_token`, `capacity` sensible, datos de otras mesas ni datos de pedidos.

### 4.5 Códigos de error

`TABLE_NOT_FOUND`, `INVALID_TOKEN`, `SESSION_CLOSED`, `SESSION_ALREADY_ACTIVE`, `INVALID_REQUEST_TYPE`, `REQUEST_NOT_FOUND`, `FORBIDDEN`, `INVALID_STATUS`, `CLOSE_REASON_REQUIRED`, `TABLE_HAS_OPEN_ORDER`, `NOT_FOUND`.

Un token inexistente, revocado o de una mesa inactiva devuelve `404`, sin distinguir entre casos.

## 5. Diseño

### 5.1 Resolución del QR

```text
GET /public/table/{token}
  ├── validar formato del token (opaco, 43 caracteres en la generación actual)
  ├── resolver mesa por qr_token en el schema del tenant
  ├── verificar mesa activa
  ├── buscar sesión activa → si existe, reanudarla
  ├── si no existe, crear sesión y poner mesa en occupied
  └── devolver etiqueta visible, estado y sesión
```

El tenant se resuelve por el token, que es único por mesa dentro del schema. La petición pública no abre una ruta de administración ni filtra el slug de otros restaurantes.

### 5.2 Sesión única

- Una mesa tiene como máximo una sesión con `status = "active"`.
- Se añade un índice único parcial sobre `table_id` para sesiones activas; el servicio también comprueba el estado antes de crear.
- Un QR antiguo sobre una sesión cerrada abre una sesión nueva solo si la mesa sigue activa; no reabre la cerrada (RN-143).
- La sesión no caduca por tiempo (RN-144).

### 5.3 Solicitudes

- `POST /public/table/{token}/requests` solo acepta si hay sesión activa; si no, devuelve `404 SESSION_CLOSED`.
- Cada solicitud guarda `session_id`, `type`, `status = "pending"` y `created_at`.
- El panel lista solicitudes `pending` con mesa y hora; `PATCH /attend` cambia a `attended` y guarda `attended_at`.
- El comensal ve el estado de sus propias solicitudes; nunca las de otra mesa.

### 5.4 Cierre de mesa

- Al confirmarse un pago, BL-12 invocará el cierre de la sesión y dejará la mesa `available`.
- Los dos botones del panel son «ocupar mesa» y «liberar mesa» (D-157). No hay tercera acción de estado en el MVP.
- Liberar exige motivo (`RN-146`) y que no haya sesión activa ni pedido sin cobrar (D-159). Sin motivo, `422 CLOSE_REASON_REQUIRED`; con operación pendiente, `422 TABLE_HAS_OPEN_ORDER`.
- Si el mesero fuerza el cierre con `force = true`, se permite, pero se guarda `close_reason`, `forced_by` y `forced_at` para trazabilidad.
- El cierre guarda `closed_at`, `close_reason`, marca la sesión `closed` y la mesa `available`.
- `pending_payment` se usa mientras hay pedido sin cobrar; `reserved` se reserva para BL-11 y solo se muestra si el tenant activa reservas (D-160).

### 5.5 Roles

| Acción | Roles |
|---|---|
| Listar mesas y solicitudes | `owner`, `admin`, `waiter`, `cook` (cocina ve número y estado, sin solicitudes de texto) |
| Crear y editar mesa | `owner`, `admin` |
| Abrir y cerrar sesión | `owner`, `admin`, `waiter` |
| Atender solicitud | `owner`, `admin`, `waiter` |
| Enviar solicitud | anónimo con token válido |

### 5.6 Panel y etiquetas

- `tenant_settings` guarda `table_label_scheme` (`numeric` | `zone`) y los nombres de piso/zona que configura el CEO.
- `display_label` se calcula en el backend: con esquema `numeric`, `01`, `02`, …; con esquema `zone`, el número dentro de la zona precedido del nombre o código de zona. No se edita a mano (D-158).
- El panel agrupa tarjetas por piso y zona. Cada tarjeta muestra la etiqueta visible, el color del estado y un botón de acción.
- Colores: verde para `available`, rojo para `occupied` y `pending_payment`, azul para `reserved`. El azul solo aparece cuando el tenant tiene activadas las reservas (D-160).
- Un cambio de esquema recalcula las etiquetas; el `id` interno de la mesa nunca cambia, de modo que pedidos, sesiones y QR siguen apuntando a la misma mesa.

## 6. Flujos

### 6.1 Crear mesa y entregar QR

1. El CEO o administrador crea mesa con número y capacidad.
2. El backend genera el token opaco y lo devuelve en `qr_token`.
3. El panel genera el código QR a partir de `/r/{slug}/mesa/{token}` (D-124), sin subdominios.
4. Se descarga o imprime; el token nunca se muestra en una lista pública.

### 6.2 Comensal escanea

1. Abre la URL del QR.
2. El backend resuelve el token, crea o reanuda la sesión y devuelve mesa y sesión.
3. La pantalla muestra el número de mesa y tres acciones: llamar al mesero, falta algo, pedir la cuenta.
4. Cada acción envía una solicitud y muestra confirmación.

### 6.3 Mesero atiende

1. `/admin/mesas` muestra el salón con estados y solicitudes pendientes.
2. El mesero ve mesa, tipo de solicitud y hora.
3. Marca «atendida»; el cambio se refleja sin recargar.
4. Si la mesa sigue ocupada, puede cerrarla indicando motivo.

### 6.4 Cierre por pago

1. BL-12 confirma el cobro por webhook firmado.
2. Se cierra la sesión activa y la mesa pasa a `available`.
3. El QR sigue siendo válido, pero ya no abre la sesión anterior.

### 6.5 Operar el salón desde el panel

1. El mesero abre `/admin/mesas` y ve tarjetas agrupadas por piso y zona, con la etiqueta visible y el color del estado.
2. Para ocupar, toca «ocupar mesa»; la tarjeta pasa a rojo y se crea la sesión.
3. Para liberar, toca «liberar mesa», escribe el motivo y confirma; si hay pedido sin cobrar, el backend lo bloquea y explica por qué.
4. Si decide forzar, marca la opción; la acción queda registrada con motivo, usuario y hora.
5. Las solicitudes pendientes aparecen sobre la tarjeta de su mesa.

## 7. Archivos a crear o modificar

| Archivo | Acción | Contenido |
|---|---|---|
| `backend/app/tables/router.py` | Modificar | Detalle, edición, sesión, cierre y solicitudes |
| `backend/app/tables/service.py` | Modificar | Resolución de token, sesión única y reglas de cierre |
| `backend/app/tables/repository.py` | Modificar | Consultas por token, sesión activa y solicitudes |
| `backend/app/tables/schemas.py` | Modificar | Respuesta pública, cierre y solicitudes |
| `backend/app/tables/models.py` | Modificar | `floor`, `zone_name`, `display_label`, `close_reason`, `forced_by` y `forced_at` |
| `backend/app/sites/models.py` | Modificar | `table_label_scheme` en la configuración del tenant |
| `backend/app/public/router.py` | Modificar | Sustituir los stubs por consultas reales |
| `backend/migrations/versions/` (cadena tenant) | Crear | Campos de mesa, etiqueta y cierre; índice único parcial de sesión activa |
| `backend/tests/` | Crear | Pruebas de token, etiqueta, sesión única, solicitudes, colores y cierre |
| `frontend/src/lib/tables.ts` | Crear | Funciones de mesas y solicitudes sobre `apiFetch` |
| `frontend/src/app/(ceo-portal)/admin/mesas/page.tsx` | Modificar | Panel por piso/zona con colores, etiquetas y dos botones |
| `frontend/src/app/(ceo-portal)/admin/mesas/[id]/page.tsx` | Crear | Detalle de mesa, sesión y cierre |
| `frontend/src/app/(public-site)/mesa/[token]/page.tsx` | Modificar | Vista del comensal conectada a la API |
| `docs/04-backend/api.md` | Modificar | Endpoints nuevos |
| `docs/04-backend/features/mesas-qr.md` | Modificar | Estado real y enlace a esta especificación |
| `docs/05-frontend/features/mesas-qr.md` | Modificar | Estado de pantallas y enlace a esta especificación |

No se crea ninguna ruta de pago ni de pedido desde el QR.

## 8. Estados obligatorios por pantalla

| Pantalla | Cargando | Vacío | Error | Sin permiso |
|---|---|---|---|---|
| `/admin/mesas` | Esqueleto del salón | «Aún no hay mesas.» | Reintento | «No tienes acceso al salón» |
| Detalle de mesa | «Cargando sesión…» | «La mesa no tiene sesión activa.» | Reintento | Mensaje por rol |
| Mesa del comensal | «Buscando tu mesa…» | No aplica | «No encontramos esta mesa. Pide ayuda al personal.» | No aplica |
| Solicitudes | «Enviando…» | «No hay solicitudes pendientes.» | Reintento | No aplica |
| Cierre de mesa | «Cerrando…» | No aplica | Motivo obligatorio | «Solo mesero o administración» |

Los botones de la vista pública tienen texto visible y tamaño suficiente para uso con una mano (D-131).

## 9. Pruebas requeridas

1. Crear mesa devuelve token opaco y estado `available`.
2. Un token válido crea sesión y pone la mesa `occupied`.
3. Escanear dos veces el mismo QR reanuda la sesión, sin crear otra.
4. Una segunda sesión activa sobre la misma mesa se rechaza o reanuda la existente.
5. Un token inexistente, de mesa inactiva o de sesión cerrada devuelve `404`.
6. Una solicitud pública se persiste y aparece en el panel con mesa y hora.
7. Un cocinero ve número y estado, pero no el texto de solicitudes.
8. `PATCH /attend` cambia la solicitud a `attended` con `attended_at`.
9. Cerrar mesa sin motivo devuelve `422 CLOSE_REASON_REQUIRED`.
10. Cerrar mesa libera la mesa y marca la sesión como `closed`.
11. Cerrar mesa con pedido sin cobrar devuelve `422 TABLE_HAS_OPEN_ORDER`; con `force = true` se permite y guarda quién, cuándo y por qué.
12. Un `waiter` cierra mesa; un `cook` no puede hacerlo.
13. Con esquema `numeric`, la etiqueta generada es `01`, `02`, …; con esquema `zone`, incluye la zona configurada. El cliente no puede enviar `display_label`.
14. Cambiar el esquema recalcula etiquetas sin cambiar el `id` interno ni invalidar sesiones ni QR.
15. El panel agrupa por piso/zona y aplica verde a libre, rojo a ocupada y azul a reservada solo si el tenant activó reservas.
16. Ninguna respuesta pública contiene `qr_token`, datos de otras mesas ni datos de pedidos.
17. La solicitud sobre una sesión cerrada devuelve `404 SESSION_CLOSED`.
18. La vista pública funciona con `/r/{slug}/mesa/{token}` y con teclado.

## 10. Criterios de aceptación

- [ ] Los endpoints públicos consultan la base de datos y ya no devuelven mensajes fijos.
- [ ] Una mesa tiene como máximo una sesión activa.
- [ ] Las solicitudes se persisten y se atienden desde el panel.
- [ ] El cierre requiere motivo, sin pedido pendiente, y libera la mesa.
- [ ] El cierre forzado queda registrado con usuario, hora y motivo.
- [ ] La etiqueta visible se genera en el backend y no se edita desde el cliente.
- [ ] El panel muestra tarjetas por piso/zona con colores y dos botones.
- [ ] El token inválido devuelve `404` sin revelar el motivo.
- [ ] El QR no crea pedidos.
- [ ] La respuesta pública no expone datos de otras mesas ni del tenant.
- [ ] Los roles de D-146 se respetan en escrituras.
- [ ] `/admin/mesas` y la vista del comensal consumen la API real.

## 11. Dependencias

- BL-01: cliente HTTP y manejo de errores.
- BL-02: sesión del personal y roles para las acciones del panel.
- BL-03: el menú público convive con la vista de mesa, pero no se mezclan datos.
- BL-04: `table_session_id` del pedido debe apuntar a una sesión real.
- BL-12: cierre de mesa por webhook de pago firmado.
- BL-11: estados `reserved` y gestión de reservas, activables por tenant (D-160). La ventana y el solape se rigen por D-161 cuando se implemente.
- D-106 y D-124: tenant en servidor y ruta pública por slug.
- D-157, D-158, D-159, D-160 y D-161: panel, etiquetas, cierre, reservas y solape.
- Deuda RT-13 en [`07-calidad/deuda-tecnica.md`](../07-calidad/deuda-tecnica.md).

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Token predecible o enumerable | Generación aleatoria de 32 bytes y búsqueda exacta por token |
| Dos sesiones activas por concurrencia | Índice único parcial y comprobación en la misma transacción |
| Filtrar mesas de otro tenant | El `search_path` limita la búsqueda al schema activo |
| QR reabre sesión cerrada | Comprobar estado; abrir una nueva solo si la mesa sigue activa |
| Solicitudes sin control de frecuencia | Documentar como deuda BL-16; no bloquear la feature |
| Cerrar mesa con pedido sin cobrar | Bloqueo con `TABLE_HAS_OPEN_ORDER`; el cierre forzado queda registrado |
| Exponer datos del comensal en cocina | Respuesta de cocina con campos explícitos |
| Etiquetas duplicadas o confusas | Las genera el backend desde la configuración; nunca se editan a mano |
| Mesa reservada ocupada por un comensal | Validación de solape de D-161 cuando BL-11 se implemente; hoy el color azul no se activa |

## 13. Definición de terminado

Se considera terminada cuando se cumplen los criterios de aceptación, pasan las pruebas del punto 9, CI pasa con lint, tests y build, y se verifica manualmente un ciclo completo: configurar el esquema de etiquetas, crear mesa, comprobar su etiqueta y color en `/admin/mesas`, abrir el QR desde `/r/{slug}/mesa/{token}`, enviar «llamar al mesero», ver y atender la solicitud, liberar la mesa con motivo y confirmar que el QR ya no reanuda la sesión cerrada.
