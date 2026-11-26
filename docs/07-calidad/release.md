# Release

**Estado:** Borrador
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Versionado

- `MAJOR.MINOR.PATCH`.
- `MAJOR`: cambio incompatible para el cliente.
- `MINOR`: funcionalidad nueva compatible.
- `PATCH`: corrección.

La versión visible se registra en el changelog y en el commit desplegado.

## 2. Ramas

- `develop`: integración.
- `main`: producción.
- `feat/*` y `fix/*`: trabajo corto.
- Un release se mergea a `main` cuando CI está verde.

## 3. Checklist previo

- [ ] Alcance congelado.
- [ ] Pruebas verdes.
- [ ] Migraciones probadas.
- [ ] Backup reciente.
- [ ] Variables revisadas.
- [ ] Documentación actualizada.
- [ ] Changelog escrito.
- [ ] Plan de rollback.
- [ ] Cliente avisado si hay cambio visible.

## 4. Despliegue

1. Merge a `main`.
2. CI ejecuta backend, frontend y docker.
3. El runner ejecuta `ops/deploy.sh main`.
4. Verificar `/health`, `/` y `/api/v1/platform/tenants`.
5. Revisar logs 5xx.
6. Confirmar con el cliente.

## 5. Post-release

- Revisar métricas y errores durante 24 horas.
- Registrar incidentes.
- Actualizar deuda si apareció.
- Comunicar el resultado al equipo.

## 6. Rollback

- Automático si falla el health check.
- Manual si el problema es funcional.
- No se revierte una migración sin backup y decisión.
- Se documenta el motivo y el commit.

## 7. Frecuencia

- Al inicio: releases pequeñas y frecuentes.
- No se acumulan semanas de cambios.
- Un release no mezcla una migración riesgosa con una feature nueva.
