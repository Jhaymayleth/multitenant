# Changelog

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026

Registra cambios de producto, documentación e infraestructura. No sustituye al registro de decisiones.

## 2.0 — 2026-11-26

- Reorganización completa de `docs/` en ocho áreas.
- Registro de decisiones reiniciado en `D-101`.
- Se separan decisiones aprobadas, propuestas y pendientes.
- Se documenta el estado real del producto y la deuda técnica.
- Se crean las fichas de feature backend/frontend.
- Se crean los borradores legales.
- Se aprueba la identidad: misión, visión y promesa (D-129).
- Se aprueba «Lixus» como nombre comercial y el uso de dominio propio (D-130).
- Se aprueba el español como único idioma de la versión inicial (D-123).
- El material anterior pasa a `_legado/` como referencia histórica.

## 1.0 — 2026-11-24

- Producción operativa en `https://lixus.coderhivex.com`.
- Nginx como reverse proxy, TLS con Let's Encrypt y renovación automática.
- PostgreSQL en RDS con TLS.
- Redes `edge` e `internal` separadas.
- Frontend en modo producción con `next start`.
- Backend con dos workers y healthchecks.
- `/platform/*` protegido con `X-Platform-Admin-Key`.
- Pipeline de despliegue desde `main`.

## 0.2 — 2026-10-22

- Consolidación de requerimientos, arquitectura, modelo de datos, seguridad, robustez y entorno.
- Definición de canales de pedido, caja ligera, sesión QR y pago por webhook.
- Registro histórico de decisiones `D-001` a `D-076`.

## 0.1 — Octubre 2026

- Primer borrador de producto y arquitectura multitenant.
- Elección de nicho: restaurantes independientes.
- Definición inicial de actores y aislamiento por schema.

## Hitos técnicos

| Fecha | Hito |
|---|---|
| Octubre 2026 | Núcleo multitenant: cadenas Alembic, aprovisionamiento y login con tenant |
| Octubre 2026 | Pruebas de aislamiento entre dos tenants |
| Noviembre 2026 | Protección de plataforma y verificación de tenants |
| Noviembre 2026 | Despliegue productivo con HTTPS y CI/CD |
