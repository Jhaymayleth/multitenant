# Variables de entorno

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

> Este documento lista nombres y usos. Nunca contiene valores reales.

## 1. Cómo se cargan

- **Backend:** `pydantic-settings` lee `.env` y `../.env`.
- **Frontend:** Next.js lee `.env`; solo `NEXT_PUBLIC_*` llega al navegador y se fija en build.
- **Docker Compose:** interpola `${...}` desde el `.env` de la raíz.
- `.env` está ignorado por git; `.env.example` es la plantilla.

## 2. Backend

| Variable | Obligatoria en producción | Uso |
|---|---|---|
| `APP_ENV` | Sí | Entorno lógico |
| `APP_NAME` | No | Título de OpenAPI |
| `APP_VERSION` | No | Versión mostrada |
| `DEBUG` | No | Modo debug; debe ser `false` |
| `APP_HOST` | No | Host de escucha |
| `APP_PORT` | No | Puerto |
| `NEXT_PUBLIC_APP_URL` | Sí | CORS y enlaces |
| `API_BASE_URL` | Sí | URL pública del API |
| `DB_HOST` | Sí | Host PostgreSQL |
| `DB_PORT` | Sí | Puerto |
| `DB_USER` | Sí | Usuario |
| `DB_PASSWORD` | Sí | Contraseña |
| `DB_NAME` | Sí | Base de datos |
| `DB_POOL_MIN_SIZE` | No | Pool |
| `DB_POOL_MAX_SIZE` | No | Pool |
| `PGSSLMODE` | Sí en RDS | TLS hacia la base |
| `REDIS_URL` | Sí | Redis |
| `JWT_SECRET` | Sí | Firma de sesión |
| `JWT_ALGORITHM` | No | Algoritmo |
| `JWT_ACCESS_TOKEN_TTL_MINUTES` | No | Expiración |
| `PLATFORM_ADMIN_KEY` | Sí | Protección de `/platform/*` |
| `DEV_PASSWORD_HASH` | No | Solo desarrollo |
| `FILES_MAX_SIZE_MB` | No | Límite de archivos |
| `FILES_ALLOWED_IMAGE_TYPES` | No | MIME permitidos |
| `RATE_LIMIT_LOGIN_PER_MINUTE` | No | Configurada, sin implementar |
| `RATE_LIMIT_WRITES_PER_MINUTE` | No | Configurada, sin implementar |
| `PAYMENT_WEBHOOK_SECRET` | Sí si hay webhooks | Firma HMAC |
| `PAYMENT_WEBHOOK_ENDPOINT` | No | Endpoint del proveedor |

## 3. Frontend

| Variable | Obligatoria | Uso |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Sí en build | Base del cliente HTTP |
| `NEXT_PUBLIC_APP_URL` | Recomendada | Enlaces y redirecciones |

## 4. Docker Compose

| Variable | Uso |
|---|---|
| `DB_HOST_PORT` | Puerto de PostgreSQL en el host |
| `UVICORN_WORKERS` | Workers del backend |
| `NEXT_PUBLIC_API_URL` | Build arg del frontend |
| `NEXT_PUBLIC_APP_URL` | Build arg del frontend |

## 5. Variables declaradas sin uso

- `AI_DEFAULT_PROVIDER`.
- `AI_MAX_TOKENS_PER_TENANT_DAY`.
- `AI_MAX_PROMPT_TOKENS`.

Están en `.env.example` pero el backend las ignora. Se eliminan o se implementan cuando exista IA.

## 6. Reglas

1. Ningún secreto real en `.env.example`.
2. El arranque de producción falla si falta un secreto obligatorio.
3. `NEXT_PUBLIC_API_URL` se define antes del build.
4. No se cambia una variable de producción sin registrar el cambio.
5. Si un token o clave se expone, se rota de inmediato.

## 7. Nota de seguridad

El archivo antiguo `VARIABLES_ENTORNO.md` contenía un token de configuración de runner. Debe rotarse y no reutilizarse. Este documento no reproduce el valor.
