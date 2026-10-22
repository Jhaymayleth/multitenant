# 00 — Índice maestro de documentación

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes  
**Versión de la documentación:** 0.2  
**Estado:** Línea base para iniciar el desarrollo  
**Última actualización:** 22 de octubre de 2026  

---

## 1. Qué es Lixus

Lixus es una plataforma SaaS multitenant para restaurantes independientes. Cada restaurante (tenant) administra su menú, personal, mesas, pedidos y reservas, publica una página propia y mantiene sus datos completamente separados de los demás.

El proyecto nace de dos fuentes:

1. El **enunciado académico**, que exige una arquitectura multitenant con un schema por tenant, autenticación segura, idempotencia, rate limiting, Docker y CI/CD.
2. Una **conversación de requerimientos** que amplió el producto hacia gestión integral, personalización visual, suscripciones e inteligencia artificial.

La documentación separa lo obligatorio de lo deseable para que el equipo no confunda la visión comercial con la entrega evaluable.

---

## 2. Mapa documental

| Documento | Contenido | Cuándo leerlo |
|---|---|---|
| `00-INDICE.md` | Este índice: navegación, estado y convenciones. | Primero, siempre |
| `01-REQUERIMIENTOS.md` | Requisitos académicos, funcionales, no funcionales, reglas y criterios de aceptación. | Antes de planificar o implementar |
| `02-DECISIONES.md` | Registro D-001 a D-066 con estado, motivo y consecuencias. | Antes de proponer un cambio |
| `03-ARQUITECTURA.md` | Componentes, multitenencia, resolución del tenant, migraciones, renderizado. | Antes de escribir código |
| `04-MODULOS.md` | Módulos funcionales, permisos, endpoints y reglas de negocio. | Al implementar cada módulo |
| `05-PENDIENTES.md` | Decisiones abiertas, contradicciones y riesgos con recomendación. | En cada reunión de avance |
| `06-HISTORIAL.md` | Cómo evolucionó la documentación y qué decisiones cambiaron. | Para entender el porqué |
| `07-MODELO-DATOS.md` | Tablas globales y por tenant, relaciones, índices y migraciones. | Al crear modelos y migraciones |
| `08-SEGURIDAD-Y-ACCESO.md` | Autenticación, sesión, autorización, CSRF, QR anónimo, IA y pruebas. | Al implementar auth y permisos |
| `09-ROBUSTEZ.md` | Idempotencia, rate limiting y concurrencia con pruebas. | Antes de la fase de robustez |
| `10-ENTORNO-Y-DESPLIEGUE.md` | Docker Compose, variables, CI/CD, R2 y despliegue. | Al montar el entorno |
| `11-PLAN-DE-IMPLEMENTACION.md` | Fases, orden de trabajo, definición de terminado y recortes. | Al planificar la semana |
| `12-ENTREGABLES-Y-EVALUACION.md` | Rúbrica, README, guion de sustentación y preguntas. | Antes de la entrega |
| `13-ROUTE-MVP.md` | Ruta de desarrollo orientada al enunciado y al cumplimiento del MVP. | Antes de arrancar la primera fase |

---

## 3. Rutas de lectura

**Para empezar a programar hoy**

1. `01-REQUERIMIENTOS.md` → qué se evalúa.
2. `03-ARQUITECTURA.md` → cómo se organiza.
3. `07-MODELO-DATOS.md` → qué tablas existen.
4. `11-PLAN-DE-IMPLEMENTACION.md` → en qué orden.
5. `13-ROUTE-MVP.md` → la ruta del MVP y cómo se encaja con el enunciado.
6. `09-ROBUSTEZ.md` → lo que no puede quedar para el final.

**Para entender una decisión**

`02-DECISIONES.md` → busca el ID → el documento de área explica la implementación.

**Para preparar la sustentación**

`12-ENTREGABLES-Y-EVALUACION.md` → `08-SEGURIDAD-Y-ACCESO.md` → `09-ROBUSTEZ.md` → `03-ARQUITECTURA.md`.

---

## 4. Estado del proyecto

| Área | Estado |
|---|---|
| Visión y nicho | Definido |
| Actores y lenguaje | Definido (CEO, personal, clientes, Lixus) |
| Modelo de aislamiento | Definido: schema por tenant |
| Stack | Definido: Next.js, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Redis, R2 |
| Requisitos académicos | Definidos y trazados |
| Alcance del MVP | Definido, con contradicciones abiertas documentadas |
| Modelo de datos | Diseño inicial |
| Seguridad | Diseñado, pendiente de implementar |
| Robustez | Diseñada, pendiente de implementar |
| Infraestructura | Local definida; producción pendiente |
| Código | No iniciado |
| Ruta del MVP | Definida en `13-ROUTE-MVP.md` |

**Resumen numérico:** 73 decisiones registradas, 19 pendientes abiertos de 24 registrados (P-02, P-03, P-08, P-18 y P-24 resueltos), 8 riesgos técnicos y 5 contradicciones documentadas (2 resueltas).

---

## 5. Decisiones cerradas que no deben reabrirse

| Tema | Decisión |
|---|---|
| Aislamiento | Un schema de PostgreSQL por tenant (D-042) |
| Stack | Next.js + FastAPI + PostgreSQL + SQLAlchemy + Alembic (D-043) |
| Sesión | JWT en cookie `httpOnly` (D-061) |
| Tenant | Resuelto en el servidor desde el token y la membresía (D-044) |
| Alta de tenants | Manual, con verificación y activación por Lixus (D-014) |
| Privacidad | Sin directorio ni publicidad cruzada entre tenants (D-049) |
| Pedidos | Solicitudes por QR + pedido del mesero; reserva y domicilio con cuenta (D-010, D-067, D-069) |
| Caja | Caja ligera: pago, comprobante impreso y QR de descarga; sin POS (D-070) |
| Lixus | Sin acceso a datos operativos del restaurante; desactivar no borra (D-071) |
| Impuestos | Sin impuestos, propinas ni descuentos (D-072) |
| Pago en línea | Webhook firmado con proveedor simulado; sin pasarela real en el MVP (D-073) |
| IA | Groq inicial + capa de proveedores; nunca escribe directo en la base (D-057, D-058) |
| Freebuff | Descartado como proveedor de inferencia (D-056) |
| Almacenamiento | Cloudflare R2 (D-059) |
| Robustez | Idempotencia y rate limiting obligatorios (D-062, D-063) |

---

## 6. Pendientes que bloquean el avance

| ID | Tema | Bloquea |
|---|---|---|
| P-01 | Modalidad académica A/B | Cierre y sustentación |
| P-05 | Matriz interna de permisos del restaurante | Autorización |
| P-11 | Proveedor de correo | Códigos y recuperación |
| P-23 | Domicilios: cobertura, costo y entrega | Domicilios |

El detalle, las opciones y la recomendación de cada uno están en `05-PENDIENTES.md`.

---

## 7. Convenciones de la documentación

### Identificadores

| Prefijo | Uso |
|---|---|
| `D-###` | Decisión |
| `RF-##` | Requisito funcional |
| `RNF-##` | Requisito no funcional |
| `RAC-##` | Requisito académico obligatorio |
| `RN-##` | Regla de negocio |
| `P-##` | Pendiente |
| `RT-##` | Riesgo técnico |
| `C-##` | Contradicción |
| `S-##` | Prueba de seguridad |
| `T-##` | Prueba de concurrencia |

### Estados de decisión

`APROBADA` · `POR CONFIRMAR` · `PENDIENTE` · `REVISIÓN NECESARIA` · `SUSTITUIDA`

### Jerarquía de fuentes

1. Enunciado académico (vinculante).
2. Decisiones aprobadas (`02-DECISIONES.md`).
3. Requisitos (`01-REQUERIMIENTOS.md`).
4. Diseño técnico (`03`, `07`, `08`, `09`, `10`).
5. Propuestas no aprobadas (solo si están marcadas como tales).

### Regla de mantenimiento

1. Una propuesta no es decisión sin confirmación explícita.
2. Toda decisión nueva entra en `02-DECISIONES.md` con su estado.
3. Las dudas van a `05-PENDIENTES.md`, no al registro de decisiones.
4. Los cambios importantes se anotan en `06-HISTORIAL.md`.
5. Si dos documentos se contradicen, se corrige el documento, no se improvisa en el código.
6. Ningún secreto real se escribe en estos documentos.

---

## 8. Glosario

| Término | Definición |
|---|---|
| **Tenant** | Restaurante independiente dentro de la plataforma; su límite es un schema de PostgreSQL |
| **Schema `platform`** | Espacio global con usuarios, tenants, membresías, planes y auditoría |
| **Schema del tenant** | Espacio exclusivo con menú, personal, mesas, pedidos, reservas y configuración |
| **CEO del tenant** | Persona que contrata el servicio y responde por el restaurante |
| **Administrador del restaurante** | Personal con funciones delegadas por el CEO |
| **Cliente registrado** | Cliente del restaurante con cuenta para reservas o comprobantes |
| **Cliente anónimo de mesa** | Sesión temporal asociada a un QR, sin cuenta |
| **Lixus** | Rol de administración global de la plataforma |
| **Membresía** | Relación técnica entre una identidad y un tenant con un rol (no es una suscripción comercial) |
| **Suscripción** | Plan comercial contratado por el tenant |
| **Idempotencia** | Repetir una operación con la misma clave produce un solo efecto y la misma respuesta |
| **Rate limiting** | Límite de peticiones por usuario, tenant o IP |
| **Tenant context** | Conjunto de datos (tenant, schema, rol) que la API establece por petición |
| **SSG / ISR** | Generación estática, con revalidación, usada en páginas públicas |
| **CSR** | Renderizado en el cliente, usado en paneles privados |

---

## 9. Uso con agentes de IA

Al delegar una tarea de código a un agente:

1. Indicar los documentos relevantes, no todo el repositorio.
2. Exigir que no invente requisitos ni decisiones.
3. Pedir que respete las decisiones cerradas de §5.
4. Pedir pruebas para aislamiento, idempotencia y permisos cuando la tarea los toque.
5. Actualizar `02-DECISIONES.md` o `05-PENDIENTES.md` si la tarea revela algo nuevo.

**Prompt base sugerido:**

```
Lee docs/00-INDICE.md, docs/01-REQUERIMIENTOS.md y docs/03-ARQUITECTURA.md.
Implementa <tarea> respetando las decisiones cerradas.
No inventes funcionalidades ni cambies el modelo de aislamiento.
Incluye pruebas de aislamiento entre tenants y validación en servidor.
Si falta una decisión, detente y anótala en docs/05-PENDIENTES.md.
```

---

## 10. Regla fundamental

**Ninguna recomendación, hipótesis o alternativa es una decisión aprobada sin confirmación explícita.**

Cuando exista incertidumbre, la documentación la muestra. El objetivo es que cualquier persona —o cualquier agente— pueda saber qué está decidido, qué falta y por qué.

---

**Fin de `00-INDICE.md`.**
