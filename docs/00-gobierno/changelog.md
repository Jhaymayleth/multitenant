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
- Se aprueba la ruta pública `/r/{slug}` (D-124).
- Se aprueban el tono directo y cercano (D-132), los límites del producto (D-133) y la prueba de cumplimiento de la promesa (D-134).
- Se aprueba Colombia como país de arranque (D-135); la ciudad piloto queda en PD-02.
- Se aprueba Barranquilla como ciudad piloto (D-136).
- Se aprueba el cliente ideal: una sede, 5–30 mesas y 3–20 empleados (D-137).
- Se aprueba la competencia principal: papel/Excel/WhatsApp y POS local (D-138).
- Se aprueba la estructura de tres planes; precios y moneda siguen en PD-07 (D-139).
- Se aprueba cobrar por pasarela de suscripción; proveedor y factura siguen en PD-08 (D-140).
- Se aprueba eliminar la prueba gratuita; cancelación y reembolso siguen en PD-09 (D-141).
- Se aprueba cancelar al final del periodo pagado sin reembolso proporcional (D-142).
- Se aprueba no descontar y cobrar implementación solo con migración (D-143).
- Se aprueba el marco de métricas sin metas numéricas hasta tener datos (D-144).
- Se aprueba el alcance de la versión vendible (D-121).
- Se aprueba el modelo de cobro: sin cajero, pasarela del restaurante para pedidos y pasarela separada para la suscripción (D-145).
- Se aprueba la matriz de permisos con cuatro roles (D-146).
- Se aprueba el domicilio con zonas, tarifa fija y entrega propia (D-147).
- Se aprueba un tenant por local; multi-sucursal queda fuera (D-122).
- Se aprueba el alta asistida con verificación manual y acceso en 48 h (D-149).
- Se difiere toda la parte legal; la decisión provisional D-150 queda cancelada a solicitud del dueño.
- Se fija el foco en el MVP y se difieren operación, venta y legal (D-151).
- Se escribe la especificación técnica de BL-01 en `05-frontend/cliente-api.md`.
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
