# Estado del producto

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Producto + Ingeniería

Este documento describe lo que existe hoy en el repositorio y en producción. No describe intenciones. Si una feature no está aquí como `EN PRODUCCIÓN`, no se puede prometer al cliente.

## 1. Resumen

Lixus tiene un núcleo multitenant real y un despliegue productivo con HTTPS. El producto visible está en construcción: el frontend aún no consume la API y varios módulos del backend son parciales. La prioridad comercial no es añadir módulos, sino cerrar el flujo que permite a un restaurante operar y pagar.

## 2. Estado por área

| Área | Estado | Qué existe | Qué falta para considerarla terminada |
|---|---|---|---|
| Producción y HTTPS | EN PRODUCCIÓN | `https://lixus.coderhivex.com`, Nginx, TLS, RDS, Redis, Docker Compose | Alertas y backups verificados |
| Núcleo multitenant | EN PRODUCCIÓN | Schema `platform`, schema por tenant, aprovisionamiento, `search_path` por transacción, prueba de aislamiento | Rol de base de datos con privilegios mínimos y RLS opcional |
| Administración Lixus | PARCIAL | Crear, listar, ver y verificar tenants; planes; clave `X-Platform-Admin-Key` | JWT con rol Lixus, auditoría por usuario, UI conectada |
| Autenticación | PARCIAL | Login, logout, `/me`, cookie `httpOnly`, resolución de membresía | Registro, recuperación, verificación de correo, revocación, `Secure` en producción, CSRF |
| Menú | PARCIAL | Listar y crear categorías y productos | Editar, borrar, publicar/despublicar, ordenar, imágenes |
| Mesas y QR | PARCIAL | Listar y crear mesas con token | Sesión QR real, solicitudes persistidas, estados de mesa |
| Pedidos | PARCIAL | Crear, listar y ver pedidos | Líneas, snapshot de precio, total en servidor, cambio de estado, cocina |
| Reservas | PARCIAL | Crear y listar reservas | Disponibilidad, solapamientos, estados, no-show |
| Caja y comprobantes | NO INICIADO | Registro de pago y endpoints base | Confirmar pago, liberar mesa, comprobante, QR de descarga |
| Página pública | PARCIAL | Configuración y menú por slug | Publicar, branding editable, reservas y mesa conectadas |
| Personal | PARCIAL | Listar y pre-registrar perfiles | Usuario global, membresía, invitación, roles y revocación |
| Suscripciones | NO INICIADO | Modelos y catálogo de planes | Cobro, facturación, vencimiento y reactivación |
| IA | NO INICIADO | Decisiones y diseño | Proveedor, permisos, cuotas y medición |
| Frontend | PARCIAL | Rutas y pantallas de las tres caras | Llamadas a la API, guards, estados de carga y error, formularios reales |
| CI/CD | EN PRODUCCIÓN | Lint, tests, build, imágenes y despliegue desde `main` | Pruebas de frontend y cobertura mínima |
| Calidad | PARCIAL | Cuatro pruebas de backend | Pruebas de idempotencia, rate limiting, permisos, frontend y cobertura |
| Documentación | EN PRODUCCIÓN | Este árbol documental | Completar los `POR DEFINIR` con el dueño |

## 3. Lo que no se puede afirmar hoy

- No hay rate limiting implementado.
- La idempotencia solo cubre el alta de tenant; pedidos y pagos no la aplican.
- No hay CSRF ni revocación de sesión.
- No hay correo transaccional.
- No hay pasarela de pagos.
- No hay IA.
- El frontend no llama a la API.
- El comprobante y la sesión QR son stubs.

## 4. Implicación comercial

Se puede vender una implantación acompañada y un producto en evolución, pero no se puede prometer autoservicio, cobro automático ni pagos en línea. El primer cliente debe entrar con un alcance cerrado, onboarding asistido y una fecha de entrega por escrito.

## 5. Evidencia

- Backend: `backend/app/*`, migraciones en `backend/migrations/`.
- Frontend: `frontend/src/app/*`.
- Producción: `docker-compose.prod.yml`, `nginx/nginx.conf`, `ops/deploy.sh`, `.github/workflows/ci.yml`.
- Deuda detallada: `07-calidad/deuda-tecnica.md`.
