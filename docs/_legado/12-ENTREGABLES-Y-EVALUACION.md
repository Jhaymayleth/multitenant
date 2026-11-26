# 12 — Entregables, rúbrica y sustentación

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Uso:** preparar la entrega y ensayar la defensa oral
**Última actualización:** 22 de octubre de 2026

---

## 1. Entregables obligatorios

| # | Entregable | Dónde | Estado |
|---|---|---|---|
| 1 | Repositorio con historial de commits coherente | Repositorio | Pendiente de código |
| 2 | `README.md` con los cinco puntos del enunciado | Raíz | Plantilla en §3 |
| 3 | `docker-compose.yml` | Raíz | Diseño en `10-ENTORNO-Y-DESPLIEGUE.md` |
| 4 | `.env.example` sin secretos | Raíz | Diseño en `10-ENTORNO-Y-DESPLIEGUE.md` |
| 5 | Pipeline CI funcionando | `.github/workflows/ci.yml` | Diseño en `10-ENTORNO-Y-DESPLIEGUE.md` |
| 6 | Sustentación oral individual | — | Guion en §4 |

---

## 2. Mapa de la rúbrica

| Criterio | Puntos | Cómo se cumple | Evidencia |
|---|---|---|---|
| Multitenancy y aislamiento | 25 | Schema por tenant, creación automática, resolución en servidor, pruebas cruzadas | `03-ARQUITECTURA.md`, `07-MODELO-DATOS.md`, `tests/security/` |
| Autenticación y seguridad | 15 | JWT en cookie httpOnly, rutas protegidas, roles, CSRF | `08-SEGURIDAD-Y-ACCESO.md`, `tests/security/` |
| Idempotencia | 15 | Crear tenant y crear pedido con `Idempotency-Key`, tabla con TTL, prueba de conteo | `09-ROBUSTEZ.md`, `tests/robustness/test_idempotency.py` |
| Rate limiting | 15 | Token bucket en Redis, login y escrituras, 429 + `Retry-After` | `09-ROBUSTEZ.md`, `tests/robustness/test_rate_limit.py` |
| Arquitectura y organización | 10 | Monolito modular por dominios, capas, lint, tipado | `03-ARQUITECTURA.md`, estructura de carpetas |
| Docker y CI/CD | 10 | Compose con healthchecks, pipeline que falla ante errores | `10-ENTORNO-Y-DESPLIEGUE.md` |
| Sustentación y documentación | 10 | README completo, demo ensayada, decisiones explicables | Este documento + `README.md` |
| **IA (opcional)** | +10 | Descripción de productos y consultas con contexto aislado, caché y límites | `04-MODULOS.md` §13 |
| **Automatización (opcional)** | +10 | Webhook firmado a n8n al crear tenant, con reintentos | `05-PENDIENTES.md` P-21 |

**Prioridad:** sin los 90 puntos base, los opcionales no compensan.

---

## 3. Contenido del `README.md`

El enunciado exige cinco puntos. Estructura sugerida:

```markdown
# Lixus — SaaS multitenant para restaurantes

## 1. Qué es y por qué este nicho
Restaurantes independientes que necesitan menú, pedidos, reservas y presencia
pública sin pagar un sistema a medida. Un tenant = un restaurante.

## 2. Arquitectura multitenant
- Schema `platform`: usuarios, tenants, membresías, planes.
- Un schema `tenant_<id>` por restaurante.
- Diagrama de componentes.
- Por qué schema por tenant y no tablas compartidas.

## 3. Cómo levantar el proyecto
cp .env.example .env
docker compose up --build
migraciones y seed
URLs locales

## 4. Cómo se resuelve el tenant en cada petición
1. JWT en cookie httpOnly.
2. Validación de firma y expiración.
3. Membresía activa en la base de datos.
4. `schema_name` obtenido del servidor.
5. `SET LOCAL search_path` dentro de la transacción.
6. Prueba de acceso cruzado.

## 5. Idempotencia y rate limiting
- Clave `Idempotency-Key`, tabla, índice único, TTL 24 h, reproducción de respuesta.
- Token bucket en Redis, límites por usuario/tenant, 429 + Retry-After.
- Por qué se eligió cada estrategia.

## 6. Estrategias de renderizado
SSG/ISR en página pública, CSR en panel. Justificación.

## 7. Pruebas y CI
Comandos, qué cubre cada suite, evidencia.
```

Cada afirmación del README debe poder demostrarse con código o con una prueba.

---

## 4. Guion de sustentación (10–12 minutos)

### 4.1 Antes de empezar

- [ ] `docker compose up` ya ejecutado y servicios saludables.
- [ ] Datos demo creados: dos tenants, un usuario en ambos, otro solo en A.
- [ ] Pestañas abiertas: navegador, terminal, editor, base de datos.
- [ ] Cookies visibles en DevTools.
- [ ] Pipeline verde en pantalla.

### 4.2 Secuencia

| Min | Acción | Mensaje |
|---|---|---|
| 1 | Mostrar la arquitectura y el diagrama | "Una aplicación, dos schemas: plataforma y tenant." |
| 2 | `docker compose ps` | "Todo se levanta con un comando; hay healthchecks." |
| 3 | Crear un tenant desde la API o portal | "El schema se crea automáticamente; el nombre lo genera el servidor." |
| 4 | `\dn` en PostgreSQL | "Aquí están los schemas de los dos restaurantes." |
| 5 | Login y DevTools | "La cookie es httpOnly; no hay token en localStorage." |
| 6 | Usuario A pide un pedido de B por ID | "404: no se confirma ni la existencia." |
| 7 | Cambiar un `tenant_id` en el body | "El servidor lo ignora y usa el de la membresía." |
| 8 | Repetir `POST /orders` con la misma clave | "Mismo resultado, un solo registro." |
| 9 | `SELECT count(*)` | "La prueba lo confirma." |
| 10 | Seis intentos de login | "429 con Retry-After." |
| 11 | Abrir la página pública | "SSG/ISR: HTML listo para SEO, sin sesión." |
| 12 | Abrir el panel | "CSR: datos privados, sin caché." |

### 4.3 Modificación en vivo

El docente puede pedir cambiar algo. Practicar al menos:

1. Añadir un campo o endpoint sencillo (por ejemplo, `is_featured` en productos).
2. Cambiar el límite de rate limiting en configuración.
3. Mostrar la consulta que selecciona el schema.
4. Añadir una validación de precio.

---

## 5. Preguntas esperadas y respuestas cortas

**¿Cómo se crea el schema de un tenant?**
Un endpoint de Lixus valida el permiso, inserta el tenant con estado `provisioning`, genera un nombre `tenant_<hex>` en el servidor, ejecuta `CREATE SCHEMA`, aplica las migraciones de Alembic con `version_table_schema`, crea el CEO y marca el tenant como activo. Todo queda auditado y protegido por idempotencia.

**¿Cómo eliges la conexión/schema en cada petición?**
El JWT identifica al usuario y su tenant activo. La API valida la membresía en `platform.tenant_memberships`, lee `schema_name` de la base de datos y ejecuta `SELECT set_config('search_path', 'tenant_x, platform', true)` dentro de la transacción. `SET LOCAL` evita contaminar el pool.

**¿Qué pasa si el usuario manipula el `tenant_id`?**
Se ignora para autorizar. El tenant siempre sale del token validado y de la membresía. Si el recurso es de otro tenant, se responde 404.

**¿Dónde guardas las claves de idempotencia y cuánto tiempo?**
En PostgreSQL, en `idempotency_keys`, con índice único `(scope, key)`, huella del cuerpo y respuesta guardada. TTL de 24 horas y purga diaria. Se eligió PostgreSQL y no Redis porque la escritura de la clave debe ser atómica con la escritura de negocio.

**¿Qué pasa si llegan dos peticiones iguales a la vez?**
El `INSERT ... ON CONFLICT` decide un ganador; el segundo espera el bloqueo de fila y recibe la respuesta guardada o un 409 si aún está en curso.

**¿Qué estrategia de rate limiting usaste y por qué?**
Token bucket con Redis y Lua. Permite ráfagas cortas legítimas, usa memoria constante y es atómico entre instancias. La ventana fija permitiría el doble de peticiones en el cambio de ventana.

**¿Qué pasa si Redis se cae?**
El login responde 503 (fail-closed) para no permitir fuerza bruta; las escrituras normales siguen con fail-open y alerta; la IA se bloquea porque el costo es real. La política está declarada por endpoint.

**¿Cómo evitas dos reservas en la misma mesa y hora?**
Con una restricción de exclusión de PostgreSQL sobre `tstzrange`, no con un "consultar y luego insertar". La base de datos rechaza el solapamiento y la API devuelve 409.

**¿Cómo proteges la cookie contra CSRF?**
`SameSite=Lax`, verificación de `Origin` y doble envío de un token CSRF en un header. La cookie de sesión es `HttpOnly`, así que el JavaScript no puede leerla.

**¿Qué pasa si un empleado es desactivado?**
Se revoca la membresía, se incrementa la versión de sesión del usuario y se añade el `jti` a la lista de revocación en Redis. El token anterior deja de servir de inmediato.

**¿Cómo se separan los clientes de los empleados?**
Son actores distintos. El cliente tiene una cuenta y un perfil en el schema del tenant, sin permisos de panel. El empleado tiene una membresía con rol. Una identidad puede existir en varios tenants sin compartir datos.

**¿Por qué schema por tenant y no `tenant_id`?**
Porque el aislamiento es estructural y es requisito del enunciado. El costo es administrar migraciones por schema y el contexto de conexión; se automatiza y se prueba.

**¿Qué pasa con los datos si un plan vence?**
Se conservan. Se restringen funciones premium y se mantiene el acceso para renovar o exportar. Nunca se elimina el schema por impago.

**¿Qué estrategias de renderizado usaste?**
SSG/ISR en la página pública y el menú (SEO y primera carga), CSR en el panel y el portal (datos privados y dependientes de sesión).

**¿Qué harías con más tiempo?**
Cobro automático con pasarela, inventario, multi-sucursal y endurecimiento de producción (respaldos, observabilidad, secretos gestionados). Está priorizado en `05-PENDIENTES.md`.

---

## 6. Puntos opcionales: cómo ganarlos

### 6.1 IA (+10)

- Generar descripción de un producto con Groq.
- Contexto construido en el backend con el tenant activo.
- Caché por producto y versión de la descripción.
- Rate limit propio y manejo explícito del 429 del proveedor.
- Registro de consumo por tenant.
- Demostrar que un prompt malicioso no accede a otro tenant.

### 6.2 Automatización (+10)

- Webhook firmado al crear un tenant.
- n8n recibe y envía un correo de bienvenida.
- Reintentos con backoff y registro de fallos.
- Explicar qué pasa si el flujo falla: el alta del tenant no se revierte, el evento queda pendiente.

### 6.3 Otros

- Despliegue público con HTTPS.
- Pruebas de aislamiento automatizadas (ya previstas).
- Roles dentro del tenant (ya previstos).

---

## 7. Checklist final de entrega

**Código**
- [ ] `docker compose up` funciona desde cero.
- [ ] Lint y build pasan.
- [ ] Pipeline verde.
- [ ] Sin secretos ni `.env` versionado.
- [ ] Commits con mensajes coherentes.

**Multitenancia**
- [ ] Schema creado automáticamente.
- [ ] Dos tenants aislados.
- [ ] Pruebas de acceso cruzado.
- [ ] `search_path` seguro en concurrencia.

**Autenticación**
- [ ] Cookie httpOnly verificada en DevTools.
- [ ] Rutas privadas protegidas.
- [ ] Roles y permisos comprobados en servidor.
- [ ] CSRF mitigado.

**Caja y pagos**
- [ ] La caja registra el pago e imprime el comprobante con QR de descarga.
- [ ] Un webhook firmado de sandbox libera la mesa sin intervención del mesero (pasarela real no, registro en caja no).
- [ ] - No se almacenan datos de tarjeta ni se expone el secreto del webhook.
- No hay pasarela real en la entrega académica: el pago en línea se confirma con proveedor simulado por webhook firmado, no con una pasarela ni con registro manual en caja.

**Robustez**
- [ ] Dos operaciones idempotentes.
- [ ] Webhook de pago deduplicado por `provider_event_id`.
- [ ] Retención de claves explicada.
- [ ] 429 con `Retry-After`.
- [ ] Límite por usuario/tenant.
- [ ] Pruebas automatizadas.

**Documentación**
- [ ] README con los cinco puntos.
- [ ] Diagrama de arquitectura.
- [ ] Decisiones y pendientes actualizados.
- [ ] Guion de sustentación ensayado.

---

## 8. Autoevaluación rápida

| Pregunta | Si la respuesta es "no", revisar |
|---|---|
| ¿Puedo crear un tenant en vivo sin tocar SQL manual? | `03-ARQUITECTURA.md` §2.3 |
| ¿Puedo mostrar el schema creado en PostgreSQL? | Misma sección |
| ¿Puedo demostrar que A no ve B? | `08-SEGURIDAD-Y-ACCESO.md` §12 |
| ¿Puedo explicar el `SET LOCAL search_path`? | `03-ARQUITECTURA.md` §2.4 |
| ¿Puedo repetir un pedido sin duplicarlo? | `09-ROBUSTEZ.md` Parte I |
| ¿Puedo provocar un 429 y mostrar `Retry-After`? | `09-ROBUSTEZ.md` Parte II |
| ¿Puedo explicar por qué el token no está en localStorage? | `08-SEGURIDAD-Y-ACCESO.md` §4 |
| ¿Puedo justificar SSG en público y CSR en panel? | `03-ARQUITECTURA.md` §4.2 |

Si todas son "sí", la entrega está lista.

---

**Fin de `12-ENTREGABLES-Y-EVALUACION.md`.**
