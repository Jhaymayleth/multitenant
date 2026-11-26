# Accesibilidad

**Estado:** Aprobado (D-131)
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería
**Decisión:** D-131

## 1. Compromiso propuesto

WCAG 2.1 nivel AA en los flujos críticos:

- Login.
- Menú y pedido.
- Mesas y QR.
- Caja y comprobante.
- Reserva.
- Página pública.

## 2. Criterios mínimos

### Contraste

- Texto normal: 4.5:1.
- Texto grande: 3:1.
- No usar color como único indicador de estado.

### Teclado

- Todo control se alcanza con Tab.
- El foco es visible.
- No hay trampas de foco.
- Los diálogos se cierran con Escape.

### Formularios

- Cada campo tiene etiqueta asociada.
- El error se anuncia y se describe.
- El autocompletado usa atributos estándar.
- El tamaño táctil mínimo es 44 × 44 px.

### Contenido

- Encabezados jerárquicos.
- Texto alternativo en imágenes.
- Enlaces con texto descriptivo.
- Idioma declarado en el HTML.

### Movimiento

- Respetar `prefers-reduced-motion`.
- No usar animaciones que impidan leer.
- No hacer parpadear contenido.

## 3. Pruebas

1. Navegación completa con teclado.
2. Lector de pantalla en login y pedido.
3. Zoom al 200 % sin pérdida de contenido.
4. Contraste con herramienta automática.
5. Prueba en móvil real.

## 4. Estado

No hay auditoría de accesibilidad. Es deuda P2 hasta que existan pantallas conectadas.
