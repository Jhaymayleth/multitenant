# 09 — Robustez: idempotencia, rate limiting y concurrencia

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Diseño listo para implementar y demostrar
**Requisitos:** RAC-04, RAC-05 (obligatorios del enunciado)
**Decisiones aplicadas:** D-062, D-063
**Última actualización:** 22 de octubre de 2026

---

## 1. Por qué este documento es crítico

La evaluación asigna **15 puntos a idempotencia y 15 a rate limiting**, y ambos se demuestran en vivo. No basta con que el código exista: hay que poder explicar dónde se guardan las claves, cuánto duran, qué pasa con dos peticiones simultáneas y por qué se eligió cada estrategia.

---

# Parte I — Idempotencia

## 2. Definición operativa

Una operación es idempotente cuando ejecutarla varias veces con la misma intención produce **el mismo resultado** y **un solo efecto**. El cliente envía una clave única por intención:

```
Idempotency-Key: 4f8c2a1e-9b3d-4c7a-8f11-2d6e5a9c0b34
```

Si repite la petición (reintento de red, doble clic, timeout), recibe la respuesta original sin crear otro registro.

## 3. Operaciones cubiertas

| Operación | Ruta | Scope | Justificación |
|---|---|---|---|
| Crear tenant | `POST /platform/tenants` | `platform:create_tenant` | Operación costosa: crea schema y tablas |
| Crear pedido | `POST /tenant/orders` | `order:create` | Riesgo real de pedidos duplicados por doble clic |
| Confirmar pago | `POST /tenant/payments/{id}/confirm` | `payment:confirm` | Evita cobros y liberaciones de mesa duplicadas |
| Webhook de pago | `POST /webhooks/payments/{provider}` | `payment:webhook` | Evento firmado; se deduplica por `provider_event_id` |
| Crear reserva (opcional) | `POST /tenant/reservations` | `reservation:create` | Refuerza la demostración |

El mínimo exigido son dos; se implementan las tres primeras de forma obligatoria. El webhook no usa `Idempotency-Key`: se deduplica por `provider_event_id` en `payment_events`.

## 4. Reglas de la clave

1. Obligatoria en los endpoints marcados: sin ella se responde **400** con código `IDEMPOTENCY_KEY_REQUIRED`.
2. Longitud 8–255 caracteres; se recomienda UUID v4 generado por el cliente.
3. Se guarda **hasheada** o indexada, nunca se usa como identificador visible.
4. La misma clave con **cuerpo distinto** se rechaza con **422** `IDEMPOTENCY_KEY_REUSED`.
5. La misma clave con el **mismo cuerpo** devuelve la respuesta original y añade `Idempotent-Replay: true`.
6. Una clave pertenece a un scope y a un tenant; no se comparte entre operaciones.
7. Vigencia por defecto: **24 horas** (`IDEMPOTENCY_TTL_HOURS`), configurable.
8. **Excepción:** los webhooks de pago no llevan `Idempotency-Key`; su clave es `provider_event_id`, única por proveedor.

## 5. Almacenamiento

Tabla `idempotency_keys` (global para tenants, por schema para pedidos; ver `07-MODELO-DATOS.md`):

| Columna | Uso |
|---|---|
| `scope` + `key` | Índice único: garantiza una sola ejecución |
| `request_hash` | Detecta reutilización con cuerpo distinto |
| `status` | `in_progress`, `completed`, `failed` |
| `response_status` / `response_body` | Reproducción exacta |
| `expires_at` | Purga automática |

La unicidad la impone **PostgreSQL**, no la aplicación. Eso resuelve la carrera entre dos peticiones simultáneas con la misma clave.

## 6. Flujo de ejecución

```
POST /tenant/orders  (Idempotency-Key: K)
   │
   ├─ 0. Validar sesión, tenant y permiso
   ├─ 1. Calcular fingerprint = sha256(método + ruta + body canónico + tenant cuando aplique)
   ├─ 2. INSERT INTO idempotency_keys (scope, key, request_hash, status, expires_at)
   │       VALUES ('order:create', K, F, 'in_progress', now() + 24h)
   │       ON CONFLICT (scope, key) DO NOTHING
   │       RETURNING id
   │
   ├─ 3a. Si insertó (primera vez):
   │       BEGIN
   │         crear pedido + líneas + totales
   │         UPDATE idempotency_keys
   │            SET status='completed', response_status=201, response_body=<json>
   │         COMMIT
   │       Devolver 201
   │
   └─ 3b. Si hubo conflicto:
           SELECT ... FOR UPDATE
           ├─ request_hash distinto        → 422 IDEMPOTENCY_KEY_REUSED
           ├─ status = 'in_progress'       → 409 REQUEST_IN_PROGRESS
           ├─ status = 'completed'         → reproducir respuesta + Idempotent-Replay
           └─ status = 'failed'            → permitir reintento o devolver error original
```

**Atomicidad:** el pedido y el registro de idempotencia se confirman en la **misma transacción**. Si falla el segundo, no queda pedido huérfano.

**Concurrencia:** la fila bloqueada serializa el reintento; la segunda petición espera y recibe la respuesta guardada, o un 409 si aún está en curso.

## 7. Caso especial: crear un tenant

Crear un schema implica DDL y ejecutar Alembic, que no conviven cómodamente en una sola transacción con el registro de idempotencia. Estrategia:

1. Insertar tenant con estado `provisioning` y la clave de idempotencia en una transacción.
2. Ejecutar la creación del schema y las migraciones.
3. Marcar `active` o `pending_verification` y guardar la respuesta.
4. Si falla, marcar `provisioning_failed` y conservar el error.
5. Un reintento con la misma clave:
   - si está `completed`, devuelve el tenant existente;
   - si está `failed`, reintenta la provisión **del mismo** tenant (no crea otro schema);
   - si está `in_progress`, devuelve 409.

La clave evita duplicar tenants; el estado del tenant evita duplicar schemas. Son dos garantías complementarias.

## 8. Retención y limpieza

- TTL predeterminado: 24 h. Las claves vencidas no se consultan.
- Job diario: `DELETE FROM idempotency_keys WHERE expires_at < now()`.
- Motivo de 24 h: cubre reintentos y dobles clics reales sin acumular datos innecesarios.
- La respuesta almacenada no contiene tokens ni datos sensibles.

## 9. Códigos de respuesta

| Situación | Código | Cuerpo |
|---|---|---|
| Primera ejecución correcta | 201 | Recurso creado |
| Reintento idéntico | 201/200 | Respuesta original + `Idempotent-Replay: true` |
| Falta la clave | 400 | `IDEMPOTENCY_KEY_REQUIRED` |
| Misma clave, cuerpo distinto | 422 | `IDEMPOTENCY_KEY_REUSED` |
| Petición concurrente en curso | 409 | `REQUEST_IN_PROGRESS` |
| Error de negocio en la primera ejecución | 4xx | Se guarda y se reproduce |

## 10. Prueba de demostración

```bash
KEY=$(uuidgen)

# Primera petición
curl -i -X POST http://localhost:8000/api/v1/tenant/orders \
  -H "Cookie: lixus_session=$TOKEN" \
  -H "X-CSRF-Token: $CSRF" \
  -H "Idempotency-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"table_id":"...","items":[{"product_id":"...","quantity":2}]}'

# Segunda petición idéntica
curl -i -X POST http://localhost:8000/api/v1/tenant/orders \
  -H "Cookie: lixus_session=$TOKEN" \
  -H "X-CSRF-Token: $CSRF" \
  -H "Idempotency-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"table_id":"...","items":[{"product_id":"...","quantity":2}]}'

# Verificación en base de datos
psql -c "SELECT count(*) FROM tenant_xxx.orders;"
# Esperado: 1 (no 2)
```

También se automatiza en `tests/security/test_idempotency.py`:
primera petición 201, segunda 201 con `Idempotent-Replay`, conteo = 1, cuerpo distinto → 422, dos hilos simultáneos → un solo pedido.

## 11. Qué explicar en la sustentación

- **Dónde se guardan:** en PostgreSQL, en `idempotency_keys`, con índice único `(scope, key)`.
- **Cuánto se conservan:** 24 horas configurables; purga diaria.
- **Qué pasa con dos peticiones a la vez:** el `INSERT ... ON CONFLICT` decide un ganador; el perdedor espera y reproduce.
- **Qué pasa si el cliente cambia el cuerpo:** 422, porque la clave representa una intención, no una autorización para cualquier contenido.
- **Por qué no se usa Redis:** la garantía debe sobrevivir a un reinicio y ser atómica con la escritura de negocio; PostgreSQL ya ofrece esa transacción.
- **Por qué la confirmación de pago también es idempotente:** además de no cobrar dos veces, libera la mesa; repetirla no debe cerrar otra sesión ni dejar la mesa en un estado inconsistente.
- **Cómo se deduplica un webhook:** por `provider_event_id` en `payment_events`; los proveedores reintentan, así que la clave no puede ser la del cliente.

---

# Parte II — Rate limiting

## 12. Objetivo

Evitar abuso de autenticación y de creación de recursos, sin afectar el uso normal. Al exceder el límite: **429** con `Retry-After`.

## 13. Alcance por endpoint

| Endpoint | Clave del límite | Límite inicial | Ventana |
|---|---|---|---|
| `POST /auth/login` | IP + correo | 5 intentos | 15 min |
| `POST /auth/register` | IP | 3 registros | 1 h |
| `POST /auth/forgot-password` | IP + correo | 3 solicitudes | 1 h |
| `POST /platform/tenants` | usuario Lixus | 5 | 1 h |
| `POST /tenant/orders` | tenant + usuario | 60 | 1 min |
| `POST /tenant/reservations` | tenant + usuario | 30 | 1 min |
| `POST /public/table/{token}/requests` | sesión de mesa | 10 | 1 min |
| `POST /tenant/ai/*` | tenant + usuario | 10 | 1 min + cuota diaria |
| Resto de escrituras autenticadas | tenant + usuario | 120 | 1 min |

**Por qué no solo por IP:** varios empleados comparten la red del restaurante; limitar por IP bloquearía a todo el local por culpa de uno. Se usa `tenant + usuario` cuando hay sesión, con respaldo por IP para anónimos.

## 14. Estrategia elegida: token bucket con Redis

### 14.1 Comparación

| Algoritmo | Ventaja | Desventaja | Decisión |
|---|---|---|---|
| Ventana fija | Muy simple | Permite ráfagas dobles en el cambio de ventana | Descartado |
| Ventana deslizante (log) | Preciso | Más memoria por usuario | Descartado para el MVP |
| **Token bucket** | Ráfagas controladas, memoria constante, atómico con Lua | Requiere script | **Elegido** |
| GCRA | Muy eficiente | Más difícil de explicar | Alternativa |

### 14.2 Funcionamiento

Cada clave tiene un cubo con capacidad `burst` y recarga `rate` tokens por segundo. Cada petición consume un token; si no hay, se rechaza.

```
capacidad = 5, recarga = 5/900 s  →  login: 5 intentos y recarga lenta
capacidad = 60, recarga = 1/s     →  pedidos: 60 de golpe y 1/s sostenido
```

Implementación atómica con Lua en Redis:

```lua
-- KEYS[1] = bucket key
-- ARGV[1] = capacity, ARGV[2] = refill_per_second, ARGV[3] = now_ms, ARGV[4] = cost
local data = redis.call("HMGET", KEYS[1], "tokens", "ts")
local tokens = tonumber(data[1]) or tonumber(ARGV[1])
local last   = tonumber(data[2]) or tonumber(ARGV[3])
local now    = tonumber(ARGV[3])
local cap    = tonumber(ARGV[1])
local rate   = tonumber(ARGV[2])
local elapsed = math.max(0, now - last) / 1000
tokens = math.min(cap, tokens + elapsed * rate)
local allowed = tokens >= tonumber(ARGV[4])
if allowed then tokens = tokens - tonumber(ARGV[4]) end
redis.call("HMSET", KEYS[1], "tokens", tokens, "ts", now)
redis.call("PEXPIRE", KEYS[1], math.ceil((cap / rate) * 1000) + 60000)
local retry_after = 0
if not allowed then retry_after = math.ceil((tonumber(ARGV[4]) - tokens) / rate) end
return {allowed and 1 or 0, math.floor(tokens), retry_after}
```

El script es atómico: dos instancias de la API no pueden consumir el mismo token.

### 14.3 Respuesta al exceder

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 12
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1761180012
Content-Type: application/json

{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Demasiados intentos. Intenta de nuevo en 12 segundos."
  }
}
```

`Retry-After` se calcula con el tiempo necesario para recuperar un token, redondeado hacia arriba.

### 14.4 Claves en Redis

```
rl:login:{sha256(email)}:{ip}
rl:user:{tenant_id}:{user_id}:{route_group}
rl:ip:{ip}:{route_group}
rl:table:{session_id}
```

Se usa hash del correo para no almacenar datos personales en Redis.

### 14.5 Fallos de Redis

| Escenario | Política |
|---|---|
| Login y registro | **Fail-closed** (503), para no abrir la puerta a fuerza bruta |
| Escrituras normales | **Fail-open** con log y alerta, para no tumbar la operación |
| IA | Fail-closed en el endpoint de IA, porque el costo es real |

La política se declara por endpoint y se prueba.

### 14.6 Configuración

```env
RATE_LIMIT_ENABLED=true
REDIS_URL=redis://redis:6379/0
RATE_LIMIT_LOGIN_BURST=5
RATE_LIMIT_LOGIN_WINDOW_SECONDS=900
RATE_LIMIT_WRITE_BURST=120
RATE_LIMIT_WRITE_RATE_PER_SECOND=2
```

## 15. Pruebas de demostración

```bash
for i in $(seq 1 6); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"demo@lixus.test","password":"incorrecta"}'
done
# Esperado: 401,401,401,401,401,429
```

Verificar el header:

```bash
curl -i -X POST http://localhost:8000/api/v1/auth/login ... | grep -i retry-after
```

Pruebas automatizadas:

- Seis intentos → el sexto es 429.
- `Retry-After` es un entero positivo.
- Pasado el tiempo, vuelve a permitir.
- Dos tenants distintos no comparten cubo.
- Un usuario bloqueado no bloquea a otro del mismo tenant.
- Con Redis caído, login responde 503 y una escritura normal sigue funcionando.

## 16. Qué explicar en la sustentación

- **Estrategia:** token bucket.
- **Por qué:** permite ráfagas cortas y legítimas (varios meseros creando pedidos), mantiene memoria constante y se implementa de forma atómica en Redis; la ventana fija permitiría el doble de peticiones en el borde.
- **Dónde vive el estado:** Redis, con expiración automática.
- **Por qué por usuario/tenant:** una IP compartida en el restaurante castigaría a todo el local.
- **Qué pasa si Redis falla:** política explícita por endpoint, documentada y probada.

---

# Parte III — Concurrencia e integridad

## 17. Reservas sin solapamiento

Comprobar "¿está libre?" y luego insertar es vulnerable a carreras. La garantía se pone en la base de datos:

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE reservations
  ADD CONSTRAINT reservations_no_overlap
  EXCLUDE USING gist (
    table_id WITH =,
    tstzrange(start_at, start_at + (duration_minutes || ' minutes')::interval) WITH &&
  )
  WHERE (status IN ('requested','confirmed','seated'));
```

- Dos reservas simultáneas para la misma mesa y franja: una falla con error de exclusión, que se traduce en **409**.
- Si no se asigna mesa, no hay conflicto de recurso; se controla el aforo general (pendiente P-07).

## 18. Sesión única por mesa

```sql
CREATE UNIQUE INDEX table_sessions_one_open
  ON table_sessions (table_id)
  WHERE status = 'open';
```

Abrir dos sesiones a la vez para la misma mesa falla a nivel de base de datos. La API responde con la sesión existente si el token es válido, o con 409.

## 19. Pedidos y totales

- El pedido y sus líneas se crean en una transacción.
- Los totales se calculan en el servidor a partir de `menu_products.price_cents`.
- Al confirmar, se copian nombre y precio a la línea (snapshot).
- Un pedido confirmado no se edita; se cancela o se crea otro.
- El cambio de estado valida transiciones permitidas en el servicio y bloquea la fila (`SELECT ... FOR UPDATE`) cuando dos usuarios podrían competir.

### 19.1 Confirmación de pago y liberación de mesa

La confirmación del pago se ejecuta en una sola transacción:

1. Bloquea el pedido (`SELECT ... FOR UPDATE`).
2. Verifica que no exista un pago confirmado para ese pedido.
3. Registra `payments.confirmed_by` y `confirmed_at`.
4. Marca el pedido como `paid`.
5. Cierra la sesión de mesa con `close_reason = 'payment_confirmed'`.
6. Deja la mesa en `available`.

El endpoint exige `Idempotency-Key`. Dos confirmaciones simultáneas producen **un solo pago** y **una sola liberación**; la segunda recibe la respuesta original. Si el pedido no tiene sesión de mesa (domicilio), solo se registra el pago.

## 20. Numeración de comprobantes

- Secuencia propia por schema (`receipt_number_seq`).
- `nextval` es atómico y no reutiliza números.
- Los huecos por transacciones fallidas son aceptables; la unicidad no.

## 21. Estados y transiciones

Máquina de estados validada en el servicio:

```
payment: registered → pending → paid
                    └────────► refunded (excepcional, auditado)
```

Cualquier transición no declarada devuelve **422**. No se acepta cambiar el estado con un PATCH genérico.

## 22. Orden de bloqueos

Para evitar interbloqueos, las operaciones bloquean siempre en el mismo orden: `orders` → `order_items` → `payments` → `receipts`. Los reportes usan `READ COMMITTED` y no bloquean escrituras.

## 23. Pruebas de concurrencia

| ID | Prueba | Esperado |
|---|---|---|
| C-01 | Dos reservas simultáneas, misma mesa y hora | Una 201, otra 409 |
| C-02 | Dos aperturas de sesión para la misma mesa | Una sesión activa |
| C-03 | Dos pedidos con la misma `Idempotency-Key` | Un pedido |
| C-04 | Confirmar pedido mientras se edita | La edición falla con 409 |
| C-05 | Dos pagos simultáneos al mismo pedido | Se rechaza el segundo o se suma según regla definida |
| C-06 | 50 peticiones concurrentes a A y B | Cada una ve su schema |
| C-07 | Dos confirmaciones de pago simultáneas | Un pago y una liberación de mesa |
| C-08 | Webhook repetido y confirmación manual en paralelo | Un pago, una liberación y una respuesta consistente |

---

## 24. Checklist de robustez para la entrega

- [ ] Dos operaciones idempotentes implementadas y probadas.
- [ ] Tabla de claves con índice único y TTL.
- [ ] `Retry-After` presente en todas las respuestas 429.
- [ ] Límite aplicado por usuario/tenant además de por IP.
- [ ] Estrategia documentada y explicable.
- [ ] Pruebas automatizadas de idempotencia, límites y concurrencia en CI.
- [ ] Restricciones de base de datos para reservas y sesiones de mesa.
- [ ] Manejo de errores 409/422 con mensajes claros.

---

**Fin de `09-ROBUSTEZ.md`.**
