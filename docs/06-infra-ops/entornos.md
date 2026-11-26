# Entornos

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Entornos

| Entorno | Uso | Dominio | Base de datos |
|---|---|---|---|
| Local | Desarrollo y pruebas | `localhost:3000` / `localhost:8000` | PostgreSQL en Docker (`5433` host) |
| Producción | Clientes reales | `https://lixus.coderhivex.com` | PostgreSQL en RDS |

No hay entorno de staging dedicado. Es una brecha para operar con clientes: los cambios se prueban en local y en CI antes de `main`.

## 2. Servicios locales

| Servicio | Imagen | Puerto | Función |
|---|---|---|---|
| `db` | `postgres:16-alpine` | 5433 host / 5432 interno | Base de datos |
| `redis` | `redis:7-alpine` | 6379 | Caché y límites |
| `api` | build `backend/` | 8000 | FastAPI |
| `web` | build `frontend/` | 3000 | Next.js |
| `mailpit` | `axllent/mailpit` | 8025 | Correo local (opcional) |

## 3. Producción

| Servicio | Imagen | Red | Puerto |
|---|---|---|---|
| `nginx` | `nginx:1.27-alpine` | `edge` | 80 y 443 |
| `frontend` | build `Dockerfile.prod` | `edge` | 3000 interno |
| `backend` | build `backend/Dockerfile` | `edge` + `internal` | 8000 interno |
| `redis` | `redis:7-alpine` | `internal` | 6379 interno |

- Solo Nginx publica puertos.
- Redis no es accesible desde internet.
- RDS exige TLS (`PGSSLMODE=require`).
- Los secretos vienen de `.env` en el servidor, nunca de git.

## 4. Diferencias que importan

| Tema | Local | Producción |
|---|---|---|
| Cookie `Secure` | Puede ser falsa | Debe ser verdadera |
| CORS | `localhost` | Dominio real |
| Frontend | `next dev` | `next start` |
| Backend | `--reload` | Uvicorn con workers |
| Base de datos | Contenedor | RDS con TLS |
| Correo | Mailpit | Proveedor real (pendiente) |
| Backups | Volumen local | RDS + política |

## 5. Reglas

1. Producción no se prueba con datos de clientes.
2. Un cambio de infraestructura se documenta aquí y en `despliegue.md`.
3. No se comparte el `.env` por chat ni por correo.
4. Staging es una necesidad antes de escalar; queda en deuda P1.
