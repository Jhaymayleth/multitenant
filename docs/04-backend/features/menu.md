# Feature: menú

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Documento frontend:** `05-frontend/features/menu.md`
**Especificación de la feature:** [`05-frontend/menu-api.md`](../../05-frontend/menu-api.md) (BL-03)

## 1. Objetivo

Permitir que el restaurante mantenga un catálogo actualizado y lo publique en su página sin depender de una carta impresa.

## 2. Alcance

- Categorías: crear, listar, editar, borrar.
- Productos: crear, listar, editar, borrar.
- Precio, descripción, imagen, disponibilidad y publicación.
- Orden dentro de la categoría.
- Menú público solo con productos publicados y disponibles.

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-131 | El precio es mayor que cero. |
| RN-132 | El producto pertenece a una categoría del mismo tenant. |
| RN-133 | El nombre es obligatorio y no se duplica en la misma categoría. |
| RN-134 | El menú público no muestra productos no publicados. |
| RN-135 | El borrado es lógico y no rompe pedidos históricos. |
| RN-136 | La imagen se valida por tipo y tamaño. |

## 4. API

| Método | Ruta | Estado |
|---|---|---|
| GET | `/tenant/menu/categories` | Implementado |
| POST | `/tenant/menu/categories` | Implementado |
| PUT | `/tenant/menu/categories/{id}` | No existe |
| DELETE | `/tenant/menu/categories/{id}` | No existe |
| GET | `/tenant/menu/products` | Implementado |
| POST | `/tenant/menu/products` | Implementado |
| PUT | `/tenant/menu/products/{id}` | No existe |
| DELETE | `/tenant/menu/products/{id}` | No existe |
| POST | `/tenant/menu/products/{id}/image` | No existe |

## 5. Datos

- `tenant.menu_categories`: nombre, orden, estado.
- `tenant.menu_products`: categoría, nombre, descripción, precio, imagen, disponibilidad, publicación.

## 6. Criterios de aceptación

- [ ] Crear, editar y borrar una categoría.
- [ ] Crear, editar y borrar un producto.
- [ ] Un producto con precio 0 se rechaza.
- [ ] Un producto de otro tenant no se puede editar.
- [ ] El menú público solo muestra lo publicado y disponible.
- [ ] El orden se respeta en la página pública.
- [ ] La imagen se sube y se sirve con URL firmada.

## 7. Dependencias

- R2 para imágenes.
- Página pública para publicación.
- Pedidos para el snapshot de precio.

## 8. Brecha actual

Solo existen listar y crear. No hay edición, borrado, publicación ni imágenes.
