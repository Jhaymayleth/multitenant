# Feature: sitio público (frontend)

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/sitio-publico.md`

## 1. Objetivo

Que el restaurante tenga una página propia, con su marca y su menú, que pueda publicar sin ayuda técnica.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Inicio público | `/r/{slug}` | Hero, información y acceso al menú |
| Menú público | `/r/{slug}/menu` | Categorías y productos |
| Reservas | `/r/{slug}/reservas` | Disponibilidad |
| Configuración | `/admin/configuracion` | Marca, textos y publicación |
| Vista previa | `/admin/configuracion/preview` | Cómo se verá |

## 3. Personalización

- Logo.
- Colores principal y secundario.
- Nombre y frase.
- Descripción.
- Horarios.
- Contacto y redes.
- Imagen principal.
- Visibilidad de secciones.

## 4. Criterios de aceptación

- [ ] El CEO edita y ve el cambio.
- [ ] Publicar y despublicar funciona.
- [ ] El menú público solo muestra lo publicado.
- [ ] La página carga en móvil y tiene metadatos.
- [ ] No se mezcla contenido de otro tenant.
- [ ] La página no enlaza al panel privado.

## 5. Estado actual

El menú público es una maqueta. La configuración no permite publicar. No hay vista previa.
