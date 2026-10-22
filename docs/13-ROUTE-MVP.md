# 13 — Ruta de desarrollo del MVP (cumplimiento del enunciado)

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes  
**Documento:** Ruta de desarrollo orientada al enunciado académico y al MVP  
**Versión:** 0.2  
**Estado:** Ruta de trabajo, no backlog completo  
**Última actualización:** 22 de octubre de 2026  
**Editor del repo:** Jhaymayeth (`josemrn2006@gmail.com`)  
**Repo:** `https://github.com/Jhaymayleth/multitenant.git`  
**Ramificaciones base:** `main` / `develop`

---

## 1. Propósito

Este documento define **el orden de desarrollo del MVP**, con un criterio claro:

- primero lo que el enunciado evalúa;
- luego lo que demuestra que el sistema es multitenant de verdad;
- y después lo demás, en el orden que deje la entrega lista para sustentar.

No es la lista de todas las cosas del producto. Es la secuencia mínima para llegar a una entrega con:

- aislamiento real de tenants,
- sesión httpOnly,
- robustez obligatoria,
- Docker y CI,
- y documentación que respalde lo exhibido.

---

## 2. Criterio de prioridad

Los trabajos del MVP se priorizan por:

1. **Obligatorio para el enunciado** (puntos evaluables directos).
2. **Bloquea la demostración del multitenant o de la robustez**.
3. **Necesario para sustentar el cambio en vivo**.
4. **Módulos de negocio del restaurante** (menú, pedidos, mesas, reservas, domicilios, caja, etc.).
5. **Opcionales, pendientes o posteriores**.

Este criterio significa que, por ejemplo, un módulo bonito pero no evaluable puede esperar a que la base del multitenant y la robustez estén listas.

---

## 3. Ramas del proyecto

El proyecto usa dos ramas base según convención:

- `main`
  - tema estable o línea base del proyecto.
  - no se usa como rama de trabajo diario.
- `develop`
  - rama de integración del trabajo en curso.
  - aquí van las features y mejoras antes de consolidar.

Esta separación es **convención del repo**, no una métrica de progreso por sí sola. Lo que importa para el enunciado es el historial coherente y la capacidad de explicar qué se hizo y por qué.

---

## 4. Fases de la ruta

### 4.1 Fase 0 — Configuración inicial del repo

**Objetivo:** un repositorio listo para trabajar y con estructura mínima para la entrega.

**Ítems:**

- repo clonado o iniciado en `https://github.com/Jhaymayleth/multitenant.git`
- autor local configurado como `Jhaymayeth` / `josemrn2006@gmail.com`
- ramas `main` y `develop`
- `.gitignore` sin entregables ni secretos
- `.env.example` sin secretos reales
- `docker-compose.yml` mínimo
- pipe de CI básico

**Criterio de salida:** el repo está listo para empezar a programar la base sin dependencias rastro de desarrollo local.

### 4.2 Fase 1 — Base del proyecto (estructura mínima que el enunciado exige)

**Objetivo:** tener el entorno local, la validación automática y el punto de partida documentado.

**Ítems:**

- `docker-compose.yml` mínimo con PostgreSQL y Redis, y los servicios de backend y frontend preparados.
- `.env.example` con las variables necesarias.
- `README.md` con los cinco puntos del enunciado en progreso.
- CI básico que instale dependencias, haga lint o build y falle si algo está mal.
- estructura del proyecto que deje claro backend y frontend.
- decisiones de stack y multitenancy actualizadas en la documentación.

**Criterio de salida:**

- `docker compose up` levanta los servicios requeridos sin pasos manuales ocultos.
- CI falla ante problemas de lint/build.

### 4.3 Fase 2 — Hueso multitenant

**Objetivo:** demostrar que el sistema puede crear un tenant aislado y que ese tenant se resuelve en cada petición.

**Ítems:**

- schema `platform` con usuarios, tenants y membresías.
- funcionalidad de aprovisionamiento de tenant con creación de schema y migraciones del tenant.
- resolución de tenant por JWT + membresía + `search_path` por transacción.
- primera prueba de aislamiento entre dos tenants.

**Criterio de salida:**

- un tenant nuevo queda operativo con su schema.
- un usuario de A no puede ver ni modificar datos de B.
- el mecanismo de resolución de tenant está explicado con el código real.

### 4.4 Fase 3 — Autenticación y sesión

**Objetivo:** que la sesión sea httpOnly y que las rutas privadas estén protegidas.

**Ítems:**

- registro e inicio de sesión.
- JWT en cookie `httpOnly`.
- rutas protegidas con dependencia de sesión + membresía.
- revocación básica y cierre de sesión.

**Criterio de salida:**

- la cookie puede verse en el navegador como httpOnly.
- sin sesión → 401.
- el contexto de tenant no proviene del cliente.

### 4.5 Fase 4 — Robustez obligatoria

**Objetivo:** cumplir los requisitos de idempotencia y rate limiting del enunciado.

**Ítems:**

- dos escrituras idempotentes con `Idempotency-Key`.
- prueba automatizada de que repetir no duplica.
- rate limiting en login y escrituras con 429 y `Retry-After`.
- política declarada y pruebas automatizadas.

**Criterio de salida:**

- el enunciado puede comprobar idempotencia y rate limiting con pruebas y demostración.

### 4.6 Fase 5 — Módulo de negocio mínimo dentro del tenant

**Objetivo:** un CRUD dentro del tenant y la capacidad de explayarlo en sustentación.

**Ítems:**

- menú o dominio mínimo equivalente con CRUD, validación y aislamiento.
- página pública mínima y panel privado mínimo.
- documentación de estrategias de renderizado según la modalidad declarada.

**Criterio de salida:**

- el enunciado puede reconocer el dominio de negocio del tenant y preguntar en vivo.

### 4.7 Fase 6 — Resto del producto necesario para el MVP

**Objetivos:** completar los módulos que el encuadre del MVP requiere.

**Ítems pendientes según la documentación vigente:**

- mesas y sesiones QR
- pedidos
- reservas
- domicilios
- caja ligera, comprobantes y webhook de pago
- planes y suscripciones (lo mínimo para la entrega)
- IA si se incluye como opcional
- automatización si se incluye como opcional

**Criterio de salida:**

- el producto es suficientemente completo para sustentar el MVP.

---

## 5. Qué no entra en la ruta MVP

Esto no forma parte del orden de desarrollo del MVP, aunque pueda ser útil después:

- pasarela real de pagos (solo sandbox por ahora, D-073)
- POS completo
- cobros automáticos de suscripciones en la primera fase
- constructor visual libre de páginas
- múltiples plantillas públicas
- app móvil nativa
- directorio público de restaurantes clientes
- gestión de flota de domicilios
- microservicios, base de datos por tenant o multi-región

---

## 6. Entregables del enunciado y a dónde apuntan en esta ruta

| Requisito del enunciado | Dónde se cubre |
|---|---|
| Multitenancy con schema por tenant | Fase 2 + documentación de arquitectura y modelo de datos |
| Autenticación y sesión httpOnly | Fase 3 |
| Dominio de negocio con CRUD y ORM | Fase 5 |
| Idempotencia (2 operaciones) | Fase 4 |
| Rate limiting con 429 + Retry-After | Fase 4 |
| Docker + .env.example | Fase 1 |
| CI | Fase 1 |
| README con los 5 puntos | Fase 1 y Fase 5 |
| Estrategias de renderizado | Fase 5 y decisión de modalidad |
| Sustentación | Ruta completa, con énfasis en Fase 2 y Fase 3 |

---

## 7. Salida de cada fase

Cada fase termina cuando:

- está implementada para el alcance declarado,
- tiene lo mínimo para demostrarla,
- queda reflejada donde corresponda en la documentación,
- y no deja una dependencia crítica sin resolver para la siguiente fase.

---

## 8. Nota de partición

Esta ruta está escrita para el **MVP**. Si en algún momento el trabajo diverge del enunciado o se amplía el alcance, este documento debe actualizarse antes de asumir que la secuencia sigue siendo válida.

---

**Fin de `13-ROUTE-MVP.md`.**
