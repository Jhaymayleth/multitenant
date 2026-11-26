# Dominios del backend

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Organización

El backend es un monolito modular. Cada dominio vive en `backend/app/<dominio>/` con `models`, `schemas`, `repository`, `service` y `router` cuando aplica.

| Dominio | Responsabilidad | Estado |
|---|---|---|
| `core` | Configuración, base de datos, dependencias, seguridad y errores | EN PRODUCCIÓN |
| `platform` | Tenants, planes, aprovisionamiento y verificación | PARCIAL |
| `auth` | Login, logout, sesión y cambio de tenant | PARCIAL |
| `menus` | Categorías y productos | PARCIAL |
| `tables` | Mesas, QR y sesiones | PARCIAL |
| `orders` | Pedidos, líneas y estados | PARCIAL |
| `reservations` | Reservas y disponibilidad | PARCIAL |
| `payments` | Pagos y comprobantes | NO INICIADO |
| `sites` | Configuración de la página pública | PARCIAL |
| `staff` | Perfiles y roles del personal | PARCIAL |
| `public` | Endpoints públicos del restaurante | PARCIAL |
| `webhooks` | Eventos firmados de proveedores | NO INICIADO |
| `audit` | Auditoría de acciones | NO INICIADO |
| `shared` | Paginación, utilidades y esquemas comunes | PARCIAL |
| `health` | Salud del servicio | EN PRODUCCIÓN |

## 2. Reglas de capa

- **Router:** valida entrada, resuelve dependencias y devuelve respuesta. No contiene reglas de negocio.
- **Service:** aplica reglas, calcula totales y coordina repositorios.
- **Repository:** consulta y persiste. No decide permisos.
- **Model:** representa la tabla. No contiene lógica de negocio.
- **Schema:** contrato de entrada y salida.

## 3. Dependencias transversales

- `get_db`: sesión de base de datos.
- `get_current_user`: valida el JWT.
- `get_tenant_context`: resuelve tenant y membresía, y fija `search_path`.
- `require_role`: autoriza por rol.
- `require_platform_admin`: protege el panel Lixus.
- `AppError`: error de negocio con código y estado.

## 4. Convenciones

- Rutas privadas del tenant: `/api/v1/tenant/...`.
- Rutas públicas: `/api/v1/public/...`.
- Rutas de plataforma: `/api/v1/platform/...`.
- Webhooks: `/api/v1/webhooks/...`.
- Auditoría: `/api/v1/audit`.

## 5. Deuda de organización

- Algunos servicios mezclan DDL, ORM y subprocess (aprovisionamiento).
- Hay modelos y esquemas sin uso.
- Faltan pruebas por dominio.
- El manejo de errores no es uniforme.

Ver `07-calidad/deuda-tecnica.md`.
