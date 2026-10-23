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

### Opción A: Con Docker Compose (Recomendado)

1. Clonar el repositorio y copiar las variables de entorno:
   ```bash
   cp .env.example .env
   ```

2. Levantar todos los servicios:
   ```bash
   docker compose up --build
   ```

3. Acceder a los servicios:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **API Backend**: [http://localhost:8000](http://localhost:8000)
   - **Documentación Swagger / OpenAPI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

### Opción B: Ejecución Local en Desarrollo

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

#### 3. Iniciar el Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
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

## 5. Verificación de Estado

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

