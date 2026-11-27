# Especificación técnica: BL-06 página pública

**Estado:** Especificación lista para implementar
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería
**Feature:** [`01-producto/backlog.md`](../01-producto/backlog.md) → BL-06
**Decisiones:** D-108 (página con plantilla común), D-109 (sin directorio ni publicidad cruzada), D-123 (español), D-124 (`/r/{slug}`), D-131 (accesibilidad), D-146 (roles), D-154 (secciones de la plantilla), D-155 (enlace de domicilio)
**Fichas espejo:** [`04-backend/features/sitio-publico.md`](../04-backend/features/sitio-publico.md) · [`05-frontend/features/sitio-publico.md`](features/sitio-publico.md)

## 1. Objetivo

Que el CEO pueda editar la información y la marca de su restaurante, publicar o despublicar la página y verla bajo `/r/{slug}` con el menú publicado, sin exponer datos de otros tenants ni del panel privado.

## 2. Estado actual

- `tenant_settings` es un singleton con `display_name`, `tagline`, `description`, `logo_url`, `hero_image_url`, colores, `sections`, `contact`, `address`, `hours` e `is_published` (nace en `false`).
- `GET /tenant/public-site` y `PUT /tenant/public-site` existen. Solo `owner` puede escribir.
- `PUT` crea el registro con `is_published=true` la primera vez y ignora `logo_url`, `hero_image_url`, `sections` y `contact` en las actualizaciones. No permite despublicar (RT-14).
- `GET /public/{slug}` filtra por `is_published`; como el update nunca publica de forma explícita, la página no puede entregarse de forma fiable.
- `GET /public/{slug}/menu` filtra solo por `is_active` y ordena por nombre; no aplica publicación ni orden del catálogo (se corrige en BL-03).
- La ruta del repositorio es `/menu` bajo un grupo de páginas públicas; la decisión vigente es `/r/{slug}` y `/r/{slug}/menu` (D-124), que BL-01 ajusta en el middleware.
- No hay vista previa, metadatos por restaurante ni subida de logo o imagen principal.
- `/admin/configuracion` es informativa y no consume la API.

## 3. Alcance de esta feature

Incluye:

1. Edición completa de textos, colores, horarios, contacto, secciones visibles, logo e imagen principal por URL.
2. Publicación y despublicación explícitas, separadas de la edición.
3. Página pública bajo `/r/{slug}`, con menú bajo `/r/{slug}/menu`.
4. Respuesta pública con solo los campos seguros del tenant del slug.
5. Metadatos básicos por restaurante: título, descripción y canonical de la ruta pública.
6. Vista previa local en `/admin/configuracion/preview`, sin publicar.
7. Enlace de domicilio configurable por el CEO; valor **POR DEFINIR** si no se provee (D-155).

Queda fuera:

- Subida real de logo e imágenes a R2; los campos se validan como URL `https` (BL-14 y `03-arquitectura/integraciones.md`).
- Reservas online y disponibilidad (BL-11).
- Dominio propio de la marca: PD-18 sigue abierto. El dominio exacto no se inventa.
- Directorio de restaurantes ni enlaces cruzados entre tenants (D-109).
- Enlaces desde la página pública al panel privado.

## 4. Contrato

Base: `/api/v1`. Las rutas `/tenant/*` usan cookie y tenant resuelto en servidor (D-106). Las rutas `/public/*` resuelven el tenant por slug.

### 4.1 Endpoints existentes

| Método | Ruta | Uso | Estado |
|---|---|---|---|
| GET | `/tenant/public-site` | Configuración del sitio | Implementado |
| PUT | `/tenant/public-site` | Edita configuración | Parcial |
| GET | `/public/{slug}` | Sitio publicado | Implementado |
| GET | `/public/{slug}/menu` | Menú publicado | Parcial (se corrige en BL-03) |

### 4.2 Endpoints a añadir o completar

| Método | Ruta | Uso | Respuesta |
|---|---|---|---|
| PUT | `/tenant/public-site` | Edita sin cambiar publicación | 200 + configuración |
| POST | `/tenant/public-site/publish` | Publica o despublica | 200 + configuración |
| GET | `/tenant/public-site/preview` | Datos para vista previa | 200 + configuración + menú |

### 4.3 Cuerpos

```text
PUT /tenant/public-site
{
  "display_name": string 2..255,
  "tagline": string | null,
  "description": string | null,
  "logo_url": string | null,
  "hero_image_url": string | null,
  "color_primary": "#rrggbb" | null,
  "color_secondary": "#rrggbb" | null,
  "sections": object,
  "contact": object,
  "address": string | null,
  "hours": object | null,
  "delivery_link": string | null
}

POST /tenant/public-site/publish
{ "is_published": bool }
```

`delivery_link` es el enlace externo que el restaurante quiere mostrar para domicilio. Su valor concreto es **POR DEFINIR**; Lixus no elige proveedor ni inventa URL. Si no se configura, la sección no se muestra.

### 4.4 Respuesta pública

```text
{
  "display_name": string,
  "tagline": string | null,
  "description": string | null,
  "logo_url": string | null,
  "hero_image_url": string | null,
  "color_primary": string | null,
  "color_secondary": string | null,
  "sections": object,
  "contact": object,
  "address": string | null,
  "hours": object | null,
  "delivery_link": string | null,
  "slug": string,
  "updated_at": datetime
}
```

No incluye `tenant_id`, `schema_name`, correos internos ni configuración de cobro.

### 4.5 Códigos de error

`SETTINGS_NOT_FOUND`, `SLUG_NOT_FOUND`, `SITE_NOT_PUBLISHED`, `INVALID_COLOR`, `INVALID_URL`, `INVALID_SECTION`, `FORBIDDEN`, `NOT_FOUND`.

## 5. Diseño

### 5.1 Servicio de configuración

```text
update_settings(data)
  ├── valida longitudes, colores y URLs
  ├── valida claves de sections contra las seis secciones aprobadas (D-154)
  ├── valida el enlace de domicilio si se provee (https)
  ├── escribe todos los campos, incluidos logo, hero, sections, contact y delivery_link
  ├── NO toca is_published
  └── guarda updated_at

publish(is_published)
  ├── requiere rol owner
  ├── exige display_name y al menos una sección visible
  └── cambia solo is_published
```

Separar edición y publicación evita que un guardado parcial deje la página visible a medias.

### 5.2 Secciones permitidas

La plantilla común admite `hero`, `menu`, `info`, `hours`, `contact` y `gallery`, aprobadas en D-154. Cualquier sección fuera de ella se rechaza con `INVALID_SECTION`. El orden lo define el array guardado en `sections`.

### 5.3 Página pública

1. `GET /public/{slug}` resuelve el tenant solo si está activo.
2. Si el sitio no está publicado, responde `404 SITE_NOT_PUBLISHED`.
3. Si está publicado, devuelve únicamente los campos de la sección 4.4.
4. `GET /public/{slug}/menu` devuelve solo productos publicados y disponibles de categorías activas, ordenados por `display_order` (BL-03).
5. La interfaz usa `/r/{slug}` y `/r/{slug}/menu` (D-124), sin subdominios.

### 5.4 Metadatos y vista previa

- `title` = `display_name`; `description` = `tagline` o `description` truncada; `canonical` = `/r/{slug}`.
- La vista previa lee `/tenant/public-site/preview` con sesión de `owner` y no depende de `is_published`.
- La página publicada no incluye enlaces a `/admin` ni al portal de Lixus.

## 6. Flujos

### 6.1 Editar la configuración

1. El CEO abre `/admin/configuracion` con sesión de `owner`.
2. Edita nombre, frase, descripción, colores, horarios, contacto, secciones y URLs de imágenes.
3. Guarda: el backend valida y conserva el estado de publicación actual.
4. La pantalla muestra confirmación y la vista previa refleja los cambios.

### 6.2 Publicar

1. El CEO revisa la vista previa.
2. Pulsa «Publicar»; el backend comprueba que haya nombre y secciones visibles.
3. La página queda disponible en `/r/{slug}`.
4. «Despublicar» vuelve a `404` sin borrar la configuración.

### 6.3 Ver la página

1. Un visitante abre `/r/{slug}`.
2. El frontend pide `/public/{slug}` y `/public/{slug}/menu`.
3. Si el sitio no está publicado, muestra «Página no disponible»; si no hay menú, muestra «Este restaurante aún no publica su menú».
4. La página respeta colores, logo, horarios y contacto del tenant.

### 6.4 Configurar el enlace de domicilio

1. El CEO pega el enlace externo que usa el restaurante para domicilio.
2. El backend valida el formato `https` y lo guarda en `tenant_settings`.
3. La página pública muestra el enlace como información, sin zonas, tarifas ni seguimiento; la entrega la resuelve el restaurante por fuera (D-155).

## 7. Archivos a crear o modificar

| Archivo | Acción | Contenido |
|---|---|---|
| `backend/app/sites/service.py` | Modificar | Edición completa sin publicar, publicación explícita, validación del enlace |
| `backend/app/sites/schemas.py` | Modificar | Cuerpos de edición, publicación y respuesta pública |
| `backend/app/sites/repository.py` | Modificar | Consulta de preview y enlace de domicilio |
| `backend/app/sites/router.py` | Modificar | `POST /publish`, `GET /preview` |
| `backend/app/public/router.py` | Modificar | Respuesta pública acotada y menú filtrado |
| `backend/app/menus/repository.py` | Modificar | Orden y filtros usados por el menú público (BL-03) |
| `backend/tests/` | Crear | Pruebas de publicación, slug, campos públicos y enlace de domicilio |
| `frontend/src/lib/site.ts` | Crear | Funciones de configuración y sitio público sobre `apiFetch` |
| `frontend/src/app/(ceo-portal)/admin/configuracion/page.tsx` | Modificar | Formulario y botón de publicación |
| `frontend/src/app/(ceo-portal)/admin/configuracion/preview/page.tsx` | Crear | Vista previa |
| `frontend/src/app/(public-site)/page.tsx` | Modificar | Inicio público con metadatos y estados |
| `frontend/src/app/(public-site)/menu/page.tsx` | Modificar | Menú público ordenado y filtrado |
| `frontend/src/middleware.ts` | Modificar | Rutas `/r/{slug}` (BL-01) |
| `docs/04-backend/api.md` | Modificar | Endpoints nuevos |
| `docs/04-backend/features/sitio-publico.md` | Modificar | Estado real y enlace a esta especificación |
| `docs/05-frontend/features/sitio-publico.md` | Modificar | Estado de pantallas y enlace a esta especificación |

No se modifica el contrato de autenticación ni se suben imágenes a almacenamiento externo.

## 8. Estados obligatorios por pantalla

| Pantalla | Cargando | Vacío | Error | Sin permiso |
|---|---|---|---|---|
| `/admin/configuracion` | Esqueleto del formulario | «Aún no hay configuración.» | Reintento | «Solo el dueño puede publicar» |
| Vista previa | «Preparando vista…» | «Agrega nombre y secciones para ver la página.» | Reintento | No aplica |
| `/r/{slug}` | Esqueleto de la página | «Página no disponible» | «No pudimos cargar la página» con reintento | No aplica |
| `/r/{slug}/menu` | Esqueleto de tarjetas | «Este restaurante aún no publica su menú.» | Reintento | No aplica |

La página pública funciona en móvil, con contraste suficiente y navegación por teclado (D-131).

## 9. Pruebas requeridas

1. Guardar la configuración no cambia `is_published`.
2. Publicar y despublicar funciona con rol `owner`; un `admin` recibe `403`.
3. Con el sitio despublicado, `GET /public/{slug}` devuelve `404`.
4. Un slug inexistente devuelve `404` sin revelar otros tenants.
5. La respuesta pública no contiene `tenant_id`, `schema_name` ni correos internos.
6. Todos los campos editables se guardan, incluidos logo, imagen principal, secciones y contacto.
7. Un color con formato inválido se rechaza con `INVALID_COLOR`.
8. Una URL `http` en imagen se rechaza en producción con `INVALID_URL`.
9. Una sección fuera de la plantilla se rechaza con `INVALID_SECTION`.
10. Un enlace de domicilio con esquema distinto de `https` se rechaza con `INVALID_URL`.
11. El menú público respeta publicación, disponibilidad y orden de BL-03.
12. La ruta pública funciona con `/r/{slug}`; no existen subdominios por tenant.
13. La página publicada no enlaza al panel privado ni al portal de Lixus.
14. La vista previa muestra los cambios sin publicar el sitio.

## 10. Criterios de aceptación

- [ ] La edición y la publicación son acciones separadas.
- [ ] Solo `owner` publica y despublica.
- [ ] `/r/{slug}` y `/r/{slug}/menu` sirven la página publicada.
- [ ] El menú público respeta lo publicado en BL-03.
- [ ] La respuesta pública contiene solo campos seguros.
- [ ] El slug inexistente o el sitio despublicado devuelven `404`.
- [ ] Los colores, URLs y secciones se validan en servidor.
- [ ] El enlace de domicilio configurado se guarda y se muestra en la página pública.
- [ ] La vista previa no depende de la publicación.
- [ ] La página pasa la revisión de móvil y teclado de D-131.

## 11. Dependencias

- BL-01: middleware de `/r/{slug}` y cliente HTTP.
- BL-03: productos publicados, disponibles y ordenados.
- BL-02: sesión y rol `owner` para publicar.
- D-108, D-109, D-124, D-146, D-154 y D-155 cerrados.
- PD-18 mantiene el dominio exacto **POR DEFINIR**; no se fija aquí.
- `03-arquitectura/integraciones.md`: R2 y `StorageProvider` para la subida real de imágenes.
- BL-04 registra el pedido de domicilio sin zonas ni tarifas (D-155).
- Deuda RT-14 en [`07-calidad/deuda-tecnica.md`](../07-calidad/deuda-tecnica.md).

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Guardar publique sin querer | `PUT` no toca `is_published`; solo `POST /publish` lo cambia |
| Página a medias | Publicar exige nombre y al menos una sección visible |
| Filtrar datos internos | Respuesta pública con campos explícitos, sin configuración de cobro |
| Menú desactualizado | BL-03 aplica publicación y orden; sin caché que retrase el cambio |
| Domicilio fuera de Lixus | Solo enlace informativo; sin zonas, tarifas ni seguimiento |
| Dominio sin decidir | Se mantiene `/r/{slug}`; PD-18 sigue abierto |
| Imagen con URL insegura | Solo `https` en producción; la subida real queda para R2 |
| Subdominios residuales | Middleware de BL-01 elimina la resolución por subdominio |

## 13. Definición de terminado

Se considera terminada cuando se cumplen los criterios de aceptación, pasan las pruebas del punto 9, CI pasa con lint, tests y build, y se verifica manualmente un ciclo completo: editar nombre, colores y horarios, comprobar que la página sigue sin publicarse, publicar, abrir `/r/{slug}` y `/r/{slug}/menu` con el menú de BL-03, despublicar y confirmar el `404`.
