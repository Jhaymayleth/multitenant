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
| D-110 | 2026-11-26 | Producto | El mesero registra pedidos de mesa; el cliente anónimo solo envía solicitudes por QR; el cliente registrado reserva y pide a domicilio. | Refleja la operación real del restaurante. La parte de domicilio queda sin efecto por D-156. | SUSTITUIDA parcialmente (D-156) | 04, 05 |
| D-111 | 2026-11-26 | Producto | Caja ligera: registra pago, emite comprobante y QR de descarga; no es POS. | Reduce alcance y evita competir con sistemas contables. | SUSTITUIDA (D-145) | 04, 05 |
| D-112 | 2026-11-26 | Seguridad | Lixus no accede a datos operativos del restaurante; desactivar un tenant no borra sus datos. | Confianza comercial y continuidad. | APROBADA | 03, 06 |
| D-113 | 2026-11-26 | Producto | La versión inicial no calcula impuestos, propinas ni descuentos. | El restaurante los maneja fuera del sistema. | APROBADA | 04 |
| D-114 | 2026-11-26 | Pagos | Lixus no procesa dinero en la versión inicial; registra el pago y deja la pasarela para una integración posterior. | Evita PCI y cuentas de comercio antes de validar el producto. | SUSTITUIDA (D-145) | 04, 08 |
| D-115 | 2026-11-26 | Infraestructura | Producción en AWS con Docker Compose, Nginx, TLS Let's Encrypt y PostgreSQL RDS. | Ya está operativo y es reproducible. | APROBADA | 06 |
| D-116 | 2026-11-26 | Infraestructura | `main` despliega; `develop` integra. | Evita publicar trabajo a medias. | APROBADA | 06 |
| D-117 | 2026-11-26 | Seguridad | `/platform/*` se protege con `X-Platform-Admin-Key` como medida interina; el destino es JWT con rol Lixus y auditoría por usuario. | Cierra el acceso público hoy sin bloquear la operación. | APROBADA (interina) | 03, 06 |
| D-118 | 2026-11-26 | Documentación | Documentación en ocho áreas, un tema por archivo y features espejo backend/frontend. | Hace la documentación navegable y mantenible. | APROBADA | Todos |
| D-119 | 2026-11-26 | Documentación | El registro nuevo empieza en `D-101`; `D-001` a `D-076` son referencia histórica. | Evita colisiones y preserva trazabilidad. | APROBADA | 00 |
| D-120 | 2026-11-26 | Documentación | Se prohíbe el lenguaje académico en la documentación vigente. | La documentación debe servir para vender y operar. | APROBADA | Todos |
| D-121 | 2026-11-26 | Producto | La versión que se vende incluye onboarding, menú, personal, mesas/QR, pedidos, reservas, caja ligera y página pública; IA y automatización quedan fuera. | Es el mínimo que resuelve la operación diaria y permite cobrar. | APROBADA | 01, 04, 05 |
| D-122 | 2026-11-26 | Producto | Un tenant equivale a un local en la versión inicial. | Simplifica mesas, menú y reportes; las cadenas se atienden después. | APROBADA | 01, 04 |
| D-123 | 2026-11-26 | Producto | La interfaz y la documentación comercial están en español en la versión inicial. | El mercado objetivo inicial es hispanohablante. | APROBADA | 01, 05 |
| D-124 | 2026-11-26 | Producto | URL pública por ruta `/r/{slug}` en la versión inicial; subdominio propio queda como evolución. | Producción ya usa un dominio único y no exige DNS comodín. | APROBADA | 03, 05 |
| D-125 | 2026-11-26 | Calidad | Cada feature tiene criterio de aceptación verificable y estado explícito. | Evita declarar terminado lo que no funciona. | APROBADA | 07, features |
| D-126 | 2026-11-26 | Operación | El soporte de la versión inicial es por canal directo con horario definido; el SLA está por definir. | Se puede operar sin prometer lo que aún no se mide. | PROPUESTA | 06 |
| D-127 | 2026-11-26 | Legal | Todo documento legal se entrega como borrador y requiere revisión de un abogado en la jurisdicción definida. | Lixus no sustituye asesoría jurídica. | APROBADA | 08 |
| D-128 | 2026-11-26 | Producto | La versión inicial no promete procesamiento de pagos ni facturación fiscal. | Evita compromisos regulatorios antes de tener proveedor y jurisdicción. | APROBADA | 01, 04, 08 |
| D-129 | 2026-11-26 | Identidad | Se aprueban como definitivas la misión «ordenar la operación y la presencia digital del restaurante», la visión «ser el sistema operativo del restaurante independiente en Latinoamérica» y la promesa «Tu restaurante, en orden y en línea». | El dueño validó la identidad; de ella dependen el tono comercial, la venta y el onboarding. | APROBADA | 01 |
| D-130 | 2026-11-26 | Marca | Se mantiene «Lixus» como nombre comercial y se usará un dominio propio; el dominio exacto se define antes del lanzamiento comercial. | Un dominio de proveedor no transmite marca ni sostiene correos y página pública. | APROBADA | 01 |
| D-131 | 2026-11-26 | Experiencia | Se adopta WCAG 2.1 AA en los flujos críticos: login, menú, pedido, caja, reserva y página pública. | Es un estándar razonable, verificable y vendible sin encarecer el producto. | APROBADA | 01, 05 |
| D-132 | 2026-11-26 | Marca | El tono de Lixus es directo y cercano: frases cortas, lenguaje de restaurante y sin jerga técnica. | El dueño y el personal deben entender el producto sin capacitación extensa. | APROBADA | 01, 05 |
| D-133 | 2026-11-26 | Identidad | Se confirman los límites: Lixus no es un POS, marketplace, reparto propio, contabilidad ni IA que opere sola. | Evita prometer de más y protege el foco del primer cliente. | APROBADA | 01 |
| D-134 | 2026-11-26 | Identidad | La promesa se cumple cuando un restaurante opera un servicio completo —pedido, cocina, cobro y página— sin volver al papel ni a Excel. | Da una prueba verificable para venta, onboarding y métricas. | APROBADA | 01, 07 |
| D-135 | 2026-11-27 | Mercado | El arranque comercial es en Colombia, con una ciudad piloto que se define antes del lanzamiento. | El dueño fijó el país inicial; define moneda, jurisdicción y alcance de la primera venta. | APROBADA | 02, 08 |
| D-136 | 2026-11-27 | Mercado | La ciudad piloto es Barranquilla. | El dueño está ubicado allí y lo considera un mercado grande; facilita entrevistas, piloto y soporte presencial. | APROBADA | 02 |
| D-137 | 2026-11-27 | Mercado | El cliente ideal es un restaurante independiente de una sede, con 5–30 mesas, 3–20 empleados y operación de mesa y domicilio. | Define límites del plan, guion de venta y carga de onboarding. | APROBADA | 01, 02 |
| D-138 | 2026-11-27 | Mercado | El competidor principal de Lixus en Barranquilla es la operación con papel, Excel y WhatsApp, seguida de un POS local. | La venta se compara contra errores y tiempo perdido; no contra un software concreto. | APROBADA | 02 |
| D-139 | 2026-11-27 | Negocio | La estructura comercial es de tres planes; las cifras, la moneda y el ciclo se validan con entrevistas antes de publicarse. | Da un marco de venta sin inventar precios ni límites. | APROBADA | 02 |
| D-140 | 2026-11-27 | Negocio | El cobro de la suscripción se hace con pasarela de suscripción desde el inicio; el proveedor concreto y la facturación electrónica se definen con abogado y contador. | El dueño eligió cobro recurrente frente a transferencia manual. | APROBADA | 02, 08 |
| D-141 | 2026-11-27 | Negocio | No hay prueba gratuita: el restaurante paga desde el primer día con implantación acompañada. | El dueño prefirió evitar un periodo sin ingreso y sostener el onboarding como parte de la venta. | APROBADA | 02, 08 |
| D-142 | 2026-11-27 | Negocio | La cancelación surte efecto al final del periodo pagado; no hay reembolso proporcional salvo fallo atribuible a Lixus. | Da claridad contractual antes del primer cobro. | APROBADA | 02, 08 |
| D-143 | 2026-11-27 | Negocio | No hay descuento de lanzamiento; la implementación se cobra solo cuando hay migración de datos. | Evita fijar un precio bajo de entrada y cobra el trabajo real de carga. | APROBADA | 02 |
| D-144 | 2026-11-27 | Negocio | Se adopta un marco de métricas de producto, negocio y soporte sin metas numéricas hasta tener datos reales del piloto. | Evita decisiones basadas en cifras inventadas. | APROBADA | 02, 06 |
| D-145 | 2026-11-27 | Pagos | Lixus no gestiona caja ni recibe dinero de los pedidos: no hay rol de cajero. El total del pedido se cobra con la pasarela propia del restaurante y el dinero llega a su cuenta; Lixus genera el cobro, recibe el webhook y marca el pedido pagado. La suscripción se cobra con una pasarela separada (D-140). | El dueño aclaró que Lixus ordena la operación; el dinero de la venta pertenece al restaurante. | APROBADA | 01, 02, 03, 04, 05, 08 |
| D-146 | 2026-11-27 | Producto | Se aprueba la matriz de permisos con cuatro roles: owner, admin, mesero y cocinero, sin rol de cajero. | Cierra autorización en backend y guards del frontend. | APROBADA | 03, 04, 05 |
| D-147 | 2026-11-27 | Producto | El domicilio se opera con zonas y tarifa fija definidas por el restaurante, entrega con personal propio y cobro por su pasarela (D-145). | Sustituida: el dueño decidió sacar la gestión de domicilio de Lixus (D-155). | SUSTITUIDA (D-155) | 01, 04, 05 |
| D-149 | 2026-11-27 | Operación | El alta de un restaurante sigue: formulario, llamada de 20 minutos, documentos del negocio, revisión manual y acceso del CEO en 48 horas. | Define tiempo hasta la primera operación y mantiene la verificación gestionada (D-107). | APROBADA | 02, 06 |
| D-150 | 2026-11-27 | Legal | Se aplica la Ley 1581 de Colombia y habeas data como régimen provisional de protección de datos, pendiente de confirmación por abogado. | Cancelada a solicitud del dueño: la parte legal se difiere hasta que la aplicación funcione. | CANCELADA | 08 |
| D-151 | 2026-11-27 | Dirección | La prioridad actual es terminar el MVP de la aplicación. La operación comercial, el soporte formal y la parte legal quedan diferidos; hoy no hay venta activa. | El proyecto es personal y se ofrecerá a restaurantes en el futuro; no se decide nada de operación antes de tener un producto funcional. | APROBADA | 00, 01, 02, 06, 08 |
| D-152 | 2026-11-27 | Seguridad | La longitud mínima de contraseña es de 8 caracteres para cualquier cuenta, sin reglas distintas por rol. | Se mantiene la regla ya vigente en el schema de login; no se añade fricción al MVP. | APROBADA | 03, 04, 05 |
| D-153 | 2026-11-27 | Seguridad | Los códigos de recuperación de contraseña caducan a los 15 minutos y son de un solo uso. | Reduce la ventana de exposición sin dificultar la recuperación. | APROBADA | 03, 04, 05 |
| D-154 | 2026-11-27 | Producto | La plantilla de la página pública admite seis secciones: hero, menú, información, horarios, contacto y galería. | Mantiene una plantilla común verificable y deja fuera un constructor libre. | APROBADA | 01, 04, 05 |
| D-155 | 2026-11-27 | Producto | Lixus no gestiona el domicilio: no administra zonas, tarifas, flota ni seguimiento. El restaurante resuelve la entrega con servicios externos. Se admite un registro simple de pedido a domicilio sin logística y un enlace configurable en la página pública, con valor POR DEFINIR si no se provee. Decisión definitiva por ahora, sin fecha de revisión. | El dueño consideró que el domicilio ya está resuelto por servicios como Didi y que Lixus debe concentrarse en lo que resuelve: orden de mesa, pedido, cobro y página. | APROBADA | 01, 03, 04, 05 |
| D-156 | 2026-11-27 | Producto | El cliente registrado reserva mesa; no realiza pedidos a domicilio en Lixus. El pedido se toma en mesa. Sustituye la parte de domicilio de D-110. | La reserva es de la mesa; el pedido nace en mesa y lo registra el mesero. | APROBADA | 01, 04, 05 |
| D-157 | 2026-11-27 | Producto | El panel de mesas muestra tarjetas por piso y zona con colores: libre en verde, ocupada en rojo y reservada en azul. La ocupación y liberación se hacen con dos botones directos. | El mesero decide el estado de un vistazo y con un toque, sin buscar un identificador en una lista. | APROBADA | 01, 04, 05 |
| D-158 | 2026-11-27 | Producto | La etiqueta visible de la mesa se genera en el backend desde la configuración del restaurante. Los esquemas del MVP son numérico (`01`) y número con zona opcional. El esquema de piso, grupo con nombre y mesa (`#2BA-02`) queda como evolución sin fecha. | Una etiqueta legible reduce errores; generarla evita duplicados y nombres inconsistentes. El esquema compuesto exige más superficie de la que necesita el cliente ideal (D-137). | APROBADA | 01, 03, 04, 05 |
| D-159 | 2026-11-27 | Producto | Liberar una mesa manualmente exige motivo y solo se permite si no hay sesión activa ni pedido sin cobrar. Si se fuerza, la acción queda registrada. | Evita que una mesa aparezca libre mientras sigue abierta una operación pendiente, sin perder la trazabilidad de la acción manual. | APROBADA | 04, 05 |
| D-160 | 2026-11-27 | Producto | Las reservas online siguen en P1 (BL-11), no entran en el MVP. Se activan por configuración de cada tenant, sin ligarlas a un plan comercial mientras D-139 siga pendiente de cifras. | El foco es D-151; un flag por restaurante permite activar la capacidad cuando esté terminada sin prometerla antes. | APROBADA | 01, 02, 04, 05 |
| D-161 | 2026-11-27 | Producto | La ventana de reserva es configurable por tenant. Valores por defecto propuestos: mínimo 2 horas y máximo 30 días. Toda reserva y toda ocupación manual validan que la mesa esté libre en la franja; el mesero puede forzar con motivo registrado. | Evita solapes reales sin perder reservas del mismo día; una ventana fija de 8 horas a 1 día trataba el síntoma, no la causa. | APROBADA | 01, 04, 05 |
| D-162 | 2026-11-27 | Arquitectura | Se incorpora Elasticsearch como índice de solo lectura para la búsqueda de menú dentro de un restaurante. PostgreSQL sigue siendo la única fuente de verdad. El índice se crea por tenant con un nombre derivado en servidor del `schema_name`; la sincronía se hace desde PostgreSQL mediante un evento en Redis; si Elasticsearch falla, la búsqueda cae a full-text de PostgreSQL. El índice es reconstruible y no requiere backup propio. MongoDB, Cassandra y Neo4j quedan diferidos con criterios medibles (PD-31, PD-32, PD-33). | Es la única de las cuatro tecnologías que se añade sin quitar responsabilidad a PostgreSQL ni romper el aislamiento por schema: es una proyección derivada, degradable y sin obligación nueva de restauración. | APROBADA · pendiente de implementación | 00, 03, 04, 05, 07 |

> D-145 sustituye a D-111, D-114 y la parte de “caja ligera” de D-121 en todo lo relativo al cobro de pedidos. D-128 se mantiene para pagos de pedidos y se matiza con D-140 para la suscripción.

> D-155 sustituye a D-147 y D-156 deja sin efecto la parte de domicilio de D-110. El domicilio queda fuera del producto sin fecha; solo se registra como pedido simple y se puede mostrar un enlace externo configurado por el restaurante.

> D-162 complementa a D-104 sin reabrirla: añade un índice de búsqueda derivado, no una nueva fuente de verdad. El stack aprobado sigue siendo PostgreSQL + Redis; Elasticsearch entra solo como proveedor de lectura y con degradación controlada.

> **Parte legal diferida:** PD-14, PD-15, PD-16, PD-17 y PD-28 quedan POR DEFINIR. D-150 fue cancelada a solicitud del dueño. No se publica ningún documento legal como vigente hasta revisión de abogado y de que la aplicación funcione.

> **Foco actual (D-151):** solo MVP. Las decisiones de negocio, operación y legales ya aprobadas son planificación futura, no una operación en marcha. Las preguntas abiertas de esas áreas quedan diferidas.

## Decisiones que no se reabren sin evidencia nueva

- Aislamiento por schema (D-103).
- Stack (D-104), ampliado con el índice de búsqueda de D-162.
- Cookie `httpOnly` (D-105).
- Resolución de tenant en servidor (D-106).
- Alta gestionada por Lixus (D-107).
- Sin directorio de tenants (D-109).
- Canales de pedido: mesero en mesa y QR solo para solicitudes (D-110, D-156).
- Domicilio fuera de Lixus, sin zonas ni logística (D-155).
- Cobro de pedidos por pasarela propia del restaurante (D-145).
- Lixus sin acceso operativo (D-112).
