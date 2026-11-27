# Especificación técnica: BL-03 menú CRUD

**Estado:** Especificación lista para implementar
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería
**Feature:** [`01-producto/backlog.md`](../01-producto/backlog.md) → BL-03
**Decisiones:** D-106 (tenant en servidor), D-123 (español), D-131 (accesibilidad en menú), D-146 (roles)
**Fichas espejo:** [`04-backend/features/menu.md`](../04-backend/features/menu.md) · [`05-frontend/features/menu.md`](features/menu.md)

## 1. Objetivo

Que el restaurante pueda mantener su carta desde el panel: crear, editar, ordenar, retirar y borrar categorías y productos, y decidir qué se ve en la página pública. El menú deja de ser un texto informativo y pasa a leer y escribir datos reales del tenant.

## 2. Estado actual

- El backend tiene `GET` y `POST` de categorías y productos en `/tenant/menu`; no hay `PUT`, `DELETE` ni acciones de publicación.
- `price_cents` acepta `0` (`ge=0`); la regla RN-131 exige precio mayor que cero.
- `category_id` es opcional en el schema y en la tabla; la regla RN-132 exige categoría del mismo tenant.
- No hay control de orden de productos: el repositorio ordena por nombre.
- No existe el campo `is_published` en `menu_products`; solo `is_active`. La publicación del sitio se rige por `tenant_settings.is_published`.
- El menú público (`GET /public/{slug}/menu`) filtra solo por `is_active`, sin comprobar publicación ni categoría activa.
- La validación de nombre duplicado dentro de la categoría (RN-133) no está implementada.
- `/admin/menu` es una página estática: no hay `fetch`, formularios ni estados de carga o error.
- Las imágenes se aceptan como `image_url` libre; no hay carga a almacenamiento (R2 sigue prevista, ver [`03-arquitectura/integraciones.md`](../03-arquitectura/integraciones.md)).
- La deuda RT-01 (frontend sin API) y RT-20 (errores inconsistentes) siguen abiertas; esta feature las aplica al dominio de menú, no las cierra en todo el sistema.

## 3. Alcance de esta feature

Incluye:

1. Completar el CRUD de categorías: editar nombre, orden y estado; borrar con reglas.
2. Completar el CRUD de productos: editar nombre, descripción, precio, categoría, imagen, disponibilidad y publicación.
3. Validaciones en servidor: precio mayor que cero, categoría del mismo tenant, nombre único por categoría.
4. Orden de productos dentro de la categoría.
5. Borrado lógico que no rompe pedidos históricos.
6. Filtrado del menú público por sitio publicado, categoría activa, producto activo y producto publicado.
7. Pantalla `/admin/menu` conectada a la API, con formularios y estados.
8. Mensajes de error en español derivados del contrato de `error.code`.

Queda fuera:

- Carga real de imágenes a R2 y URLs firmadas. El campo `image_url` se mantiene y se valida como URL; la subida se implementa cuando exista `StorageProvider` configurado.
- Publicación de la página completa, branding y horarios (BL-06).
- Snapshot de precio en pedidos (BL-04). El precio del catálogo no se reescribe en pedidos ya creados.
- Idempotencia en escrituras (BL-17), rate limiting (BL-16) y auditoría (BL-19).
- Cambios en el contrato de autenticación ni en el middleware de rutas públicas (BL-01).
- Duplicar productos, importación masiva y multi-sucursal (fuera de la versión inicial, D-122).

## 4. Contrato

Base: `/api/v1`. Autenticación por cookie `lixus_session`; el tenant se resuelve en el servidor desde la sesión (D-106). El cliente nunca envía `tenant_id`.

### 4.1 Endpoints existentes

| Método | Ruta | Uso | Estado |
|---|---|---|---|
| GET | `/tenant/menu/categories` | Lista categorías del tenant | Implementado |
| POST | `/tenant/menu/categories` | Crea categoría (`owner`, `admin`) | Implementado |
| GET | `/tenant/menu/products` | Lista productos; filtro `category_id` | Implementado |
| POST | `/tenant/menu/products` | Crea producto (`owner`, `admin`) | Implementado |

### 4.2 Endpoints a añadir

| Método | Ruta | Uso | Respuesta |
|---|---|---|---|
| PUT | `/tenant/menu/categories/{id}` | Editar nombre, orden y estado | 200 + categoría |
| DELETE | `/tenant/menu/categories/{id}` | Retirar categoría | 204 sin cuerpo |
| PUT | `/tenant/menu/products/{id}` | Editar producto | 200 + producto |
| DELETE | `/tenant/menu/products/{id}` | Retirar producto | 204 sin cuerpo |
| PATCH | `/tenant/menu/products/{id}/publication` | Publicar u ocultar | 200 + producto |
| PATCH | `/tenant/menu/products/{id}/order` | Reordenar dentro de la categoría | 200 + producto |

### 4.3 Cuerpos propuestos

```text
Categoría (PUT):
{ "name": string, "display_order": int >= 0, "is_active": bool }

Producto (PUT):
{
  "category_id": uuid,
  "name": string,
  "description": string | null,
  "price_cents": int > 0,
  "image_url": string | null,
  "is_active": bool,
  "is_published": bool,
  "display_order": int >= 0
}

Publicación (PATCH): { "is_published": bool }
Orden (PATCH): { "display_order": int >= 0 }
```

Los campos `price_cents`, `is_active` e `is_published` se validan en el servidor. El frontend no calcula ni envía totales; solo edita el catálogo.

### 4.4 Respuestas y errores

- `200` lectura o actualización, `201` creación, `204` borrado.
- Error objetivo: `{ "error": { "code": "...", "message": "...", "request_id": "..." } }`.
- Hoy algunas rutas devuelven `{"detail": "..."}`. El cliente acepta ambos formatos sin mostrar internos (BL-01, RT-20, RT-21).
- Códigos de esta feature: `CATEGORY_IN_USE`, `CATEGORY_NOT_FOUND`, `PRODUCT_NOT_FOUND`, `DUPLICATE_PRODUCT_NAME`, `INVALID_PRICE`, `INVALID_CATEGORY`, `SITE_NOT_PUBLISHED`, `FORBIDDEN`.
- `403` cuando el rol no permite escribir; `404` para recursos de otro tenant, sin revelar si existen.
- `GET /public/{slug}/menu` devuelve `404` si el sitio no está publicado y `[]` si no hay productos publicados.

## 5. Diseño

### 5.1 Servicio y repositorio

```text
MenuService
  ├── valida precio (> 0) y longitud de texto
  ├── comprueba que la categoría pertenece al schema activo
  ├── controla nombre único por categoría (sin distinción de mayúsculas)
  ├── aplica borrado lógico: is_active = false
  └── escribe display_order y updated_at

MenuRepository
  ├── list_categories(only_active)
  ├── list_products(category_id, only_active, only_published)
  └── ordena por display_order ascendente y nombre como desempate
```

El schema del tenant ya aísla los datos (D-103, D-106). No se añade `tenant_id` a estas tablas. Una categoría de otro tenant no existe en el `search_path` activo y se trata como `404`.

### 5.2 Publicación

- `is_active`: el producto está disponible para la operación del restaurante.
- `is_published`: el producto se muestra en la página pública.
- Un producto publicado pero inactivo no se muestra; un producto activo sin publicar tampoco.
- La categoría debe estar activa para que sus productos aparezcan en la página.
- El sitio debe estar publicado (`tenant_settings.is_published`). Esta feature solo consume ese estado; no lo edita.

### 5.3 Borrado

- Producto: `DELETE` marca `is_active = false` e `is_published = false`. Los pedidos históricos conservan su snapshot de nombre y precio.
- Categoría con productos activos: `409 CATEGORY_IN_USE` con mensaje «Mueve o retira los productos antes de borrar la categoría».
- Categoría vacía: borrado lógico (`is_active = false`). No se elimina la fila.

### 5.4 Imágenes

- Si `image_url` viene vacío, el producto se muestra sin imagen.
- El frontend valida extensiones y tamaño antes de enviar; el backend valida el tipo de URL y rechaza esquemas distintos de `https` en producción.
- La subida real queda fuera de esta feature; el campo no bloquea el CRUD.

## 6. Flujos

### 6.1 Crear o editar una categoría

1. El usuario abre `/admin/menu` con sesión de rol `owner` o `admin`.
2. Escribe nombre y orden; guarda.
3. El backend valida longitud y nombre duplicado en el tenant; devuelve la categoría.
4. El frontend actualiza la lista sin recargar y muestra confirmación.

### 6.2 Crear o editar un producto

1. Elige categoría, nombre, descripción, precio en centavos, imagen opcional, disponibilidad y publicación.
2. El frontend muestra el precio convertido a la moneda del tenant solo para lectura; envía `price_cents` entero.
3. El backend valida precio, categoría y nombre único; guarda.
4. Con precio `0` o categoría inexistente, muestra mensaje concreto y mantiene el formulario abierto.

### 6.3 Retirar una categoría o un producto

1. El usuario confirma la acción.
2. Si la categoría tiene productos activos, el backend devuelve `409` y el frontend explica qué hacer.
3. Si no, se marca como inactivo y desaparece de la vista del panel.
4. El producto retirado deja de mostrarse en la página pública.

### 6.4 Publicar u ocultar

1. El usuario activa o desactiva «Publicado» en el producto.
2. `PATCH /products/{id}/publication` actualiza solo ese campo.
3. El menú público refleja el cambio en la siguiente consulta; sin caché que lo retrase.

### 6.5 Reordenar

1. El usuario sube o baja el producto dentro de su categoría.
2. `PATCH /products/{id}/order` recibe el nuevo `display_order`.
3. El backend normaliza los valores de la categoría para evitar empates y devuelve la lista ordenada.

### 6.6 Menú público

1. El navegador pide `GET /public/{slug}/menu`.
2. El backend resuelve el tenant por slug, comprueba que el sitio esté publicado y filtra categoría activa, producto activo y producto publicado.
3. Devuelve la lista ordenada, con nombre, descripción, precio y categoría.
4. La vista `/r/{slug}/menu` muestra estados de carga, vacío y error (D-124, D-131).

## 7. Archivos a crear o modificar

| Archivo | Acción | Contenido |
|---|---|---|
| `backend/app/menus/models.py` | Modificar | `is_published` y `display_order` en `MenuProduct` |
| `backend/app/menus/schemas.py` | Modificar | Esquemas de edición, publicación y orden; `price_cents > 0`; categoría obligatoria |
| `backend/app/menus/service.py` | Modificar | Reglas RN-131 a RN-135 y borrado lógico |
| `backend/app/menus/repository.py` | Modificar | Filtros de publicación y orden por `display_order` |
| `backend/app/menus/router.py` | Modificar | `PUT`, `DELETE` y `PATCH` con `require_role("owner", "admin")` |
| `backend/migrations/versions/` (cadena tenant) | Crear | Migración de los campos nuevos y restricción de nombre único |
| `backend/app/public/router.py` | Modificar | Filtro de publicación del menú público |
| `backend/tests/` | Crear | Pruebas de CRUD, validación, roles y publicación |
| `frontend/src/app/(ceo-portal)/admin/menu/page.tsx` | Modificar | Lista, formularios y acciones conectadas |
| `frontend/src/lib/menu.ts` | Crear | Funciones de menú sobre `apiFetch` de BL-01 |
| `frontend/src/components/menu/` | Crear | Formularios de categoría y producto, confirmación de borrado |
| `docs/04-backend/api.md` | Modificar | Endpoints nuevos |
| `docs/04-backend/features/menu.md` | Modificar | Estado del contrato y enlace a esta especificación |
| `docs/05-frontend/features/menu.md` | Modificar | Estado de pantallas y enlace a esta especificación |

No se cambia el contrato de autenticación ni el middleware de rutas públicas.

## 8. Estados obligatorios por pantalla

| Pantalla | Cargando | Vacío | Error | Sin permiso |
|---|---|---|---|---|
| `/admin/menu` | Esqueleto de lista | «Aún no hay categorías. Crea la primera.» | Mensaje con reintento | «No tienes acceso a esta sección» |
| Formulario de categoría | Botón «Guardando…» | No aplica | Error de nombre duplicado o longitud | No aplica |
| Formulario de producto | Botón «Guardando…» | No aplica | Precio, categoría o nombre inválidos | No aplica |
| Confirmación de borrado | Botón «Retirando…» | No aplica | `CATEGORY_IN_USE` con acción sugerida | No aplica |
| `/r/{slug}/menu` | Esqueleto de tarjetas | «Este restaurante aún no publica su menú.» | Error con reintento | No aplica |

Todos los mensajes van en español, sin trazas ni URLs internas (D-123). Los controles mantienen etiquetas visibles y foco al navegar con teclado (D-131).

## 9. Pruebas requeridas

1. Crear, editar y retirar una categoría con rol `owner` y con rol `admin`.
2. Un mesero o cocinero puede listar, pero no crear, editar ni borrar.
3. Crear, editar y retirar un producto.
4. Un producto con `price_cents = 0` se rechaza con `INVALID_PRICE`.
5. Un producto sin categoría o con categoría de otro tenant se rechaza con `INVALID_CATEGORY`.
6. Dos productos con el mismo nombre en una categoría se rechazan con `DUPLICATE_PRODUCT_NAME`; el mismo nombre en categorías distintas se acepta.
7. Borrar una categoría con productos activos devuelve `409 CATEGORY_IN_USE`.
8. El producto retirado no aparece en el menú público; un pedido anterior conserva su snapshot.
9. Un producto inactivo no se publica aunque `is_published` esté en `true`.
10. Con el sitio sin publicar, `/public/{slug}/menu` devuelve `404`.
11. El orden de la página pública respeta `display_order`.
12. Un producto de otro tenant no se puede editar ni borrar; devuelve `404`.
13. La pantalla `/admin/menu` muestra carga, vacío, error y éxito sin recargar.
14. El menú público pasa la revisión de teclado y contraste de los flujos críticos (D-131).

## 10. Criterios de aceptación

- [ ] Existen `PUT` y `DELETE` de categorías y productos, y `PATCH` de publicación y orden.
- [ ] `price_cents` es mayor que cero en creación y edición.
- [ ] La categoría es obligatoria y pertenece al tenant activo.
- [ ] El nombre no se duplica dentro de una categoría.
- [ ] El borrado es lógico y no altera pedidos anteriores.
- [ ] La categoría con productos activos no se puede borrar.
- [ ] El menú público respeta sitio publicado, categoría activa, producto activo y producto publicado.
- [ ] El orden de categorías y productos se respeta en panel y página pública.
- [ ] `/admin/menu` consume la API real y muestra los cuatro estados obligatorios.
- [ ] Solo `owner` y `admin` escriben; `mesero` y `cocinero` solo leen (D-146).
- [ ] Los errores se muestran en español y no filtran datos del backend.
- [ ] La ficha backend y la ficha frontend reflejan el estado terminado.

## 11. Dependencias

- BL-01: `apiFetch` y `AppError` en `frontend/src/lib/api.ts`; sin ellos no hay conexión real.
- D-106: resolución del tenant en servidor; no se acepta `tenant_id` del cliente.
- D-146: matriz de permisos ya aprobada para los guards.
- D-124: ruta pública `/r/{slug}`; el menú público se sirve bajo esa ruta.
- `NEXT_PUBLIC_API_URL` definida en build (ver [`06-infra-ops/variables-entorno.md`](../06-infra-ops/variables-entorno.md)).
- Cadena Alembic de tenant operativa (ver [`04-backend/migraciones.md`](../04-backend/migraciones.md)).
- BL-06 publicará el sitio; esta feature solo consume `tenant_settings.is_published`.
- BL-04 tomará nombre y precio del catálogo al crear el pedido.
- Deuda RT-01 y RT-20 en [`07-calidad/deuda-tecnica.md`](../07-calidad/deuda-tecnica.md).
- D-162 aprueba Elasticsearch como índice de búsqueda de menú; queda fuera de esta feature y se registra como RT-27. La lista actual no ofrece búsqueda dedicada.

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Publicar sin que el sitio esté publicado genera confusión | El menú público comprueba ambos estados y devuelve `404` si el sitio no está listo |
| Cambiar un precio rompe pedidos en curso | El pedido guarda snapshot; el catálogo nunca reescribe líneas existentes |
| Borrar una categoría deja productos huérfanos | `409 CATEGORY_IN_USE` y borrado solo de categorías vacías |
| El frontend muestre precios sin la moneda del tenant | Formatear desde la configuración del tenant; nunca inventar símbolo ni cifra |
| Errores con formatos distintos | Normalizar `detail` y `error` en `AppError` (BL-01) |
| Campos nuevos sin migración en tenants existentes | Migración en la cadena de tenant, probada en schema limpio y existente |
| Subida de imágenes sin proveedor | El campo `image_url` se valida; la subida real queda para cuando exista `StorageProvider` |
| Reordenar con valores duplicados | Normalizar `display_order` en servidor después de cada cambio |

## 13. Definición de terminado

Se considera terminada cuando se cumplen todos los criterios de aceptación, pasan las pruebas listadas en el punto 9, CI pasa con lint, tests y build, y se verifica manualmente un ciclo completo en un tenant de prueba: entrar como `owner`, crear categoría y producto, editar precio, publicar, comprobar el menú en `/r/{slug}/menu`, retirar el producto y confirmar que desaparece sin afectar pedidos anteriores.
