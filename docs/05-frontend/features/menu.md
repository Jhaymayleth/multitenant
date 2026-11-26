# Feature: menú (frontend)

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/menu.md`

## 1. Objetivo

Que el restaurante mantenga su carta actualizada y decida qué se publica en la página.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Menú | `/admin/menu` | Categorías y productos |
| Producto | modal o `/admin/menu/{id}` | Crear y editar |
| Categoría | modal | Crear y editar |
| Imagen | modal | Subir y recortar |

## 3. Estructura

- Lista de categorías con orden.
- Productos dentro de cada categoría.
- Estado de publicación y disponibilidad visible.
- Acciones: editar, duplicar, ocultar, borrar.

## 4. Flujos

### Crear producto

1. Elegir categoría.
2. Nombre, descripción y precio.
3. Imagen opcional.
4. Disponible y publicado.
5. Guardar y ver en la página.

### Publicar

1. Revisar el menú.
2. Activar publicación del sitio.
3. Abrir la página pública.

## 5. Criterios de aceptación

- [ ] Crear, editar y borrar categorías.
- [ ] Crear, editar y borrar productos.
- [ ] El precio se muestra en la moneda del restaurante.
- [ ] Un precio inválido muestra error claro.
- [ ] El producto oculto no aparece en la página.
- [ ] La imagen se previsualiza antes de guardar.
- [ ] El menú se ve bien en móvil.

## 6. Estado actual

La página es informativa y no consume la API. No hay formularios ni CRUD.
