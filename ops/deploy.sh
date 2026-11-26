#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Lixus — despliegue de produccion
# Ejecutado por el runner self-hosted de GitHub Actions (via sudo) o a mano.
#
# Propiedades:
#   * Idempotente: si ya esta en el commit pedido, no hace nada.
#   * No derriba el sitio si el build falla (compose aborta antes de `up`).
#   * Rollback automatico si el health check falla tras desplegar.
#   * Un solo deploy a la vez (flock).
# -----------------------------------------------------------------------------
set -euo pipefail

BRANCH="${1:-main}"
APP_DIR="${APP_DIR:-/opt/lixus}"
APP_URL="${APP_URL:-https://lixus.coderhivex.com}"
COMPOSE_FILE="docker-compose.prod.yml"

log() { echo "[deploy $(date -u +%H:%M:%SZ)] $*"; }

# Un unico deploy simultaneo
exec 9>/var/lock/lixus-deploy.lock
flock -n 9 || { log "otro deploy en curso; salgo"; exit 0; }

cd "$APP_DIR"

PREV=$(git rev-parse HEAD)

git fetch --quiet --prune origin
TARGET=$(git rev-parse "origin/$BRANCH")

# Produccion sigue una sola rama: si el clon se quedo en otra, lo movemos
CURRENT=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT" != "$BRANCH" ]; then
  log "clon estaba en $CURRENT; lo dejo en $BRANCH"
  git checkout --quiet -B "$BRANCH" "$TARGET"
fi

if [ "$PREV" = "$TARGET" ]; then
  log "sin cambios ($PREV); nada que hacer"
  exit 0
fi

log "desplegando $PREV -> $TARGET"
git reset --hard "$TARGET"

docker compose -f "$COMPOSE_FILE" build
docker compose -f "$COMPOSE_FILE" up -d --remove-orphans

docker exec lixus-nginx nginx -t
docker exec lixus-nginx nginx -s reload

sleep 5
if curl -fsS --max-time 10 "$APP_URL/health" >/dev/null; then
  log "deploy OK: $(git log -1 --oneline)"
  exit 0
fi

log "health check fallo; rollback a $PREV"
git reset --hard "$PREV"
docker compose -f "$COMPOSE_FILE" build
docker compose -f "$COMPOSE_FILE" up -d --remove-orphans
docker exec lixus-nginx nginx -s reload
log "rollback completado"
exit 1
