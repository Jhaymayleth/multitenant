# Feature: sitio público

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Decisiones:** D-108, D-109, D-154, D-155
**Documento frontend:** `05-frontend/features/sitio-publico.md`
**Especificación de la feature:** [`05-frontend/sitio-publico-api.md`](../../05-frontend/sitio-publico-api.md) (BL-06)

## 1. Objetivo

Dar a cada restaurante una página pública con su marca, menú, horarios y contacto, sin construir un sitio a medida.

## 2. Alcance

- Plantilla común con seis secciones aprobadas: hero, menú, información, horarios, contacto y galería (D-154).
- Enlace de domicilio configurable por el CEO; la entrega se resuelve fuera de Lixus (D-155).
- Personalización de logo, colores, textos, imagen principal y visibilidad de secciones.
- Publicar y despublicar.
- SEO básico y metadatos por restaurante.
- Menú publicado.

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-181 | Solo se muestra el contenido del tenant del slug. |
| RN-182 | Un sitio no publicado responde 404. |
| RN-183 | No se exponen datos internos ni de otros tenants. |
| RN-184 | El menú público solo muestra productos publicados y disponibles. |
| RN-185 | La URL es única por restaurante. |
| RN-186 | El contenido lo controla el CEO. |

## 4. API

| Método | Ruta | Estado |
|---|---|---|
| GET | `/public/{slug}` | Implementado |
| GET | `/public/{slug}/menu` | Implementado |
| GET | `/tenant/public-site` | Implementado |
| PUT | `/tenant/public-site` | Parcial |
| POST | `/tenant/public-site/publish` | No existe |

## 5. Datos

- `tenant.tenant_settings`: nombre, tagline, descripción, colores, logo, horarios, publicación.
- `tenant.menu_products`: menú público.

## 6. Criterios de aceptación

- [ ] El CEO publica y despublica su sitio.
- [ ] La página carga con la marca del restaurante.
- [ ] El menú muestra solo lo publicado.
- [ ] Un slug inexistente responde 404.
- [ ] El sitio no revela datos de otro tenant.
- [ ] La página funciona en móvil y tiene metadatos.

## 7. Brecha actual

`is_published` nace en `False` y el update no lo cambia. El sitio público siempre responde 404. No hay endpoints de publicación ni subida de logo.
