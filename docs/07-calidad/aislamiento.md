# Especificación técnica: BL-08 aislamiento entre tenants

**Estado:** Especificación lista para implementar
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería
**Feature:** [`01-producto/backlog.md`](../01-producto/backlog.md) → BL-08
**Decisiones:** D-103 (schema por tenant), D-106 (tenant en servidor), D-117 (plataforma interina), D-146 (roles), D-151 (foco en MVP)
**Documentos relacionados:** [`03-arquitectura/multitenancy.md`](../03-arquitectura/multitenancy.md) · [`03-arquitectura/seguridad.md`](../03-arquitectura/seguridad.md) · [`07-calidad/estrategia-pruebas.md`](estrategia-pruebas.md)

## 1. Objetivo

Dejar evidencia de que un restaurante no puede leer ni modificar datos de otro, ni con credenciales propias, ni manipulando la URL, el cuerpo, el slug público o el `search_path`. El aislamiento es la base del producto multitenant; sin prueba negativa no se puede afirmar que funciona.

## 2. Estado actual

- El modelo es un schema por tenant más el schema `platform` (D-103). No hay columna `tenant_id` en las tablas del tenant.
- `set_tenant_schema` valida el nombre con `^tenant_[a-f0-9]{12}$` y aplica `set_config('search_path', :sp, true)` dentro de la transacción.
- Un listener `after_begin` reaplica el `search_path` tras cada transacción nueva para evitar fugas por reutilización del pool.
- `get_tenant_context` valida token, tenant activo, membresía activa y rol desde base de datos antes de fijar el schema.
- `require_role` restringe escrituras por rol; `/platform/*` y `/audit` usan la clave interina `X-Platform-Admin-Key` (D-117).
- Existen dos pruebas de integración: `test_products_are_isolated_between_tenants` y `test_cross_tenant_login_is_rejected`.
- La prueba de seguridad `test_isolation_poc.py` solo comprueba que una ruta privada sin sesión devuelve `401`.
- No hay pruebas de concurrencia en el pool, de `schema_name` inválido, de sustitución de `tenant_id` en el cuerpo, de dominio público cruzado ni de escalada de roles.
- No hay RLS ni `SET ROLE`; la aplicación conecta con un rol con privilegios amplios en algunos entornos (RT-17).

## 3. Alcance de esta feature

Incluye:

1. Una matriz de pruebas negativas que cubra todas las rutas del tenant.
2. Pruebas de concurrencia sobre el pool de conexiones.
3. Pruebas de rechazo de `schema_name` y `tenant_id` manipulados.
4. Pruebas de que las rutas públicas solo devuelven el tenant del slug.
5. Pruebas de que el rol de la membresía manda sobre el rol del token.
6. Ejecución de las pruebas en CI con base de datos inicializada.
7. Registro de los límites que quedan para después del MVP.

Queda fuera:

- Activar RLS o `SET ROLE` por petición: defensa adicional, no sustituto del schema (RT-17, P1).
- Reducir privilegios del rol de base de datos en producción: se documenta como deuda P1.
- Cambiar el modelo de autenticación ni la clave interina de plataforma.
- Reescribir las pruebas de negocio de menú, pedidos o sitio público; estas solo prueban el límite entre tenants.

## 4. Contrato de aislamiento

Esta feature no añade endpoints. Verifica las siguientes invariantes:

| Invariante | Cómo se comprueba |
|---|---|
| El tenant se resuelve en servidor desde sesión y membresía (D-106) | Petición con cookie válida; respuesta solo con datos de ese tenant |
| El cliente no elige schema ni tenant | Body y headers con `tenant_id` o `schema_name` extraños se ignoran o se rechazan |
| El `search_path` se fija por transacción | Dos sesiones concurrentes sobre tenants distintos no se cruzan |
| La membresía activa se revalida en cada petición | Desactivar la membresía corta el acceso sin esperar a que expire el token |
| El rol de la membresía manda | Token con rol inventado no autoriza operación reservada a `owner` |
| Las rutas públicas usan solo el slug | `/public/{slugB}/menu` no devuelve datos de A; slug inexistente devuelve `404` |
| La clave de plataforma no abre datos operativos | Sin clave, `/platform/*` y `/audit` devuelven `403` o `503`; con clave, no devuelven pedidos de tenant |
| Un recurso de otro tenant no se distingue | UUID de otra tenant devuelve `404`, no `403` con detalle |

Los errores no revelan si un identificador pertenece a otro restaurante.

## 5. Diseño de las pruebas

### 5.1 Fixtures

```text
tenant A + usuario owner A
tenant B + usuario owner B
usuario waiter A y usuario cook A
cookie A, cookie B, cookie waiter A, cookie cook A
cliente HTTP con TestClient contra /api/v1
base de datos PostgreSQL inicializada por CI
```

Cada prueba aprovisiona sus propios tenants con slugs únicos y usa `Idempotency-Key` en el alta. Los datos de ejemplo son genéricos; no se usan nombres de clientes reales.

### 5.2 Matriz por endpoint

| Dominio | Ruta | Prueba negativa |
|---|---|---|
| Menú | `/tenant/menu/products`, `/tenant/menu/categories` | B no ve productos de A; no edita un producto de A por UUID |
| Pedidos | `/tenant/orders`, `/tenant/orders/{id}` | B no ve ni abre el pedido de A |
| Mesas | `/tenant/tables` | B no ve mesas ni tokens QR de A |
| Solicitudes | `/tenant/service-requests` | B no atiende solicitudes de A |
| Sitio | `/tenant/public-site` | B no edita la configuración de A |
| Personal | `/tenant/staff` | B no lista personal de A |
| Pagos | `/tenant/payments` | B no ve cobros de A |
| Público | `/public/{slug}`, `/public/{slug}/menu` | Solo el tenant del slug; slug inexistente → `404` |
| Plataforma | `/platform/tenants`, `/audit` | Sin clave → rechazo; con clave → sin datos operativos |

### 5.3 Concurrencia

1. Abrir dos sesiones en paralelo, una con `search_path` de A y otra con el de B.
2. Escribir un producto distinto en cada una y hacer varios commits intermedios.
3. Leer desde cada sesión y comprobar que cada una ve solo su producto.
4. Repetir con reutilización de la misma conexión del pool.

### 5.4 Manipulación

- Enviar `tenant_id`, `schema_name` y `X-Tenant` en body/headers con valores de B usando cookie de A; la petición debe ignorarlos o rechazarlos.
- Enviar un `schema_name` con caracteres fuera del patrón permitido; debe rechazarse antes de ejecutar SQL.
- Cambiar el `tenant_id` del payload del token por el de B; la firma debe fallar con `401`.

### 5.5 Roles

- Token con rol `owner` del tenant A pero membresía real `cook`: la operación de publicar sitio se rechaza con `403`.
- `cook` no ve datos personales en la cola de cocina.
- Empleado desactivado: petición con token vigente se rechaza al revalidar la membresía.

## 6. Flujos de ejecución

### 6.1 En local

1. Levantar PostgreSQL de prueba y aplicar las dos cadenas Alembic.
2. Ejecutar `pytest -m integration` y `pytest tests/security`.
3. Repetir las pruebas de concurrencia cinco veces para detectar fugas intermitentes.

### 6.2 En CI

1. El pipeline crea la base, aplica migraciones y ejecuta las pruebas antes del build de imágenes.
2. Una prueba fallida bloquea el merge a `develop`.
3. El resultado queda en el log de CI; no se publica evidencia manual sustituyendo a la automática.

### 6.3 Antes de un despliegue

1. Verificar que las pruebas de aislamiento estén en verde en la rama que se publica.
2. Repetir manualmente el caso de dos tenants con el menú de BL-03 y el pedido de BL-04.
3. Anotar el resultado en el registro de release de [`07-calidad/release.md`](release.md).

## 7. Archivos a crear o modificar

| Archivo | Acción | Contenido |
|---|---|---|
| `backend/tests/conftest.py` | Modificar | Fixtures de dos tenants, usuarios y cookies |
| `backend/tests/integration/test_tenant_isolation.py` | Ampliar | Matriz del punto 5.2 y manipulación del punto 5.4 |
| `backend/tests/security/test_isolation_poc.py` | Ampliar | Concurrencia, roles y platform sin clave |
| `backend/tests/integration/test_public_slug_isolation.py` | Crear | Pruebas de rutas públicas por slug |
| `backend/app/core/dependencies.py` | Modificar solo si falla | Refuerzo de revalidación o rechazo de cabeceras |
| `backend/app/core/database.py` | Modificar solo si falla | Ajuste del `search_path` por transacción |
| `.github/workflows/ci.yml` | Modificar | Ejecutar todas las pruebas de aislamiento con base inicializada |
| `docs/07-calidad/estrategia-pruebas.md` | Modificar | Enlace a esta especificación |
| `docs/03-arquitectura/multitenancy.md` | Modificar | Enlace a esta especificación en el apartado de pruebas |

No se cambia el contrato HTTP de ninguna feature.

## 8. Estados de verificación

| Estado | Significado |
|---|---|
| SIN EJECUTAR | La prueba existe pero no se ha ejecutado en CI |
| FALLIDA | Hay un caso que permite cruce entre tenants |
| EN VERDE | Todos los casos pasan con PostgreSQL real |
| VERIFICADA EN RELEASE | además, se repitió manualmente antes del despliegue |

Hoy las dos pruebas de integración están implementadas; el resto de la matriz está `SIN EJECUTAR` o no existe.

## 9. Pruebas requeridas

1. Usuario de A no lee productos de B.
2. Usuario de A no edita ni borra un producto de B por UUID conocido.
3. Usuario de A no ve pedidos de B ni abre un pedido de B por UUID.
4. Usuario de A no ve mesas ni tokens QR de B.
5. Usuario de A no atiende solicitudes de B.
6. Usuario de A no edita la configuración pública de B.
7. Usuario de A no ve personal ni cobros de B.
8. Token de A en una ruta de B devuelve `403` o `404`.
9. `tenant_id` y `schema_name` en body o headers no cambian el tenant resuelto.
10. Un `schema_name` fuera del patrón permitido se rechaza antes de SQL.
11. Dos sesiones concurrentes no comparten `search_path` aunque reutilicen conexión.
12. `/public/{slugB}/menu` nunca devuelve productos de A; slug inexistente → `404`.
13. Sin clave de plataforma, `/platform/*` y `/audit` responden `403` o `503`.
14. Con clave de plataforma, no se devuelven datos operativos de ningún tenant.
15. Un token con rol manipulado no autoriza una escritura; la membresía manda.
16. Un empleado desactivado pierde acceso con token vigente.
17. Un `cook` no ve datos personales en la cola de cocina.

## 10. Criterios de aceptación

- [ ] La matriz del punto 5.2 cubre todas las rutas de tenant del contrato vigente.
- [ ] Los 17 casos del punto 9 están implementados y pasan con PostgreSQL real.
- [ ] Las pruebas se ejecutan en CI antes del build de imágenes.
- [ ] No existe acceso cruzado por UUID, slug, body, header ni token.
- [ ] El `search_path` no se filtra con concurrencia ni con commits intermedios.
- [ ] Los errores no revelan pertenencia de un recurso a otro tenant.
- [ ] Los límites sin cerrar (RLS, rol de BD) están documentados como deuda P1.

## 11. Dependencias

- D-103 y D-106 cerrados: schema por tenant y resolución en servidor.
- BL-01 a BL-06: las rutas que se prueban deben existir con su contrato final.
- PostgreSQL real en CI, con base inicializada y migraciones aplicadas.
- D-117 para la clave interina de plataforma.
- D-146 para la matriz de roles probada.
- Deuda RT-17 en [`07-calidad/deuda-tecnica.md`](deuda-tecnica.md).

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Fuga intermitente por pool de conexiones | Prueba de concurrencia repetida y `SET LOCAL` reaplicado por transacción |
| Cruce por UUID conocido | El `search_path` acota la consulta y se devuelve `404` |
| Cruce por slug público | Resolución de tenant por slug y filtro en todas las consultas públicas |
| Escalada por rol del token | Recalcular rol desde la membresía en cada petición |
| Pruebas que usen base simulada | Ejecutar siempre con PostgreSQL real en CI |
| Falsa sensación de seguridad | Documentar que no hay RLS ni rol de privilegios mínimos |
| Matriz incompleta al añadir rutas nuevas | Toda feature nueva del tenant añade su caso negativo antes de terminar |

## 13. Definición de terminado

Se considera terminada cuando los 17 casos pasan en CI con PostgreSQL real, no hay acceso cruzado en la matriz de rutas, se registró una verificación manual con dos tenants y el documento de deuda mantiene RT-17 como pendiente de P1. Una feature del tenant no se marca como terminada si añade una ruta sin su caso negativo de aislamiento.
