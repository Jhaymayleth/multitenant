# Variables de entorno — Lixus (multitenant)

**Fecha:** 2026-11-18
**Arquitectura:** FastAPI (`:8000`) + Next.js (`:3000`) + PostgreSQL (`:5433` host / `5432` contenedor) + Redis (`:6379`).

## Cómo se cargan

- **Backend:** `pydantic-settings` en `backend/app/core/config.py:14-18` lee `.env` y `../.env` (raíz del repo). Los nombres son *case-insensitive*: `DB_HOST` → `db_host`.
- **Frontend:** Next.js lee `.env` de `frontend/`. Solo las variables `NEXT_PUBLIC_*` llegan al navegador y se **inlinean en build**.
- **Docker Compose:** interpola `${...}` desde el `.env` de la raíz y además inyecta variables a los contenedores (`docker-compose.yml`).
- El repo versiona `.env.example`; `.env` está ignorado por git.

## Backend (`config.py`)

| Variable | ¿Obligatoria? | Por defecto | Ejemplo | Uso |
|---|---|---|---|---|
| `APP_ENV` | No | `local` | `local` / `production` | Entorno lógico. |
| `APP_NAME` | No | `Lixus API` | `Lixus API` | Título de OpenAPI. **No está en `.env.example`.** |
| `APP_VERSION` | No | `0.1.0` | `0.1.0` | Versión mostrada. **No está en `.env.example`.** |
| `DEBUG` | No | `false` | `true` local | Modo debug de FastAPI. **No está en `.env.example`.** |
| `APP_HOST` | No | `0.0.0.0` | `0.0.0.0` | Host de escucha. |
| `APP_PORT` | No | `8000` | `8000` | Puerto del API. |
| `NEXT_PUBLIC_APP_URL` | No | `http://localhost:3000` | `https://app.example.com` | Origen permitido en CORS y enlaces del frontend. **Obligatoria en producción.** |
| `API_BASE_URL` | No | `http://localhost:8000` | `https://api.example.com` | URL pública del backend. |
| `DB_HOST` | No | `localhost` | `postgres` en Docker | Host PostgreSQL. |
| `DB_PORT` | No | `5433` | `5432` dentro de Docker | Puerto que usa la app. **Ojo:** el host publica `DB_HOST_PORT` (`5433`), pero el backend en Compose usa `5432`. |
| `DB_USER` | No | `lixus` | `lixus` | Usuario. |
| `DB_PASSWORD` | No (Sí en producción) | `changeme_local` | secreto | Contraseña. |
| `DB_NAME` | No | `platform` | `platform` | BD que contiene el schema `platform`. |
| `DB_POOL_MIN_SIZE` | No | `5` | `5` | Pool SQLAlchemy. |
| `DB_POOL_MAX_SIZE` | No | `20` | `20` | Pool SQLAlchemy. |
| `REDIS_URL` | No | `redis://localhost:6379/0` | `redis://redis:6379/0` | Rate limit/caché (reservado). |
| `JWT_SECRET` | **Sí en producción** | `changeme_jwt_secret_do_not_use_in_prod` | cadena larga | Firma de JWT. **Cambiar obligatoriamente.** |
| `JWT_ALGORITHM` | No | `HS256` | `HS256` | Algoritmo. |
| `JWT_ACCESS_TOKEN_TTL_MINUTES` | No | `60` | `60` | Vida del access token. |
| `DEV_PASSWORD_HASH` | Solo desarrollo | `changeme_do_not_use_in_prod` | hash bcrypt | Fixtures locales. **Nunca en producción.** |
| `FILES_MAX_SIZE_MB` | No | `5` | `5` | Límite de subida. |
| `FILES_ALLOWED_IMAGE_TYPES` | No | `image/jpeg,image/png,image/webp` | igual | MIME permitidos. |
| `RATE_LIMIT_LOGIN_PER_MINUTE` | No | `6` | `6` | Configurada pero **sin implementación** (auditoría P0). |
| `RATE_LIMIT_WRITES_PER_MINUTE` | No | `30` | `30` | Configurada pero **sin implementación**. |
| `PAYMENT_WEBHOOK_SECRET` | **Sí** si se usan webhooks | `changeme_payment_webhook_secret` | secreto | Firma HMAC del proveedor simulado. |
| `PAYMENT_WEBHOOK_ENDPOINT` | No | `http://localhost:8000/webhooks/payments/sandbox` | URL | Endpoint del proveedor sandbox. |

### Solo para Docker Compose

| Variable | Uso |
|---|---|
| `DB_HOST_PORT` | Puerto publicado en el host para PostgreSQL (por defecto `5433`). No lo lee la app. |

## Frontend

| Variable | ¿Obligatoria? | Por defecto | Ejemplo | Uso |
|---|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | **Sí** (build) | `http://localhost:8000/api/v1` | `https://api.example.com/api/v1` | Base del cliente HTTP (`frontend/src/lib/api.ts:10`). Se inlinea en build. |
| `NEXT_PUBLIC_APP_URL` | Recomendada | — | `https://app.example.com` | Pasada por Compose; usada para enlaces/redirects. |

## Variables declaradas pero no usadas

- `AI_DEFAULT_PROVIDER`, `AI_MAX_TOKENS_PER_TENANT_DAY`, `AI_MAX_PROMPT_TOKENS`: están en `.env.example` pero `Settings` las ignora (`extra="ignore"`) y no hay módulo de IA. Eliminarlas o implementarlas.
- `NEXT_PUBLIC_APP_URL` existe en el backend (CORS) y en Compose; en el código del frontend no se referencia directamente.

## `.env` mínimo para local

```bash
APP_ENV=local
APP_HOST=0.0.0.0
APP_PORT=8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

DB_HOST=localhost
DB_HOST_PORT=5433
DB_PORT=5433
DB_USER=lixus
DB_PASSWORD=changeme_local
DB_NAME=platform

REDIS_URL=redis://localhost:6379/0
JWT_SECRET=cambia-esta-clave-por-una-larga-y-aleatoria
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_TTL_MINUTES=60
PAYMENT_WEBHOOK_SECRET=cambia-este-secreto
```

## Notas

- En Docker, `DB_HOST=postgres` y `DB_PORT=5432`; en local, `DB_HOST=localhost` y `DB_PORT=5433`.
- `NEXT_PUBLIC_API_URL` debe existir **antes de `next build`**; si se cambia después, el bundle sigue apuntando a la URL vieja.
- No pongas `JWT_SECRET`, `DB_PASSWORD`, `PAYMENT_WEBHOOK_SECRET` ni `DEV_PASSWORD_HASH` reales en `.env.example`.
- El frontend actual corre `npm run dev` dentro del contenedor (`frontend/Dockerfile`), por lo que lee `NEXT_PUBLIC_API_URL` en runtime; una build de producción requerirá pasarla como build arg.
