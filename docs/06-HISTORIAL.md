# 06 — Historial de cambios

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Última actualización:** 22 de octubre de 2026

Este documento registra cómo evolucionó la documentación y por qué cambiaron las decisiones. No sustituye a `02-DECISIONES.md`: explica el recorrido.

---

## 1. Cronología de la definición

| Momento | Qué ocurrió | Resultado |
|---|---|---|
| Inicio | Se revisa el enunciado del proyecto integrador y se plantean las preguntas de descubrimiento. | Requisitos académicos identificados: schema por tenant, JWT en cookie, CRUD, idempotencia, rate limiting, Docker, CI/CD, renderizado. |
| Ronda 1 | Se elige nicho restaurantes y una visión amplia (multirol, personalización, IA). | Visión de producto más ambiciosa que el mínimo académico. |
| Ronda 2 | Se responden alcance, roles, incorporación, personalización y suscripciones. | Primera SRS (v0.1) con requisitos funcionales y preguntas abiertas. |
| Ronda 3 | Se responden las preguntas abiertas de dominio, identidad, personalización, suscripciones, IA y tecnología. | SRS v0.2 con línea base consolidada y riesgos técnicos. |
| Aclaración de identidad | Se corrige la confusión entre cliente del restaurante y comprador del SaaS. | Aparecen CEO del tenant, personal, cliente registrado, cliente anónimo y Lixus. Se descarta "membresía" como término de negocio. |
| Ronda 4 | Se definen mesas, QR anónimo, comprobantes, Lixus, R2, SQLAlchemy, AWS y Freebuff. | SRS v0.3 con módulos ampliados y contradicciones visibles. |
| Cierre técnico | Se comparan proveedores de IA y se elige Groq; se confirma schema por tenant y el stack. | Arquitectura técnica v0.1 (documento de conversación). |
| Cierre de P-02 | Se define quién puede pedir: anónimo solo solicita por QR; cliente registrado reserva y pide domicilio; mesero registra el pedido. | Decisiones D-010, D-067, D-068 y D-069. |
| Cierre de P-03, P-05, P-08 y P-18 | Caja ligera con comprobante; Lixus sin acceso a datos del restaurante; sesión QR por condición; sin impuestos ni propinas. | Decisiones D-070, D-071 y D-072. |
| Cierre de P-24 | El pago en línea se confirma por webhook firmado con proveedor simulado; sin pasarela real en el MVP. | Decisión D-073. |
| Consolidación | Se reorganiza todo en la carpeta `docs/`. | Documentación v0.2 con 13 documentos y registro de decisiones D-001 a D-073. |

---

## 2. Cambios de decisión relevantes

| Tema | Primera postura | Postura vigente | Motivo |
|---|---|---|---|
| Aislamiento | Esquema por tenant como preferencia por confirmar | **Schema por tenant confirmado** | Requisito académico + decisión explícita del usuario |
| Alternativa interina | Tablas compartidas con `tenant_id` y RLS | Descartada como diseño del MVP | Se retomó la decisión de schema por tenant |
| Stack | "Por decidir"; React + Vite propuesto | **Next.js + FastAPI + SQLAlchemy + Alembic** | Decisión final del usuario y necesidad de SSR en páginas públicas |
| Registro de restaurantes | Registro autónomo | **Alta manual por Lixus** | Evitar activaciones sin control |
| Invitación de empleados | Enlace temporal por correo | **Correo pre-registrado + código** | Flujo descrito por el usuario |
| IA | Freebuff / Ollama / híbrido | **Groq + capa de proveedores intercambiables** | Freebuff no ofrece API pública integrable; Groq tiene cuotas utilizables |
| Almacenamiento | Proveedor por decidir | **Cloudflare R2** | Selección explícita y compatibilidad S3 |
| Despliegue | Local con Docker | **Local; AWS como destino previsto** | Dirección aprobada, arquitectura pendiente |
| Caja | Fuera del MVP | **Caja ligera:** registra pago, imprime comprobante y ofrece QR de descarga; sin POS | Decisión explícita (D-070) |
| Pago en línea | Pasarela real desde el inicio | **Webhook firmado + proveedor simulado**; pasarela real al desplegar | Evitar PCI y cuentas de comercio en una entrega de una semana (D-073) |
| Administrador global | Acceso excepcional auditado | **Sin acceso a datos operativos del restaurante** | Decisión explícita (D-071) |
| Impuestos y propinas | Por definir | **No se aplican en el MVP** | Decisión explícita (D-072) |
| Pedidos del cliente | Cliente puede pedir en línea | **Resuelto:** anónimo solo solicita por QR; cliente registrado reserva y pide domicilio; mesero registra el pedido de mesa | Aclaración explícita del flujo físico y de los canales |

---

## 3. Versiones de la documentación

### 0.1 — Borrador inicial
- `01-INDICE.md` (nombre anterior; hoy es `00-INDICE.md`) y `02-DECISIONES.md`.
- Decisiones D-001 a D-041.
- Estructura documental propuesta, sin completar.

### 0.2 — Consolidación (actual)
- Se renombra el índice a `00-INDICE.md`.
- Se añaden: requerimientos, arquitectura, módulos, pendientes, historial, modelo de datos, seguridad, robustez, entorno, plan y evaluación.
- Se actualizan estados de D-006, D-008, D-010, D-013, D-021, D-035, D-036 y D-040.
- Se añaden D-042 a D-073.
- Se formalizan las contradicciones C-01 a C-05.

---

## 4. Correcciones aplicadas en esta consolidación

| Corrección | Detalle |
|---|---|
| Confusión de actores | Se dejó de usar "usuario" como término único; se separaron CEO, personal, cliente registrado, cliente anónimo y Lixus. |
| Suscripción | Se aclaró que la paga el restaurante, no cada persona. |
| Privacidad comercial | Se formalizó que no se revela ni promociona a otros tenants. |
| Alcance de caja | Se resolvió con caja ligera: registro de pago y comprobante, sin POS (D-070). |
| Acceso de Lixus | Se limitó a metadatos y administración de plataforma, sin datos operativos (D-071). |
| Sesión QR | Se cambió el temporizador por una condición: pago o cancelación en efectivo (D-068). |
| Idempotencia y rate limiting | Se incorporaron como requisitos y decisiones, no como "extras". |
| Renderizado | Se mapeó por pantalla y se advirtió la ambigüedad de la modalidad académica. |
| Nombres de archivo | Se alineó el índice con la numeración real del directorio. |

---

## 5. Registro de riesgos aceptados

| Riesgo | Decisión | Mitigación |
|---|---|---|
| Sesión anónima de mesa accesible con el QR | Aceptado | Caducidad corta, límite de solicitudes, cierre por el mesero |
| Un solo local por tenant | Aceptado en el MVP | Documentado como evolución (P-20) |
| Sin procesamiento de pagos | Aceptado | Se registra estado; no se promete cobro |
| IA dependiente de cuotas gratuitas | Aceptado para el MVP | Capa de proveedores, medición y límites |
| Sin antivirus de archivos | Aceptado | Validación y re-codificación de imágenes |

---

## 6. Próximas actualizaciones previstas

1. Resolver P-01 y P-05 (matriz interna) antes de escribir autorización.
2. Resolver P-11 y P-23 antes de cerrar correo y domicilios.
3. Registrar el resultado de la PoC de migraciones (RT-01) y del pool (RT-02).
4. Actualizar este historial con cada decisión nueva o sustituida.

---

**Fin de `06-HISTORIAL.md`.**


---

## 4. Implementación Fase 2 — Hueso multitenant (octubre 2026)

Rama: `feat/phase-2-multitenant-core`. Commits:

| Commit | Descripción |
|---|---|
| `feat(db)` | Cadenas Alembic para `platform` y `tenant_<id>`; migración inicial de ambos schemas; `env.py` con filtro por schema y `search_path`. |
| `feat(auth)` | `get_tenant_context` resuelve tenant y membresía desde la base de datos (autoritativo); fija `search_path` local. |
| `feat(platform)` | Aprovisionamiento real: `CREATE SCHEMA`, migraciones del tenant, usuario CEO + membresía `owner`, `tenant_settings`, permisos a `lixus_app`, estado `pending_verification`, idempotencia por `Idempotency-Key`. |
| `feat(auth)` | Login con `tenant_slug` que emite JWT con `tenant_id`/`role`; hashing con `bcrypt` directo (compatibilidad bcrypt 5). |
| `test(isolation)` | Pruebas de aislamiento entre tenants; persistencia de `search_path` por transacción (`after_begin`); CI con Postgres/Redis. |

Notas técnicas:
- Se reemplazó `passlib` por `bcrypt` directo por incompatibilidad con bcrypt 5.
- Se añadió un listener `after_begin` en SQLAlchemy para reaplicar `SET LOCAL search_path` en cada transacción, evitando pérdida de aislamiento tras `commit`/`refresh`.
- Las migraciones del tenant se aplican vía `python -m alembic` con `-x schema=...`.
