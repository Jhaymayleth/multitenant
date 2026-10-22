# 11 — Plan de implementación

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Plan de trabajo para el MVP académico
**Última actualización:** 22 de octubre de 2026

---

## 1. Principio rector

**Primero la arquitectura evaluable, después el producto soñado.**

El enunciado no premia la cantidad de módulos: premia el aislamiento, la autenticación, la idempotencia, el rate limiting, el orden del código, Docker/CI y la capacidad de explicarlo. El plan construye primero esa columna vertebral y añade módulos de negocio encima.

**Congelamiento de alcance:** hasta que el checklist de la Fase 3 esté completo, no se añaden módulos nuevos. Las ideas se anotan en `05-PENDIENTES.md`.

---

## 2. Fases

### Fase 0 — Preparación (2–3 horas)

| Tarea | Entregable |
|---|---|
| Repositorio y estructura base | `frontend/`, `backend/`, `infra/`, `docs/` |
| Docker Compose con PostgreSQL y Redis | `docker-compose.yml` funcionando |
| Variables de entorno de ejemplo | `.env.example` |
| Lint y formateo | Ruff + ESLint configurados |
| README inicial | Arranque documentado |

**Terminado cuando:** `docker compose up` levanta base y Redis, y el README permite a otra persona arrancar el entorno.

---

### Fase 1 — Identidad, tenants y aislamiento (la más importante)

| Orden | Tarea |
|---|---|
| 1.1 | Modelo `platform`: `users`, `tenants`, `tenant_memberships`, `plans` |
| 1.2 | Migración de plataforma con Alembic |
| 1.3 | Aprovisionamiento: crear tenant + schema + migraciones de tenant |
| 1.4 | Autenticación con contraseña y JWT en cookie `httpOnly` |
| 1.5 | Contexto de tenant por petición (`search_path` por transacción) |
| 1.6 | Roles y guard de permisos |
| 1.7 | Pruebas de aislamiento: A no ve B |
| 1.8 | Prueba de concurrencia del pool |

**Terminado cuando:**

- Se crea un tenant desde la API y su schema existe con tablas.
- Un usuario puede iniciar sesión y recibe cookie `HttpOnly`.
- Dos tenants tienen datos separados y el acceso cruzado devuelve 404/403.
- El `search_path` no se filtra entre peticiones concurrentes.

**Riesgo:** si las migraciones multi-schema no funcionan, **parar y resolver**. No construir CRUD sobre una base insegura.

---

### Fase 2 — CRUD de negocio mínimo

| Orden | Tarea |
|---|---|
| 2.1 | Categorías y productos del menú (CRUD completo) |
| 2.2 | Validaciones de entrada y errores uniformes |
| 2.3 | Subida de imágenes a R2/MinIO con validación |
| 2.4 | Mesas, sesiones QR y ciclo de estado (`occupied → pending_payment → available`) |
| 2.5 | Pedidos de mesa con líneas y cálculo de totales en servidor |
| 2.6 | Pedido a domicilio para cliente registrado |
| 2.7 | Cocina: cola de pedidos con ID de mesa y cambios de preparación |
| 2.8 | Confirmación de pago y liberación automática de la mesa |
| 2.9 | Caja ligera: comprobante simple con QR de descarga |
| 2.10 | Webhook de pago firmado y página sandbox; liberación automática de mesa |

**Terminado cuando:** el CRUD de menú y pedidos funciona con validación, y cada operación está protegida y filtrada por tenant.

**Entidades académicas cubiertas:** categorías, productos y pedidos (3 entidades con CRUD; el mínimo exigido es 2).

---

### Fase 3 — Robustez obligatoria

| Orden | Tarea |
|---|---|
| 3.1 | Tabla de idempotencia y middleware/dependencia |
| 3.2 | Idempotencia en crear tenant y crear pedido |
| 3.3 | Rate limiting con Redis y token bucket |
| 3.4 | 429 + `Retry-After` + cabeceras informativas |
| 3.5 | Restricciones de concurrencia (sesión única, reservas) |
| 3.6 | Pruebas automatizadas de todo lo anterior |

**Terminado cuando** las pruebas demuestran: un solo pedido con clave repetida, 429 tras exceder el límite, y una sola sesión abierta por mesa.

Este es el punto de **entrega mínima defendible**.

---

### Fase 4 — Producto visible

| Orden | Tarea |
|---|---|
| 4.1 | Página pública con SSG/ISR y datos del tenant por `slug` |
| 4.2 | Panel del restaurante en CSR |
| 4.3 | Reservas |
| 4.4 | Portal de Lixus para verificar y activar tenants |
| 4.5 | Configuración visual de la página pública |

**Terminado cuando** un visitante ve el menú de un restaurante y el personal administra su negocio desde el panel.

---

### Fase 5 — Cierre académico

| Orden | Tarea |
|---|---|
| 5.1 | CI completo (lint, tests, build, Docker) |
| 5.2 | README con los cinco puntos del enunciado |
| 5.3 | Pruebas de aislamiento y de seguridad en CI |
| 5.4 | Datos demo y guion de sustentación |
| 5.5 | Revisión de cabeceras, cookies y secretos |

---

### Fase 6 — Opcionales (solo con lo anterior terminado)

1. IA con Groq: descripción de productos y consultas del menú.
2. Automatización con n8n: webhook al crear tenant.
3. Despliegue público en VPS.
4. Pruebas de aislamiento adicionales.

---

## 3. Distribución en siete días

| Día | Objetivo | Resultado verificable |
|---|---|---|
| 1 | Fase 0 + modelo de datos y migraciones | Base de datos versionada y entorno reproducible |
| 2 | Autenticación, sesión y contexto de tenant | Login funcional con cookie httpOnly |
| 3 | Aprovisionamiento y aislamiento | Dos tenants aislados + pruebas |
| 4 | CRUD de menú | Productos y categorías operativos |
| 5 | Pedidos, mesas y QR | Flujo presencial básico |
| 6 | Idempotencia, rate limiting y CI | Robustez demostrable |
| 7 | Documentación, pruebas finales y ensayo | Entrega y sustentación listas |

> La distribución es una guía. Si un día se retrasa, se recorta alcance de producto, **nunca** de aislamiento, idempotencia o rate limiting.

---

## 4. Orden de commits recomendado

Un historial coherente también se evalúa. Secuencia sugerida:

```
chore: bootstrap monorepo, docker compose and env example
feat(db): platform schema with users, tenants and memberships
feat(tenant): provision schema and run tenant migrations
feat(auth): password login with httpOnly jwt cookie
feat(auth): tenant context and membership guard
test(security): cross-tenant access is denied
feat(menu): categories and products crud
feat(menu): image upload with server validation
feat(tables): tables, qr sessions and service requests
feat(orders): create order with server-side totals
feat(reservations): booking with overlap protection
feat(robustness): idempotency for tenant and order creation
feat(robustness): redis token bucket rate limiting
ci: lint, tests, build and docker images
docs: readme with architecture, tenant resolution and decisions
```

Cada commit debe compilar y pasar las pruebas que existan en ese momento.

---

## 5. Estrategia de pruebas

| Nivel | Qué cubre | Herramienta |
|---|---|---|
| Unitarias | Servicios, cálculos, máquinas de estado | pytest |
| Integración | Endpoints con base de datos real | pytest + httpx |
| Seguridad | Aislamiento, IDOR, roles, cookies | pytest |
| Robustez | Idempotencia, rate limit, concurrencia | pytest + hilos/async |
| E2E (opcional) | Flujo del panel y página pública | Playwright |

**Mínimo para la entrega:** integración + seguridad + robustez. Las unitarias cubren cálculos de totales y transiciones.

Cobertura sugerida: no perseguir un porcentaje, sino cubrir los caminos que se van a demostrar.

---

## 6. Recortes permitidos si falta tiempo

En este orden:

1. Portal visual de Lixus → sustituir por endpoints y datos seed.
2. Configuración visual avanzada → dejar logo, colores y textos básicos.
3. Reservas → mantener el modelo, dejar solo creación y cancelación.
4. Comprobantes → solo registro de estado de pago.
5. IA → documentar el diseño y no implementarla.
6. Página pública → versión mínima con hero y menú.

**Nunca recortar:** aislamiento, sesión httpOnly, idempotencia, rate limiting, Docker, CI, README.

---

## 7. Riesgos del plan

| Riesgo | Señal temprana | Respuesta |
|---|---|---|
| Migraciones multi-schema fallan | Alembic no encuentra las tablas del tenant | Cambiar a SQL de migración propio o un engine por tenant |
| `search_path` se filtra | Prueba concurrente devuelve datos de otro tenant | Fijar `SET LOCAL` y revisar el pool; si persiste, engine por tenant |
| Alcance excesivo | Día 5 sin pedidos funcionando | Congelar módulos y cerrar robustez |
| Rate limiting mal configurado | Bloquea al personal legítimo | Ajustar cubo por usuario y excluir lecturas |
| Cookie no viaja entre frontend y API | 401 constante en el panel | Proxy en Next.js y mismo dominio |
| IA consume la cuota | 429 del proveedor | Caché, límite propio y fallback |

---

## 8. Definición de terminado (global)

Una tarea está terminada cuando:

- [ ] Cumple el requisito y sus criterios de aceptación.
- [ ] Tiene validación de entrada y errores claros.
- [ ] Está protegida por autenticación y permiso.
- [ ] Respeta el aislamiento del tenant.
- [ ] Tiene al menos una prueba automatizada relevante.
- [ ] Pasa lint y build.
- [ ] Está documentada si cambia una regla o una decisión.
- [ ] Puede explicarse en voz alta en menos de dos minutos.

---

## 9. Próximas cinco acciones concretas

1. Confirmar la modalidad académica con el docente (P-01).
2. Aprobar la matriz de permisos (P-05).
3. Crear el repositorio y el `docker-compose.yml` de la Fase 0.
4. Escribir la migración de plataforma y la de tenant.
5. Implementar la PoC de aprovisionamiento y aislamiento antes de cualquier CRUD.

---

**Fin de `11-PLAN-DE-IMPLEMENTACION.md`.**
