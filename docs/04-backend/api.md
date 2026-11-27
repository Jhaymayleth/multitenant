# API

**Estado:** Vigente
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Base

- Prefijo: `/api/v1`.
- Formato: JSON.
- Autenticación privada: cookie `lixus_session`.
- Autenticación de plataforma: cabecera `X-Platform-Admin-Key` (interina).
- Documentación interactiva: `/docs` y `/redoc`.

## 2. Convenciones

### Éxito

- `200` lectura o actualización.
- `201` creación.
- `204` borrado sin cuerpo.

### Error

Objetivo:

```json
{
  "error": {
    "code": "SLUG_ALREADY_EXISTS",
    "message": "Ya existe un restaurante con ese slug",
    "request_id": "..."
  }
}
```

Estado actual: algunas rutas devuelven `{"detail": "..."}`. La unificación es deuda P0.

### Idempotencia

- Cabecera `Idempotency-Key` en escrituras críticas.
- Misma clave + mismo cuerpo → misma respuesta.
- Misma clave + cuerpo distinto → `409`.
- TTL propuesto: 24 horas.

### Paginación

- `limit` y `offset`.
- `limit` con cota máxima.
- Respuesta con `items`, `total`, `limit`, `offset` cuando aplique.

### Fechas y dinero

- Fechas ISO 8601 con zona horaria.
- Dinero en enteros (`*_cents`).
- Moneda del tenant en su configuración.

### Búsqueda de menú

`GET /tenant/menu/products?q=` busca dentro del tenant resuelto en servidor. El proveedor es Elasticsearch sobre un índice por tenant (D-162); si no responde, el backend cae a full-text de PostgreSQL. El cliente no elige índice ni envía `tenant_id`.

## 3. Endpoints actuales

### Salud

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio |

### Autenticación

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/auth/login` | Inicia sesión y emite cookie |
| POST | `/auth/logout` | Borra la cookie |
| GET | `/auth/me` | Usuario y tenant activo |
| POST | `/auth/switch-tenant` | Cambio de tenant (stub) |

### Plataforma

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/platform/tenants` | Aprovisiona un tenant |
| GET | `/platform/tenants` | Lista tenants |
| GET | `/platform/tenants/{id}` | Detalle |
| POST | `/platform/tenants/{id}/verify` | Aprueba o cancela |
| GET | `/platform/plans` | Planes activos |

### Menú

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/menu/categories` | Lista categorías |
| POST | `/tenant/menu/categories` | Crea categoría |
| GET | `/tenant/menu/products` | Lista productos; acepta `q` para búsqueda (D-162) |
| POST | `/tenant/menu/products` | Crea producto |
| PUT | `/tenant/menu/products/{id}` | Edita producto |
| DELETE | `/tenant/menu/products/{id}` | Retira producto |
| PATCH | `/tenant/menu/products/{id}/publication` | Publica u oculta |
| PATCH | `/tenant/menu/products/{id}/order` | Reordena |
| PUT | `/tenant/menu/categories/{id}` | Edita categoría |
| DELETE | `/tenant/menu/categories/{id}` | Retira categoría |

### Mesas

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/tables` | Lista mesas |
| POST | `/tenant/tables` | Crea mesa |

### Pedidos

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/orders` | Lista pedidos |
| POST | `/tenant/orders` | Crea pedido |
| GET | `/tenant/orders/{id}` | Detalle |

### Reservas

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/reservations` | Lista reservas |
| POST | `/tenant/reservations` | Crea reserva |

### Pagos

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/tenant/orders/{id}/payment-link` | Genera cobro con pasarela del restaurante |
| GET | `/tenant/payments` | Historial de cobros del pedido |
| POST | `/webhooks/orders/{provider}` | Confirma cobro por webhook firmado (stub) |

### Sitio público

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/public-site` | Configuración |
| PUT | `/tenant/public-site` | Actualiza configuración |

### Personal

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/staff` | Lista personal |
| POST | `/tenant/staff` | Pre-registra empleado |

### Público

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/public/{slug}` | Sitio público |
| GET | `/public/{slug}/menu` | Menú publicado |
| GET | `/public/table/{token}` | Sesión QR (stub) |
| POST | `/public/table/{token}/requests` | Solicitud (stub) |
| GET | `/public/receipts/{token}` | Comprobante (stub) |

### Webhooks y auditoría

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/webhooks/subscriptions/{provider}` | Evento de suscripción (stub) |
| GET | `/audit` | Auditoría global |

## 4. Reglas de contrato

1. El cliente no envía `tenant_id` para elegir tenant.
2. El cliente no envía precios ni totales definitivos.
3. El servidor valida y normaliza todo.
4. Los errores no filtran detalles internos.
5. Todo cambio de contrato actualiza este documento y la ficha de feature.

## 5. Versionado

- `v1` mientras no haya clientes externos.
- Un cambio incompatible requiere `v2` o una migración coordinada.
- Los webhooks llevan versión de evento.
