# Alcance del producto

**Estado:** Vigente (D-121)
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Producto
**Decisión:** D-121

## 1. Principio de alcance

La versión que se vende debe resolver el día completo de un restaurante independiente de una sede: recibir, preparar, cobrar y mostrarse al público. Todo lo que no contribuya a ese ciclo queda fuera hasta que el primer cliente pague y renueve.

## 2. Qué incluye la versión que se vende

| Capacidad | Qué debe hacer | Estado actual |
|---|---|---|
| Onboarding | Alta gestionada, verificación del negocio, creación del tenant y acceso del CEO | PARCIAL |
| Identidad y sesión | Login, logout, sesión httpOnly, roles y recuperación de acceso | PARCIAL |
| Menú | Categorías y productos con precio, descripción, imagen, disponibilidad y publicación | PARCIAL |
| Personal | Crear empleados, asignar rol, activar y desactivar | PARCIAL |
| Mesas y QR | Mesas con zona y estado; QR por mesa; solicitudes del cliente | PARCIAL |
| Pedidos | Pedido de mesa por el mesero, líneas, notas, cocina y estados | PARCIAL |
| Reservas | Disponibilidad, reserva con cuenta, estados y no-show | PARCIAL |
| Cobro de pedidos | Botón de pago con pasarela del restaurante, comprobante y QR; sin cajero | NO INICIADO |
| Página pública | Marca, menú, horarios, contacto y publicación | PARCIAL |
| Panel del CEO | Resumen del día y acceso a las áreas anteriores | PARCIAL |
| Administración Lixus | Tenants, verificación, planes y estado del servicio | PARCIAL |

## 3. Qué queda fuera de la versión que se vende

- Caja, arqueo, manejo de efectivo y conciliación bancaria del restaurante.
- Facturación fiscal y contabilidad.
- POS con turnos, arqueo, inventario y devoluciones.
- Reparto con flota propia o seguimiento en mapa.
- Múltiples sucursales por tenant.
- Constructor visual libre y plantillas múltiples.
- Directorio o marketplace de restaurantes.
- App móvil nativa.
- IA generativa y automatizaciones.
- Multi-idioma y multi-moneda.
- Dominio personalizado por restaurante.

Estas capacidades pueden aparecer en el roadmap, pero no se prometen en la venta inicial.

## 4. Qué significa “listo para el primer cliente que paga”

Se considera listo cuando se cumplen todos estos puntos:

1. Un restaurante nuevo se crea, se verifica y su CEO inicia sesión sin tocar la base de datos.
2. El CEO carga su menú, sus mesas y su personal.
3. Un mesero registra un pedido con líneas y total correcto.
4. Cocina ve el pedido y cambia su estado.
5. El cobro se confirma por webhook, la mesa queda libre y el comprobante se descarga.
6. Un cliente consulta la página pública, ve el menú y reserva.
7. El restaurante no puede ver datos de otro restaurante.
8. El frontend consume la API y muestra errores comprensibles.
9. Hay backups y un procedimiento de restauración probado.
10. El cliente firma términos, política de privacidad y acuerdo de servicio.

## 5. Dependencias críticas

- Cerrar precios y contrato (PD-07, PD-17).
- Definir jurisdicción y tratamiento de datos (PD-14, PD-15).
- Elegir proveedor de correo (PD-23).
- Definir soporte y horarios (PD-12).
- Resolver la matriz de permisos (PD-22).

## 6. Regla de cambio de alcance

Toda capacidad nueva entra por `01-producto/backlog.md` y requiere una decisión en `00-gobierno/decisiones.md`. No se añade “porque es fácil” ni se promete en una venta sin fecha y dueño.
