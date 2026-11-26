# Despliegue

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Arquitectura de producción

```text
Internet
  │ 80 / 443
  ▼
Nginx (contenedor, TLS Let's Encrypt)
  ├── /            → frontend Next.js (3000)
  └── /api, /health → backend FastAPI (8000)
                         ├── RDS PostgreSQL (TLS)
                         └── Redis (red interna)
```

## 2. Componentes

- **Servidor:** instancia AWS con Docker.
- **Repositorio:** clon en `/opt/lixus`.
- **Compose:** `docker-compose.prod.yml`.
- **Proxy:** `nginx/nginx.conf`.
- **TLS:** Certbot fuera del contenedor; certificados montados.
- **Runner:** self-hosted en la instancia, etiqueta `lixus`.

## 3. Despliegue normal

El pipeline de `main` ejecuta `ops/deploy.sh main` en el runner. El script:

1. Toma un lock para evitar despliegues simultáneos.
2. Hace `git fetch` y compara el commit.
3. Si no hay cambios, termina.
4. Hace `git reset --hard` al commit de `origin/main`.
5. Construye imágenes.
6. Levanta contenedores con `--remove-orphans`.
7. Valida Nginx y recarga.
8. Comprueba `/health`.
9. Si falla, vuelve al commit anterior y reconstruye.

## 4. Despliegue manual

```bash
cd /opt/lixus
sudo git pull
sudo docker compose -f docker-compose.prod.yml up -d --build --remove-orphans
sudo docker exec lixus-nginx nginx -t
sudo docker exec lixus-nginx nginx -s reload
curl -s -o /dev/null -w "%{http_code}\n" https://lixus.coderhivex.com/
```

## 5. Verificación posterior

- `/health` responde `ok`.
- `/` responde 200.
- HTTP redirige a HTTPS con 301.
- `/api/v1/platform/tenants` responde 403 sin clave.
- Los logs no muestran errores 5xx.
- El certificado sigue vigente.

## 6. Rollback

```bash
cd /opt/lixus
sudo git log --oneline -5
sudo git checkout <commit>
sudo docker compose -f docker-compose.prod.yml up -d --build
sudo docker exec lixus-nginx nginx -s reload
```

El script automático hace rollback si el health check falla. Un rollback de base de datos requiere backup y decisión; no es automático.

## 7. TLS

- Let's Encrypt con renovación automática.
- Certificado válido hasta 2027-02-22 (al 26 de noviembre de 2026).
- Respaldo en `/root/letsencrypt-2026-11-24.tar.gz`.
- Límite: 5 duplicados por semana.

## 8. Reglas

1. Solo `main` despliega.
2. No se despliega sin CI verde.
3. No se edita producción a mano sin registrar el cambio.
4. Todo cambio de infraestructura se prueba en local.
5. Un despliegue que falla se revierte antes de investigar.

## 9. Pendientes

- Staging.
- Migraciones de tenant coordinadas en el despliegue.
- Backups verificados antes de cada migración.
- Alertas de fallo de despliegue.
- Documentar la creación del schema `platform` en una RDS nueva.
