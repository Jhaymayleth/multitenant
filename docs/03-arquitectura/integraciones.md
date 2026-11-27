# Integraciones

**Estado:** Borrador
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería
**Decisiones abiertas:** PD-23, PD-26

## 1. Principio

Toda integración externa se encapsula detrás de una interfaz del backend. El resto del sistema no conoce el proveedor concreto. Esto permite cambiar de proveedor sin reescribir la lógica de negocio.

## 2. Inventario

| Integración | Uso | Estado | Interfaz | Variables |
|---|---|---|---|---|
| Cloudflare R2 | Imágenes de menú y marca | Prevista | `StorageProvider` | `R2_*` |
| Correo transaccional | Invitaciones, códigos, avisos | No iniciada | `EmailProvider` | `EMAIL_*` |
| Pagos | Cobro de pedidos con pasarela del restaurante y suscripción con pasarela de Lixus | No iniciada | `RestaurantPaymentProvider` + `SubscriptionProvider` | `PAYMENT_*` |
| Google | Login de clientes registrados | Prevista | `OAuthProvider` | `GOOGLE_*` |
| IA | Descripciones y asistencia | Fuera de la versión inicial | `AIProvider` | `AI_*` |
| Monitoreo | Salud, errores y métricas | Parcial | Logs y healthchecks | `OBS_*` |
| Backups | Copia de PostgreSQL | Parcial | RDS / script | `BACKUP_*` |

## 3. Almacenamiento

- R2 compatible con S3.
- Bucket privado.
- Ruta por tenant: `tenant_<id>/...`.
- Validación de tipo y tamaño antes de subir.
- URL firmada para lectura.
- No se sirve un archivo sin verificar el tenant.

## 4. Correo

- Proveedor por definir (PD-23).
- Capa de abstracción para cambiar de proveedor.
- En local se usa Mailpit.
- Casos: verificación, recuperación, invitación de personal, comprobante, aviso de suscripción.
- No se envía correo sin plantilla y sin registro de envío.

## 5. Pagos

Hay dos flujos separados (D-140 y D-145):

- **Suscripción:** la paga el restaurante a Lixus con la pasarela de Lixus.
- **Pedidos:** los paga el comensal con la pasarela que configura cada restaurante; el dinero llega a la cuenta del restaurante, no a Lixus.

Lixus genera el cobro del pedido, recibe el webhook firmado, marca el pedido pagado, libera la mesa y emite un comprobante operativo. No almacena datos de tarjeta.

- Eventos: `payment.created`, `payment.confirmed`, `payment.failed`.
- Idempotencia por `event_id` y firma HMAC obligatoria.
- Proveedor de pedidos por tenant; proveedor de suscripción global.

## 6. Google

- Solo para clientes registrados en la versión inicial.
- No para empleados, salvo decisión contraria.
- La identidad de Google se vincula a una cuenta existente por correo verificado.
- Si el correo no coincide, se pide vinculación explícita.

## 7. IA

- Fuera de la versión inicial.
- Si se activa: proveedor con capa de abstracción, permisos del usuario, cuotas por tenant y registro de consumo.
- La IA nunca escribe directo en la base de datos; propone y el backend valida.
- Pruebas de inyección de prompt y aislamiento.

## 8. Monitoreo

- Healthcheck de API y frontend.
- Logs estructurados con `request_id`.
- Alertas por caída, error 5xx y backup fallido.
- Panel interno para el equipo Lixus.
- Sin datos personales en logs.

## 9. Reglas de integración

1. Timeout y reintento con backoff.
2. Idempotencia en eventos.
3. Registro de request y response sin secretos.
4. Degradación controlada si el proveedor falla.
5. Prueba de integración en entorno local o sandbox.
6. Documentar el contrato y la versión del proveedor.
