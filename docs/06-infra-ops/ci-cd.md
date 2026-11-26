# CI/CD

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería
**Decisiones:** D-116

## 1. Pipeline

Archivo: `.github/workflows/ci.yml`.

| Job | Qué hace | Cuándo |
|---|---|---|
| `backend` | Instala dependencias, levanta PostgreSQL y Redis, migra, ejecuta Ruff y pytest | Push y PR |
| `frontend` | `npm ci`, lint y build | Push y PR |
| `docker` | Construye las imágenes | Push y PR |
| `deploy` | Ejecuta `ops/deploy.sh main` en el runner self-hosted | Push a `main` o manual |

## 2. Reglas de rama

- `develop`: integración. Pasa pruebas, no despliega.
- `main`: producción. Despliega solo si los tres jobs anteriores pasan.
- Un PR debe pasar CI antes de merge.
- No se hace push directo a `main` sin revisión.

## 3. Runner

- Self-hosted en la instancia de producción.
- Etiqueta `lixus`.
- No requiere puerto 22 abierto ni clave SSH.
- Ejecuta el script con `sudo`.

## 4. Secretos

- Los secretos de aplicación viven en `.env` del servidor.
- GitHub no necesita secretos de aplicación para el despliegue actual.
- Nunca se escribe un token en un documento o en el repositorio.
- Si un token se expone, se rota de inmediato.

## 5. Qué falta

- Pruebas de frontend.
- Cobertura mínima.
- `mypy`.
- Pruebas de idempotencia, rate limiting y permisos.
- Escaneo de dependencias.
- Staging antes de producción.

## 6. Criterio de pipeline sano

1. Falla si lint, test o build fallan.
2. No despliega si falta un job.
3. No deja el sitio caído si el build falla.
4. Registra el commit desplegado.
5. Permite rollback.
