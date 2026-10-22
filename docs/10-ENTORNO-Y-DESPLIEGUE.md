# 10 — Entorno, Docker y CI/CD

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Diseño de entorno local y pipeline; el despliegue productivo está pendiente
**Requisitos:** RAC-06, RAC-07
**Decisiones aplicadas:** D-043, D-059, D-060, D-064
**Última actualización:** 22 de octubre de 2026

---

## 1. Servicios del entorno local

| Servicio | Imagen | Puerto | Función |
|---|---|---|---|
| `db` | `postgres:16-alpine` | 5432 | Base de datos con schema global y schemas de tenant |
| `redis` | `redis:7-alpine` | 6379 | Rate limiting, revocación de sesiones y caché |
| `api` | build `backend/` | 8000 | FastAPI |
| `web` | build `frontend/` | 3000 | Next.js |
| `mailpit` | `axllent/mailpit` | 8025 | Captura de correos en desarrollo (opcional) |
| `minio` | `minio/minio` | 9000 | S3 compatible para desarrollo sin R2 (opcional) |

**Regla:** un solo comando debe levantar todo:

```bash
docker compose up --build
```

---

## 2. Estructura del repositorio

```
lixus/
├── frontend/                # Next.js + TypeScript
│   ├── src/app/
│   ├── src/features/
│   ├── src/lib/
│   └── package.json
├── backend/                 # FastAPI + Python
│   ├── app/
│   ├── migrations/
│   │   ├── platform/
│   │   └── tenant/
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── infra/
│   ├── docker/
│   │   ├── postgres/init/
│   │   └── nginx/
│   └── scripts/
│       ├── provision_local.sh
│       └── seed_demo.py
├── .github/workflows/ci.yml
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── docs/
```

---

## 3. `docker-compose.yml` (referencia)

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports: ["5432:5432"]
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./infra/docker/postgres/init:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes"]
    ports: ["6379:6379"]
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 10

  api:
    build: ./backend
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_healthy }
    ports: ["8000:8000"]
    volumes:
      - ./backend:/app
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

  web:
    build: ./frontend
    env_file: .env
    depends_on:
      api: { condition: service_started }
    ports: ["3000:3000"]
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: ["npm", "run", "dev"]

volumes:
  pgdata:
  redisdata:
```

Puntos deliberados:

- `depends_on` con `condition: service_healthy` evita que la API arranque antes de PostgreSQL.
- Volumen persistente para no perder datos entre reinicios.
- La API se recarga en caliente solo en desarrollo.
- `mailpit` y `minio` se añaden en un archivo `docker-compose.override.yml` para no cargar el entorno básico.

---

## 4. `.env.example`

Sin valores reales. El archivo `.env` va en `.gitignore`.

```env
# --- Aplicación ---
APP_ENV=development
APP_NAME=Lixus
API_BASE_URL=http://localhost:8000
PUBLIC_WEB_URL=http://localhost:3000
FRONTEND_ORIGIN=http://localhost:3000

# --- PostgreSQL ---
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/lixus
PLATFORM_SCHEMA=platform

# --- Sesión ---
JWT_SECRET=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_TTL_MINUTES=30
REFRESH_TOKEN_TTL_DAYS=7
COOKIE_DOMAIN=localhost
COOKIE_SECURE=false
CSRF_HEADER=X-CSRF-Token

# --- Redis ---
REDIS_URL=redis://redis:6379/0
RATE_LIMIT_ENABLED=true
RATE_LIMIT_LOGIN_BURST=5
RATE_LIMIT_LOGIN_WINDOW_SECONDS=900
RATE_LIMIT_WRITE_BURST=120
RATE_LIMIT_WRITE_RATE_PER_SECOND=2

# --- Idempotencia ---
IDEMPOTENCY_TTL_HOURS=24

# --- Pagos ---
PAYMENT_PROVIDER=sandbox
PAYMENT_WEBHOOK_SECRET=
PAYMENT_SANDBOX_ENABLED=true

# --- Almacenamiento (Cloudflare R2) ---
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET=lixus-media
R2_PUBLIC_BASE_URL=
MEDIA_MAX_MB=5

# --- IA ---
AI_PROVIDER=groq
GROQ_API_KEY=
AI_MODEL=openai/gpt-oss-20b
AI_MAX_OUTPUT_TOKENS=512
AI_DAILY_TENANT_BUDGET=

# --- Correo ---
SMTP_HOST=
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
MAIL_FROM=no-reply@lixus.local

# --- Lixus ---
PLATFORM_ADMIN_EMAIL=
PLATFORM_ADMIN_INITIAL_PASSWORD=
PLATFORM_MFA_REQUIRED=false
```

**Reglas:** ninguna credencial real en el repositorio, ni en `README`, ni en capturas; el `.env.example` solo documenta el nombre de cada variable.

---

## 5. Puesta en marcha

```bash
cp .env.example .env          # completar valores locales
docker compose up --build     # levantar todo
docker compose exec api alembic -c migrations/platform/alembic.ini upgrade head
docker compose exec api python -m app.scripts.seed   # planes y datos demo
```

Migraciones de tenant: se aplican automáticamente al aprovisionar; para tenants existentes existe un comando explícito:

```bash
docker compose exec api python -m app.scripts.migrate_all_tenants
```

Verificación rápida:

```bash
curl http://localhost:8000/health          # {"status":"ok"}
curl http://localhost:3000                 # landing
```

---

## 6. PostgreSQL local

- Extensiones: `pgcrypto`, `citext`, `btree_gist`.
- El script de inicialización crea los roles `lixus_migrator` y `lixus_app` con permisos mínimos.
- El schema `platform` se crea con la primera migración, no en el `init.sql` (para que el esquema esté versionado).
- Copia de seguridad local: `pg_dump` documentado en el README.

---

## 7. CI/CD

### 7.1 Etapas mínimas

```
push / pull_request
   │
   ├── api-lint        ruff + mypy
   ├── api-tests       pytest con PostgreSQL y Redis de servicio
   ├── web-lint        eslint
   ├── web-build       tsc + next build
   ├── docker-build    construir ambas imágenes
   └── isolation-tests pruebas de aislamiento (obligatorias)
```

El pipeline **falla** si lint, tipos, pruebas o build fallan. Publicar imágenes es opcional y solo en `main`.

### 7.2 `.github/workflows/ci.yml` (referencia)

```yaml
name: ci

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  api:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: lixus
          POSTGRES_PASSWORD: lixus
          POSTGRES_DB: lixus_test
        ports: ["5432:5432"]
        options: >-
          --health-cmd "pg_isready -U lixus"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10
      redis:
        image: redis:7
        ports: ["6379:6379"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy app
      - run: alembic -c migrations/platform/alembic.ini upgrade head
      - run: pytest --cov=app --cov-report=term-missing

  web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: frontend/package-lock.json
      - run: npm ci
        working-directory: frontend
      - run: npm run lint
        working-directory: frontend
      - run: npm run build
        working-directory: frontend

  docker:
    runs-on: ubuntu-latest
    needs: [api, web]
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t lixus-api ./backend
      - run: docker build -t lixus-web ./frontend
```

### 7.3 Pruebas obligatorias dentro del pipeline

- Aislamiento entre dos tenants.
- Autorización por rol.
- Idempotencia (conteo de registros).
- Rate limiting (429 + `Retry-After`).
- Migración aplicada a dos schemas.

---

## 8. Almacenamiento con Cloudflare R2

| Aspecto | Configuración |
|---|---|
| Acceso | API S3; credenciales solo en el backend |
| Bucket | Privado |
| Rutas | `tenants/{tenant_id}/menu/{uuid}.webp`, `tenants/{tenant_id}/branding/{uuid}.png` |
| Validación | Tipo real, tamaño y dimensiones antes de subir |
| Entrega | URL firmada de corta duración o proxy autenticado |
| Borrado | Al reemplazar o eliminar un recurso, se elimina el objeto |
| Límite | Cuota fija para todos los tenants en el MVP |

La cuota gratuita de R2 (10 GB-mes, 1 M operaciones clase A, 10 M clase B, sin egress) es una referencia sujeta a condiciones vigentes; no se usa como garantía en el README.

En local se puede usar MinIO con las mismas credenciales S3; el código no cambia, solo el endpoint.

---

## 9. Despliegue productivo (pendiente P-14)

Dirección aprobada: AWS, con posibilidad de VPS según costo. Antes de desplegar se requiere:

- [ ] Dominio y TLS.
- [ ] Gestión de secretos (no variables en texto plano del repositorio).
- [ ] Base de datos administrada o contenedor con respaldo automático.
- [ ] Copias de seguridad probadas y restauración documentada.
- [ ] Migraciones con estrategia de reversión.
- [ ] Healthchecks y reinicio automático.
- [ ] Logs centralizados y alertas.
- [ ] Límites de recursos y protección de red.
- [ ] `COOKIE_SECURE=true` y cookies de primera parte.
- [ ] MFA obligatorio para Lixus.
- [ ] Revisión de la política de datos y privacidad.

**No se considera "listo para producción"** solo porque funcione en local.

---

## 10. Scripts de operación

| Script | Función |
|---|---|
| `seed` | Planes, usuario Lixus y tenants demo |
| `migrate_all_tenants` | Aplica migraciones de tenant a todos los schemas |
| `purge_idempotency` | Elimina claves vencidas |
| `purge_expired_sessions` | Cierra sesiones QR vencidas |
| `check_isolation` | Ejecuta el set de pruebas de aislamiento contra un entorno |

Los scripts se ejecutan manualmente o desde un job programado; nunca otorgan permisos adicionales.

---

## 11. Checklist de entorno

- [ ] `docker compose up` funciona desde cero en una máquina limpia.
- [ ] `.env.example` lista todas las variables usadas por el código.
- [ ] `.env` no está versionado.
- [ ] Migraciones de plataforma y de tenant son reproducibles.
- [ ] CI falla ante lint, test o build incorrectos.
- [ ] Las pruebas de aislamiento corren en CI.
- [ ] Healthchecks de base de datos y Redis activos.
- [ ] El README explica el arranque y la resolución del tenant.

---

**Fin de `10-ENTORNO-Y-DESPLIEGUE.md`.**
