# Mapa de pantallas

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Web pública

| Ruta | Pantalla | Estado | Datos |
|---|---|---|---|
| `/r/{slug}` | Inicio del restaurante | NO INICIADO | Configuración pública |
| `/r/{slug}/menu` | Menú | PARCIAL | Productos publicados |
| `/r/{slug}/reservas` | Reserva | PARCIAL | Disponibilidad |
| `/r/{slug}/mesa/{token}` | Mesa y solicitudes | PARCIAL | Sesión QR |
| `/r/{slug}/comprobante/{token}` | Comprobante | NO INICIADO | Pago |

## 2. Panel del CEO

| Ruta | Pantalla | Estado | Datos |
|---|---|---|---|
| `/admin` | Resumen del día | PARCIAL | Pedidos, mesas, caja |
| `/admin/menu` | Menú y categorías | PARCIAL | CRUD |
| `/admin/mesas` | Mesas y QR | PARCIAL | Mesas y sesiones |
| `/admin/pedidos` | Pedidos y cocina | PARCIAL | Pedidos y estados |
| `/admin/caja` | Caja | PARCIAL | Pagos y comprobantes |
| `/admin/reservas` | Reservas | NO INICIADO | Reservas |
| `/admin/personal` | Personal y roles | NO INICIADO | Empleados |
| `/admin/configuracion` | Página pública | PARCIAL | Marca y publicación |
| `/admin/cuenta` | Plan y facturación | NO INICIADO | Suscripción |

## 3. Portal Lixus

| Ruta | Pantalla | Estado | Datos |
|---|---|---|---|
| `/solicita` | Solicitud de alta | PARCIAL | Formulario |
| `/portal` | Resumen de plataforma | PARCIAL | Contadores |
| `/portal/tenants` | Tenants | PARCIAL | Lista y detalle |
| `/portal/tenants/{id}` | Detalle y verificación | NO INICIADO | Tenant |
| `/portal/planes` | Planes | PARCIAL | Catálogo |
| `/portal/auditoria` | Auditoría | NO INICIADO | Eventos |

## 4. Autenticación

| Ruta | Pantalla | Estado |
|---|---|---|
| `/login` | Inicio de sesión | PARCIAL |
| `/recuperar` | Recuperación | NO INICIADO |
| `/verificar` | Código de verificación | NO INICIADO |

## 5. Reglas de navegación

- Sin sesión, `/admin` redirige a `/login`.
- Sin rol, la pantalla muestra “no autorizado”, no un error técnico.
- Un tenant inactivo muestra un mensaje claro y no permite operar.
- La web pública nunca muestra enlaces al panel privado.
- El portal Lixus no enlaza a datos operativos del restaurante.

## 6. Estados obligatorios por pantalla

1. Cargando.
2. Vacío con acción sugerida.
3. Error con reintento.
4. Sin permiso.
5. Éxito con confirmación.
