# Lixus — Plataforma SaaS Multitenant para Restaurantes

Lixus es un sistema SaaS multitenant diseñado para la gestión integral y presencia digital de restaurantes.

---

## 1. Arquitectura del Proyecto

El sistema se estructura como un **monolito modular** compuesto por un backend multitenant autoritativo y un frontend organizado en tres áreas claramente delimitadas:

```
┌────────────────────────────────────────────────────────────────────────┐
│                         Navegador del Usuario                          │
│   Web Pública · Panel del CEO (/admin) · Captación y Portal de Lixus   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS + Cookies HttpOnly
┌───────────────────────────────────▼────────────────────────────────────┐
│                    Next.js + TypeScript (frontend)                     │
│   SSG/ISR para sitios públicos · CSR para paneles administrativos      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ REST / JSON (sesión protegida)
┌───────────────────────────────────▼────────────────────────────────────┐
│                       FastAPI + Python (backend)                       │
│  Resolución de Tenant · Autorización · Idempotencia · Rate Limiting    │
└───────────┬───────────────────────┬──────────────────────┬─────────────┘
            │                       │                      │
    ┌───────▼────────┐      ┌───────▼────────┐     ┌───────▼─────────────┐
    │  PostgreSQL 16 │      │     Redis 7    │     │    Cloudflare R2    │
    │  platform      │      │  rate limit    │     │   archivos/fotos    │
    │  tenant_<id>   │      │  caché/tokens  │     │   bucket privado    │
    └────────────────┘      └────────────────┘     └─────────────────────┘
```

### Aislamiento Multitenant (Schema por Tenant)
- **Schema `platform`**: Datos globales del SaaS (usuarios globales, catálogo de tenants, membresías, planes, suscripciones, verificaciones, claves de idempotencia globales y auditoría).
- **Schemas `tenant_<id>`**: Cada restaurante dispone de un schema aislado generado en el servidor (`tenant_[a-f0-9]{12}`).
- **Sin columna `tenant_id` en tablas del tenant**: El schema es el límite estricto de aislamiento.
- **Resolución autoritativa en el servidor**: Cada transacción ejecuta `SELECT set_config('search_path', :sp, true)` (`SET LOCAL`), aislando las consultas sin contaminar el pool de conexiones.
- **Puerto local (host)**: PostgreSQL expone el puerto `5433` hacia el host (configurable vía `DB_HOST_PORT` en `.env`) para evitar conflictos con servicios PostgreSQL existentes en el puerto por defecto `5432`. Internamente en la red Docker se conecta en el puerto estándar `5432`.

---

## 2. Las Tres Caras del Frontend

Basado en las decisiones arquitectónicas D-001, D-074, D-075 y D-076:

1. **Web Pública del Restaurante (`(public-site)`)**:
   - Resuelto por subdominio propio (`restaurante1.dominio.com`).
   - Plantilla común con personalización del tenant (logo, colores, horarios, menú publicado y reservas).
   - Acceso anónimo a mesas mediante códigos QR (`/mesa/[token]`).
2. **Panel Privado del CEO del Restaurante (`(ceo-portal)`)**:
   - Ruta privada dentro del mismo subdominio (`/admin`).
   - Exclusivo para el CEO del restaurante; acceso protegido por cookie `HttpOnly` y membresía activa (`owner`).
   - Gestión de catálogo, mesas, monitoreo de pedidos, cola de cocina, caja ligera y configuración visual.
3. **Portal y Solicitud de Lixus (`(lixus)`)**:
   - Sitio independiente de captación (`/solicita` o `solicita.dominio.com`) para registro de solicitudes.
   - Portal administrativo global (`/portal`) para que Lixus gestione el ciclo de vida de tenants, aprobación, planes y facturación.

---

## 3. Estructura del Repositorio

```
multitenant/
├── backend/                         # Backend en FastAPI (Python 3.12)
│   ├── app/
│   │   ├── core/                    # Configuración, Base de Datos, Dependencias, Seguridad y Errores
│   │   ├── platform/                # Dominio de plataforma global y aprovisionamiento SaaS
│   │   ├── auth/                    # Autenticación, JWT, cookies HttpOnly y sesión
│   │   ├── menus/                   # Catálogo de productos y categorías del menú
│   │   ├── tables/                  # Mesas, sesiones QR y solicitudes de servicio
│   │   ├── orders/                  # Pedidos, máquina de estados y cola de cocina
│   │   ├── reservations/            # Reservas y control de disponibilidad
│   │   ├── payments/                # Caja ligera, pagos, comprobantes con QR y sandbox
│   │   ├── sites/                   # Configuración del sitio público (branding, horarios)
│   │   ├── staff/                   # Perfiles de empleados y roles del tenant
│   │   ├── public/                  # Endpoints públicos consumidos por visitantes y QR
│   │   ├── webhooks/                # Eventos y webhooks firmados de pagos
│   │   ├── audit/                   # Registro de auditoría
│   │   ├── shared/                  # Paginación, utilidades y esquemas compartidos
│   │   ├── api/                     # Agregador del router central (/api/v1)
│   │   └── main.py                  # Entrypoint de FastAPI
│   ├── migrations/
│   │   ├── platform/                # Cadena de migraciones Alembic para schema platform
│   │   └── tenant/                  # Cadena de migraciones Alembic para schemas tenant_<id>
│   ├── tests/                       # Pruebas unitarias, de integración y de aislamiento
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                        # Frontend en Next.js 15 (React 19 + TypeScript)
│   ├── src/
│   │   ├── app/
│   │   │   ├── (public-site)/       # Cara 1: Web pública (/menu, /reservas, /mesa/[token])
│   │   │   ├── (ceo-portal)/admin/  # Cara 2: Panel privado del CEO
│   │   │   ├── (lixus)/             # Cara 3: /solicita (onboarding) y /portal (administración SaaS)
│   │   │   ├── (auth)/login/        # Login de usuario
│   │   │   ├── layout.tsx           # Layout raíz
│   │   │   └── page.tsx             # Enrutador visual del proyecto
│   │   ├── lib/                     # Cliente API, constantes y tipos TypeScript
│   │   └── middleware.ts            # Resolución de subdominios y contexto del tenant
│   ├── Dockerfile
│   └── package.json
├── infra/
│   └── docker/
│       └── postgres/init/01-init.sql # Extensiones (pgcrypto, citext, btree_gist) y roles
├── docs/                            # Documentación integral de arquitectura y decisiones
├── docker-compose.yml               # Orquestación de servicios (Postgres, Redis, API, Web)
├── .env.example                     # Plantilla de variables de entorno
└── .github/workflows/ci.yml         # Pipeline de Integración Continua (Lint & Build)
```

---

## 4. Cómo Levantar el Proyecto

> **Regla de oro:** el puerto `8000` solo puede ser usado por **un** backend a la vez. Elige **una** de las dos opciones (Docker **o** ejecución local) y no mezcles ambas para el mismo puerto. Si ya levantaste el proyecto antes, primero verifica si sigue corriendo (ver §4.0) en vez de volver a ejecutar `uvicorn`.

### 4.0 Verificar si el proyecto ya está corriendo

Antes de levantar nada, comprueba el estado actual:

```bash
# Salud de la API
curl -s http://localhost:8000/health || echo "API no responde en :8000"

# Estado de los contenedores
docker compose ps

# Qué proceso ocupa el puerto 8000 (host)
ss -ltnp 'sport = :8000' || lsof -i :8000
```

Si la API responde `{"status":"ok",...}` y `docker compose ps` muestra los contenedores `Up`, **el proyecto ya está levantado**: no necesitas volver a ejecutar `uvicorn`; los cambios en el código se recargan solos (`--reload`). Salta a §4.3 para saber cómo reiniciar o detener.

### Opción A: Con Docker Compose (Recomendado)

1. Clonar el repositorio y copiar las variables de entorno:
   ```bash
   cp .env.example .env
   ```

2. Levantar todos los servicios:
   ```bash
   docker compose up --build
   ```

   > En segundo plano (libera la terminal):
   > ```bash
   > docker compose up --build -d
   > ```

3. Acceder a los servicios:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **API Backend**: [http://localhost:8000](http://localhost:8000)
   - **Documentación Swagger / OpenAPI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

### Opción B: Ejecución Local en Desarrollo

Usa esta opción solo si **no** tienes el contenedor `lixus-backend` corriendo en el puerto `8000`.

#### 1. Iniciar Base de Datos y Redis
```bash
docker compose up postgres redis -d
```

#### 2. Iniciar el Backend (FastAPI)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

> El backend lee `.env` automáticamente (ver `app/core/config.py`). Si corres en local, deja `DB_HOST=localhost` y `DB_PORT=5433` en `.env`.

#### 3. Iniciar el Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

---

### 4.3 Si el proyecto ya está levantado (reutilizar, reiniciar o detener)

El backend de FastAPI se arranca con `--reload`, por lo que **no hace falta reiniciarlo** cuando editas código: guarda el archivo y uvicorn recarga solo. Solo necesitas intervenir en estos casos:

| Necesitas… | Comando |
|---|---|
| Ver logs del backend | `docker compose logs -f backend` (Docker) o la terminal donde corre uvicorn (local) |
| Reiniciar solo el backend | `docker compose restart backend` (Docker) o `Ctrl+C` y volver a ejecutar `uvicorn ...` (local) |
| Detener todo (Docker) | `docker compose down` |
| Detener solo el backend (Docker) | `docker compose stop backend` |
| Detener uvicorn local | `Ctrl+C` en su terminal, o `fuser -k 8000/tcp` |
| Volver a levantar desde cero | `docker compose down && docker compose up --build` |

> **No ejecutes `uvicorn` si `docker compose ps` muestra `lixus-backend` en estado `Up`**: ambos intentarían ocupar el puerto `8000` y obtendrás `Address already in use`.

### 4.4 Error: `Address already in use` (errno 98)

**Qué significa:** el puerto `8000` (o el que indicaste con `--port`) ya está en uso por otro proceso. En este proyecto casi siempre es porque:
- ya levantaste el backend con Docker Compose (contenedor `lixus-backend`), o
- quedó un proceso `uvicorn` anterior sin cerrar, o
- otra aplicación usa el puerto `8000`.

**Cómo resolverlo (elige una):**

1. **Reutilizar el que ya corre** (recomendado si solo quieres desarrollar):
   ```bash
   curl http://localhost:8000/health
   # Si responde ok, no hagas nada: el backend ya está listo.
   ```

2. **Detener el contenedor Docker que ocupa el puerto** y luego levantar en local:
   ```bash
   docker compose stop backend        # o: docker compose down
   # ahora sí puedes correr uvicorn en local
   cd backend && source .venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Matar el proceso local que ocupa el puerto** y volver a arrancar:
   ```bash
   # Ver qué proceso usa :8000
   lsof -i :8000
   # o: ss -ltnp 'sport = :8000'
   # Terminarlo (sustituye <PID> por el número mostrado)
   kill <PID>
   # Alternativa rápida (mata todo lo que escuche en :8000):
   fuser -k 8000/tcp
   ```

4. **Usar otro puerto** (útil para tener Docker y local a la vez, p. ej. depurar):
   ```bash
   cd backend && source .venv/bin/activate
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```
   > Si cambias el puerto del backend, actualiza `NEXT_PUBLIC_API_URL`/`API_BASE_URL` en `.env` y reinicia el frontend para que apunte al nuevo puerto.

**Comprobación final:** en todos los casos, `curl http://localhost:8000/health` (o el puerto elegido) debe devolver `{"status":"ok","app":"Lixus API",...}`.

### 4.5 Comandos de gestión frecuentes

```bash
# Estado de servicios
docker compose ps

# Logs en tiempo real
docker compose logs -f backend
docker compose logs -f frontend

# Reiniciar un servicio
docker compose restart backend

# Detener todo conservando datos (volúmenes)
docker compose down

# Detener todo y borrar datos (¡cuidado!)
docker compose down -v

# Reconstruir imágenes tras cambiar dependencias
docker compose up --build -d

# Ejecutar migraciones de plataforma dentro del contenedor
docker compose exec backend alembic -c migrations/platform/alembic.ini upgrade head

# Ejecutar tests dentro del contenedor
docker compose exec backend pytest
```

---

## 5. Cumplimiento del enunciado

Estado actual (Fase 1 en curso). Cada punto se demostrará con código y pruebas al cerrar su fase.

| # | Punto del enunciado | Estado | Dónde |
|---|---|---|---|
| 1 | Qué es y por qué este nicho | ✅ Documentado | `docs/00-INDICE.md`, `docs/01-REQUERIMIENTOS.md` |
| 2 | Arquitectura multitenant (schema `platform` + `tenant_<id>`) | 🟡 En implementación | `backend/app/core/database.py`, `docs/03-ARQUITECTURA.md`, `docs/07-MODELO-DATOS.md` |
| 3 | Cómo levantar el proyecto (Docker + variables + URLs) | ✅ Implementado | Sección 4 de este README, `docker-compose.yml`, `.env.example` |
| 4 | Resolución del tenant por petición (JWT httpOnly, membresía, `SET LOCAL search_path`) | 🟡 En implementación | `backend/app/core/dependencies.py`, `backend/app/core/security.py` |
| 5 | Idempotencia y rate limiting (clave, tabla, TTL, 429 + `Retry-After`) | 🔴 Pendiente (Fase 4) | `docs/09-ROBUSTEZ.md` |
| 6 | Estrategias de renderizado (SSG/ISR público, CSR panel) | 🟡 En implementación | `frontend/src/app`, `frontend/src/middleware.ts` |
| 7 | Pruebas y CI | 🟡 En implementación | `backend/tests/`, `.github/workflows/ci.yml` |

Leyenda: ✅ implementado · 🟡 en implementación · 🔴 pendiente.

---

## 6. Verificación de Estado

Puedes verificar que la API esté respondiendo ejecutando:
```bash
curl http://localhost:8000/health
```
Respuesta esperada:
```json
{
  "status": "ok",
  "app": "Lixus API",
  "version": "0.1.0",
  "environment": "local"
}
```

