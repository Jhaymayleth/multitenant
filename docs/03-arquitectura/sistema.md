# Arquitectura del sistema

**Estado:** Vigente
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería
**Decisiones:** D-102, D-104, D-115, D-162

## 1. Vista general

Lixus es un monolito modular con dos aplicaciones desplegables y servicios de apoyo:

- **Frontend:** Next.js 15 con React 19 y TypeScript.
- **Backend:** FastAPI con Python 3.12, SQLAlchemy y Alembic.
- **Base de datos:** PostgreSQL 16, con schema `platform` y un schema por tenant. Es la única fuente de verdad.
- **Caché y límites:** Redis 7.
- **Búsqueda:** Elasticsearch como índice de solo lectura del menú, por tenant y reconstruible (D-162, pendiente de implementar).
- **Archivos:** Cloudflare R2 (previsto).
- **Borde:** Nginx con TLS.

```text
Navegador
   │ HTTPS
   ▼
Nginx (TLS, cabeceras, proxy)
   ├── /            → Next.js
   └── /api, /health → FastAPI
                         ├── PostgreSQL (RDS): platform + tenant_<id>
                         ├── Redis: rate limiting, sesión, caché
                         └── R2 / correo / pagos / IA (previstos)
```

El índice de Elasticsearch se alimenta desde PostgreSQL y no guarda la fuente de verdad. Redis transporta los eventos de reindexado.

## 2. Las tres caras

| Cara | Ruta | Usuario | Autenticación |
|---|---|---|---|
| Web pública | `/r/{slug}` (D-124) | Visitante y comensal | No |
| Panel del CEO | `/admin` | CEO y personal autorizado | Sí, cookie httpOnly |
| Portal Lixus | `/portal` y `/solicita` | Equipo Lixus y solicitante | Sí, clave o JWT de plataforma |

Las tres caras comparten backend y modelo de datos. La separación es de responsabilidad y de autorización, no de repositorio.

## 3. Flujo de una petición privada

1. El navegador envía la cookie `lixus_session`.
2. El backend valida el JWT y obtiene `sub`, `tenant_id` y `role`.
3. El backend vuelve a consultar el tenant y la membresía en la base de datos.
4. Si el tenant está activo y la membresía también, fija el `search_path` del schema del tenant.
5. La operación se ejecuta solo contra ese schema.
6. La respuesta se devuelve sin datos de otros tenants.

## 4. Flujo de una petición pública

1. La URL trae el slug del restaurante.
2. El backend busca el tenant activo por slug.
3. Fija el `search_path` de su schema.
4. Devuelve solo la configuración pública y el menú publicado.
5. Si el sitio no está publicado, responde 404.

## 5. Componentes y responsabilidades

| Componente | Responsabilidad | No debe hacer |
|---|---|---|
| Frontend | Presentar, navegar y enviar formularios | Decidir permisos o tenant |
| Backend | Validar, autorizar, calcular y persistir | Confiar en precios o roles del cliente |
| PostgreSQL | Guardar datos y aislar por schema | Decidir reglas de negocio |
| Redis | Límites, sesión, eventos y caché | Ser fuente de verdad |
| Elasticsearch | Buscar menú por tenant sobre una proyección | Guardar precios o ser la fuente de los productos |
| Nginx | TLS, proxy y cabeceras | Lógica de negocio |
| R2 | Archivos | Servir datos privados sin firma |

## 6. Despliegue actual

- Producción: `https://lixus.coderhivex.com`.
- Nginx en contenedor, TLS con Let's Encrypt.
- Frontend con `next start`, backend con Uvicorn y dos workers.
- Redis en red interna.
- PostgreSQL en RDS con TLS.
- CI/CD desde GitHub Actions; `main` despliega.

Detalle en `06-infra-ops/`.

## 7. Restricciones de diseño

1. Un solo backend es la fuente de autoridad.
2. El tenant se resuelve en el servidor.
3. No se comparten datos entre tenants.
4. El frontend no es una frontera de seguridad.
5. Las migraciones se versionan por cadena: plataforma y tenant.
6. Los secretos viven en variables de entorno, nunca en el repositorio.

## 8. Deuda arquitectónica conocida

- Rol de base de datos con privilegios mínimos y RLS opcional.
- Revocación de sesión y CSRF.
- Rate limiting y idempotencia completa.
- Observabilidad con `request_id` y métricas.
- Backups verificados.
- Proveedor de búsqueda con Elasticsearch aprobado pero no implementado (D-162).

Ver `07-calidad/deuda-tecnica.md`.
