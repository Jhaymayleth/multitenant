# Seguridad y control de acceso

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería
**Decisiones:** D-105, D-106, D-112, D-117

## 1. Principios

1. El frontend no es una frontera de seguridad.
2. El servidor decide identidad, tenant, rol y permiso.
3. Mínimo privilegio por rol y por operación.
4. El schema del tenant es el límite; las demás defensas son adicionales.
5. Todo lo privilegiado se audita.
6. Ningún secreto vive en el repositorio.

## 2. Activos y amenazas

| Activo | Amenaza | Control |
|---|---|---|
| Datos de un tenant | Acceso cruzado por ID, filtro olvidado o schema incorrecto | Contexto validado + `search_path` + pruebas negativas |
| Credenciales | Fuerza bruta, reutilización, filtración | Hash bcrypt, rate limiting, códigos de un solo uso |
| Sesión | Robo de cookie, XSS, CSRF | `httpOnly`, `Secure`, `SameSite`, CSRF token |
| Roles | Escalada de privilegios | Permisos en servidor y revalidación de membresía |
| Enlaces de comprobante | Enumeración | Token aleatorio con caducidad |
| Panel Lixus | Acceso no autorizado | Clave interina, JWT de rol Lixus como destino |
| Archivos | Contenido malicioso | Validación de tipo y tamaño, re-codificación, URL firmada |

## 3. Autenticación

### 3.1 Métodos

- Correo y contraseña para CEO, personal y clientes registrados.
- Google para clientes registrados (previsto; no para empleados en la versión inicial).
- Código de un solo uso para verificar correo y primer acceso de un empleado pre-registrado.
- Recuperación de contraseña por enlace de un solo uso.

### 3.2 Contraseñas

- Hash con bcrypt y salt.
- Longitud mínima por definir; propuesta: 10 caracteres para clientes y 12 para personal.
- No se almacena la contraseña en claro ni se envía por correo.
- Mensaje de login genérico para no filtrar si el correo existe.

### 3.3 Sesión

- JWT firmado con `JWT_SECRET`.
- Cookie `lixus_session`, `httpOnly`, `SameSite=Lax`, `Secure` en producción.
- Expiración por defecto: 60 minutos.
- Logout borra la cookie; la revocación real del token es deuda pendiente.
- Cambio de tenant debe emitir un token nuevo y validar la membresía.

### 3.4 CSRF

- Propuesta: doble envío con cookie `lixus_csrf` y cabecera `X-CSRF-Token`.
- Las rutas de solo lectura no lo exigen.
- Las rutas de escritura lo exigen.
- Estado actual: no implementado.

## 4. Autorización

Cadena de verificación:

1. ¿Hay sesión válida?
2. ¿El tenant existe y está activo?
3. ¿La membresía existe y está activa?
4. ¿El rol permite la operación?
5. ¿El recurso pertenece al tenant?

Si falla cualquier paso, se rechaza. No se corrige en el frontend.

### Roles del tenant

| Rol | Alcance |
|---|---|
| `owner` | Todo el restaurante, plan y personal |
| `admin` | Operación, menú y personal; no plan ni CEO |
| `waiter` | Mesas, pedidos y reservas |
| `cook` | Estados de preparación; sin datos personales |

No existe rol de cajero (D-145): Lixus no recibe dinero de los pedidos. La matriz definitiva está aprobada en D-146 y documentada en `04-backend/features/personal-permisos.md`.

### Rol Lixus

- Administra tenants, verificación y planes.
- No lee datos operativos del restaurante.
- No cambia contraseñas de clientes.
- No borra datos al desactivar.
- Toda acción queda auditada.

## 5. Sesión anónima de mesa

- El QR contiene un token opaco de mesa.
- La sesión se crea al escanear y se reanuda si sigue abierta.
- No requiere cuenta.
- Permite enviar solicitudes, no crear pedidos.
- Se cierra por pago confirmado por webhook o por cierre manual del mesero con motivo.
- Un QR antiguo no reabre una sesión cerrada.

## 6. Archivos

- Validar tipo y tamaño en el servidor.
- Aceptar solo imágenes raster.
- Re-codificar para eliminar metadatos.
- Guardar en R2 privado.
- Servir con URL firmada y caducidad.
- Antivirus: fuera de la versión inicial; documentado como mejora.

## 7. Webhooks

- Hay webhooks de pedidos (pasarela del restaurante) y de suscripción (pasarela de Lixus).
- Firmados con HMAC y secreto compartido.
- Validar firma, timestamp y `event_id` único.
- Rechazar eventos repetidos.
- No confiar en el cuerpo sin verificar.
- Estado actual: el endpoint existe, pero no valida firma.

## 8. Secretos

- Variables de entorno, nunca en git.
- `.env.example` solo con valores de ejemplo.
- El arranque de producción falla si falta un secreto obligatorio.
- Rotación de `JWT_SECRET` con periodo de gracia.
- MFA obligatorio para el panel Lixus en producción (propuesto).

## 9. Auditoría

Registrar:

- Alta, verificación y activación de tenants.
- Cambios de rol y desactivación de personal.
- Accesos de Lixus a metadatos.
- Cambios de plan.
- Acciones de IA que escriban datos.
- Incidentes de seguridad.

No registrar contraseñas, tokens ni datos sensibles innecesarios.

## 10. Pruebas de seguridad

1. Sin sesión → 401.
2. Token de A en recurso de B → 403.
3. Cambio de `tenant_id` en body → rechazo.
4. `schema_name` inválido → rechazo antes de SQL.
5. Webhook sin firma → rechazo.
6. Login repetido → rate limit.
7. Cookie sin `Secure` en producción → fallo de configuración.
8. CSRF ausente en escritura → rechazo.

## 11. Brechas actuales

- `Secure=False` en el código de login.
- Sin CSRF.
- Sin revocación de sesión.
- `/auth/me` devuelve un nombre genérico.
- `switch-tenant` no emite token.
- Webhook sin firma.
- Rate limiting ausente.
- Rol de base de datos con privilegios amplios.

Ver `07-calidad/deuda-tecnica.md`.
