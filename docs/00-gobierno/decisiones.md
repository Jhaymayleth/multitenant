# Registro de decisiones

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Producto

Este registro empieza en `D-101`. Las decisiones `D-001` a `D-076` citadas en el material antiguo se conservan como referencia histórica en `_legado/`; no se reabren sin una decisión nueva.

Estados: `PROPUESTA`, `APROBADA`, `POR DEFINIR`, `SUSTITUIDA`.

| ID | Fecha | Área | Decisión | Motivo | Estado | Documentos afectados |
|---|---|---|---|---|---|---|
| D-101 | 2026-11-26 | Producto | Lixus se opera y vende como SaaS por suscripción a restaurantes independientes. | El producto debe sostener clientes reales, no una entrega. | APROBADA | Todos |
| D-102 | 2026-11-26 | Arquitectura | Un backend y un frontend con tres caras: web pública, panel del CEO y portal/solicitud de Lixus. | Evita duplicar sistemas y mantiene una sola fuente de verdad. | APROBADA | 03, 05 |
| D-103 | 2026-11-26 | Multitenancy | Un schema de PostgreSQL por tenant más el schema `platform`. | Aislamiento fuerte y verificable. | APROBADA | 03, 04 |
| D-104 | 2026-11-26 | Stack | Next.js 15 + React 19 + TypeScript; FastAPI + Python 3.12; PostgreSQL 16; SQLAlchemy + Alembic; Redis 7. | Es la base ya desplegada y conocida por el equipo. | APROBADA | 03, 04, 06 |
| D-105 | 2026-11-26 | Seguridad | Sesión con JWT en cookie `httpOnly` y `SameSite=Lax`. | Evita exponer el token a JavaScript. | APROBADA | 03, 04 |
| D-106 | 2026-11-26 | Multitenancy | El tenant se resuelve en el servidor desde la sesión y la membresía, nunca desde un header o body del cliente. | Evita IDOR y suplantación. | APROBADA | 03, 04 |
| D-107 | 2026-11-26 | Operación | El alta de restaurantes es gestionada por Lixus, no autoservicio, en la versión inicial. | Permite verificar el negocio y cuidar el onboarding. | APROBADA | 06 |
| D-108 | 2026-11-26 | Producto | Cada tenant tiene página pública con plantilla común y personalización de marca, textos, horarios y menú. | Da presencia digital sin construir un sitio a medida. | APROBADA | 05 |
| D-109 | 2026-11-26 | Producto | No hay directorio público ni publicidad cruzada entre tenants. | Protege la privacidad comercial. | APROBADA | 01, 03 |
| D-110 | 2026-11-26 | Producto | El mesero registra pedidos de mesa; el cliente anónimo solo envía solicitudes por QR; el cliente registrado reserva y pide a domicilio. | Refleja la operación real del restaurante. | APROBADA | 04, 05 |
| D-111 | 2026-11-26 | Producto | Caja ligera: registra pago, emite comprobante y QR de descarga; no es POS. | Reduce alcance y evita competir con sistemas contables. | APROBADA | 04, 05 |
| D-112 | 2026-11-26 | Seguridad | Lixus no accede a datos operativos del restaurante; desactivar un tenant no borra sus datos. | Confianza comercial y continuidad. | APROBADA | 03, 06 |
| D-113 | 2026-11-26 | Producto | La versión inicial no calcula impuestos, propinas ni descuentos. | El restaurante los maneja fuera del sistema. | APROBADA | 04 |
| D-114 | 2026-11-26 | Pagos | Lixus no procesa dinero en la versión inicial; registra el pago y deja la pasarela para una integración posterior. | Evita PCI y cuentas de comercio antes de validar el producto. | PROPUESTA | 04, 08 |
| D-115 | 2026-11-26 | Infraestructura | Producción en AWS con Docker Compose, Nginx, TLS Let's Encrypt y PostgreSQL RDS. | Ya está operativo y es reproducible. | APROBADA | 06 |
| D-116 | 2026-11-26 | Infraestructura | `main` despliega; `develop` integra. | Evita publicar trabajo a medias. | APROBADA | 06 |
| D-117 | 2026-11-26 | Seguridad | `/platform/*` se protege con `X-Platform-Admin-Key` como medida interina; el destino es JWT con rol Lixus y auditoría por usuario. | Cierra el acceso público hoy sin bloquear la operación. | APROBADA (interina) | 03, 06 |
| D-118 | 2026-11-26 | Documentación | Documentación en ocho áreas, un tema por archivo y features espejo backend/frontend. | Hace la documentación navegable y mantenible. | APROBADA | Todos |
| D-119 | 2026-11-26 | Documentación | El registro nuevo empieza en `D-101`; `D-001` a `D-076` son referencia histórica. | Evita colisiones y preserva trazabilidad. | APROBADA | 00 |
| D-120 | 2026-11-26 | Documentación | Se prohíbe el lenguaje académico en la documentación vigente. | La documentación debe servir para vender y operar. | APROBADA | Todos |
| D-121 | 2026-11-26 | Producto | La versión que se vende incluye onboarding, menú, personal, mesas/QR, pedidos, reservas, caja ligera y página pública; IA y automatización quedan fuera. | Es el mínimo que resuelve la operación diaria y permite cobrar. | PROPUESTA | 01, 04, 05 |
| D-122 | 2026-11-26 | Producto | Un tenant equivale a un local en la versión inicial. | Simplifica mesas, menú y reportes; las cadenas se atienden después. | PROPUESTA | 01, 04 |
| D-123 | 2026-11-26 | Producto | La interfaz y la documentación comercial están en español en la versión inicial. | El mercado objetivo inicial es hispanohablante. | APROBADA | 01, 05 |
| D-124 | 2026-11-26 | Producto | URL pública por ruta `/r/{slug}` en la versión inicial; subdominio propio queda como evolución. | Producción ya usa un dominio único y no exige DNS comodín. | PROPUESTA | 03, 05 |
| D-125 | 2026-11-26 | Calidad | Cada feature tiene criterio de aceptación verificable y estado explícito. | Evita declarar terminado lo que no funciona. | APROBADA | 07, features |
| D-126 | 2026-11-26 | Operación | El soporte de la versión inicial es por canal directo con horario definido; el SLA está por definir. | Se puede operar sin prometer lo que aún no se mide. | PROPUESTA | 06 |
| D-127 | 2026-11-26 | Legal | Todo documento legal se entrega como borrador y requiere revisión de un abogado en la jurisdicción definida. | Lixus no sustituye asesoría jurídica. | APROBADA | 08 |
| D-128 | 2026-11-26 | Producto | La versión inicial no promete procesamiento de pagos ni facturación fiscal. | Evita compromisos regulatorios antes de tener proveedor y jurisdicción. | APROBADA | 01, 04, 08 |
| D-129 | 2026-11-26 | Identidad | Se aprueban como definitivas la misión «ordenar la operación y la presencia digital del restaurante», la visión «ser el sistema operativo del restaurante independiente en Latinoamérica» y la promesa «Tu restaurante, en orden y en línea». | El dueño validó la identidad; de ella dependen el tono comercial, la venta y el onboarding. | APROBADA | 01 |
| D-130 | 2026-11-26 | Marca | Se mantiene «Lixus» como nombre comercial y se usará un dominio propio; el dominio exacto se define antes del lanzamiento comercial. | Un dominio de proveedor no transmite marca ni sostiene correos y página pública. | APROBADA | 01 |
| D-131 | 2026-11-26 | Experiencia | Se adopta WCAG 2.1 AA en los flujos críticos: login, menú, pedido, caja, reserva y página pública. | Es un estándar razonable, verificable y vendible sin encarecer el producto. | APROBADA | 01, 05 |

## Decisiones que no se reabren sin evidencia nueva

- Aislamiento por schema (D-103).
- Stack (D-104).
- Cookie `httpOnly` (D-105).
- Resolución de tenant en servidor (D-106).
- Alta gestionada por Lixus (D-107).
- Sin directorio de tenants (D-109).
- Canales de pedido (D-110).
- Caja ligera (D-111).
- Lixus sin acceso operativo (D-112).
