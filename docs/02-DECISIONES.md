# 02 — Registro de decisiones del proyecto Lixus

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Registro consolidado
**Fuentes:** Conversación de requerimientos + `Enunciado Proyecto Integrador SaaS Multitenant.pdf`
**Última actualización:** 22 de octubre de 2026

---

## 1. Cómo leer este documento

Este registro conserva **todas las decisiones** del proyecto, incluidas las que fueron sustituidas, para que nadie vuelva a proponer algo ya descartado ni aplique una idea antigua por error.

Cada decisión indica su estado. Los detalles de implementación no se repiten aquí: viven en los documentos de arquitectura, módulos, seguridad y robustez, que se referencian al final de cada entrada.

### Estados

| Estado | Significado |
|---|---|
| **APROBADA** | Decisión vigente y aceptada. Se implementa así. |
| **POR CONFIRMAR** | Hay preferencia, pero falta validación explícita o evidencia. No se implementa como definitiva. |
| **PENDIENTE** | Todavía no se ha decidido. |
| **REVISIÓN NECESARIA** | Decisión anterior que debe reconciliarse con una posterior o con el enunciado. |
| **SUSTITUIDA** | Reemplazada por otra decisión. Se conserva como historial. |

### Regla de oro

Ninguna recomendación se convierte en decisión aprobada sin confirmación explícita. Cuando hay conflicto, se documenta el conflicto; no se resuelve por conveniencia.

---

## 2. Índice de decisiones

| ID | Decisión | Estado |
|---|---|---|
| D-001 | Lixus será un SaaS multitenant para restaurantes | APROBADA |
| D-002 | El desarrollo comienza con un MVP funcional | APROBADA |
| D-003 | Entorno inicial local con Docker | APROBADA |
| D-004 | Diseño preparado para crecer | APROBADA |
| D-005 | El aislamiento de datos es requisito fundamental | APROBADA |
| D-006 | Esquema de PostgreSQL por restaurante | APROBADA (confirmada en D-042) |
| D-007 | Base de datos inicial en Docker | APROBADA |
| D-008 | Stack frontend/backend sin cerrar | SUSTITUIDA por D-043 |
| D-009 | Menú y página pública con alcance completo | APROBADA |
| D-010 | Canales de pedido y gestión interna | APROBADA |
| D-011 | La caja física queda fuera del MVP | APROBADA |
| D-012 | Caja física ≠ facturación de la suscripción SaaS | APROBADA |
| D-013 | Alcance de reservas, mesas y QR | APROBADA (caja ligera en D-070) |
| D-014 | Alta inicial de restaurantes manual | APROBADA |
| D-015 | Separación entre administración de Lixus y del restaurante | APROBADA |
| D-016 | El rol global se denomina "Lixus" | APROBADA |
| D-017 | Cada restaurante tiene un propietario responsable | APROBADA |
| D-018 | Roles del personal predefinidos | APROBADA |
| D-019 | Cuentas individuales por empleado | APROBADA |
| D-020 | El propietario gestiona el acceso del personal | APROBADA |
| D-021 | Invitaciones de empleados por enlace seguro | SUSTITUIDA por D-051 |
| D-022 | La baja de un empleado no elimina su historial | APROBADA |
| D-023 | Una persona puede tener cuentas en distintos restaurantes | APROBADA |
| D-024 | Acceso del personal independiente del público | APROBADA |
| D-025 | Correo/contraseña y Google | APROBADA (actualizada) |
| D-026 | Google no concede acceso automático a un tenant | APROBADA |
| D-027 | El acceso privilegiado es limitado y auditado | APROBADA |
| D-028 | Los requisitos académicos de seguridad se preservan | APROBADA |
| D-029 | Planes de suscripción para restaurantes | APROBADA |
| D-030 | Cobro automático como modelo deseado | APROBADA (futuro) |
| D-031 | Alta del tenant y activación comercial son distintas | APROBADA |
| D-032 | El impago no elimina datos | APROBADA |
| D-033 | Plantilla configurable inicial | APROBADA |
| D-034 | Personalización básica de identidad y contenido | APROBADA |
| D-035 | Cloudflare R2 para multimedia | APROBADA (confirmada en D-059) |
| D-036 | Arquitectura de IA en evaluación | SUSTITUIDA por D-056/D-057 |
| D-037 | Seleccionar modelo con pruebas reales | APROBADA |
| D-038 | Las escrituras de IA pasan por el backend | APROBADA |
| D-039 | Medir consumo de IA por restaurante | APROBADA |
| D-040 | AWS como alternativa de despliegue | APROBADA como dirección (D-060) |
| D-041 | Configuración reproducible | APROBADA |
| D-042 | Aislamiento definitivo: un schema por tenant | APROBADA |
| D-043 | Stack definitivo del MVP | APROBADA |
| D-044 | El tenant se resuelve en el servidor | APROBADA |
| D-045 | Cuatro reglas obligatorias de la capa de datos | APROBADA |
| D-046 | Identidades globales y perfiles por tenant | APROBADA |
| D-047 | Lenguaje de participantes del negocio | APROBADA |
| D-048 | La suscripción pertenece al tenant | APROBADA |
| D-049 | Sin publicidad ni revelación entre tenants | APROBADA |
| D-050 | Identidad reutilizable sin acceso implícito | APROBADA |
| D-051 | Alta de personal con código de verificación | APROBADA |
| D-052 | Sitio público y portal de tenants separados | APROBADA |
| D-053 | Mesas y sesiones QR dentro del MVP | APROBADA |
| D-054 | Pedido presencial por mesa, sin datos personales | APROBADA |
| D-055 | Cierre y reinicio de la sesión anónima | APROBADA |
| D-056 | Freebuff descartado como proveedor de inferencia | APROBADA |
| D-057 | Groq como proveedor inicial de IA | APROBADA |
| D-058 | Capa de proveedores de IA intercambiables | APROBADA |
| D-059 | Cloudflare R2 confirmado | APROBADA |
| D-060 | AWS como destino de despliegue previsto | APROBADA |
| D-061 | JWT en cookie httpOnly | APROBADA |
| D-062 | Idempotencia obligatoria | APROBADA |
| D-063 | Rate limiting obligatorio | APROBADA |
| D-064 | CI/CD obligatorio | APROBADA |
| D-065 | Dos estrategias de renderizado | APROBADA |
| D-066 | README con evidencias de sustentación | APROBADA |
| D-067 | Cuenta del cliente para reservas y domicilios | APROBADA |
| D-068 | Ciclo de vida de la mesa y liberación automática | APROBADA |
| D-069 | Pedido a domicilio como canal separado | APROBADA |
| D-070 | Caja ligera con comprobante simple | APROBADA |
| D-071 | Límites del administrador global Lixus | APROBADA |
| D-072 | Sin impuestos, propinas ni descuentos | APROBADA |
| D-073 | Confirmación de pago en línea por webhook firmado | APROBADA |

---

## 3. Visión y enfoque del producto

### D-001. Lixus será un SaaS multitenant para restaurantes
**Estado:** APROBADA

Plataforma SaaS para restaurantes donde varios negocios comparten infraestructura con datos, usuarios y operaciones separados. El aislamiento se contempla desde el diseño.

### D-002. El desarrollo comienza con un MVP funcional
**Estado:** APROBADA

La primera versión debe ser útil y estar bien diseñada para evolucionar, no cubrir todas las funcionalidades imaginables. Se prioriza la arquitectura sobre la cantidad de módulos.

### D-003. Entorno inicial local con Docker
**Estado:** APROBADA

Desarrollo local con Docker. Las decisiones posteriores de infraestructura deben permitir la transición a un entorno real.

### D-004. La plataforma debe prepararse para crecer
**Estado:** APROBADA

El diseño admite nuevos módulos, tenants y funcionalidades sin romper el aislamiento. Esto no obliga a implementar infraestructura compleja desde el día uno.

---

## 4. Arquitectura y aislamiento

### D-005. El aislamiento de datos es un requisito fundamental
**Estado:** APROBADA

Cada restaurante accede solo a su información. La separación se aplica en backend y base de datos; ocultar elementos en la interfaz no cuenta como aislamiento. Se contemplan autenticación, autorización y prevención de accesos cruzados.

### D-006. Esquema de PostgreSQL por restaurante
**Estado:** APROBADA (confirmada definitivamente en D-042)

Se evaluó frente a tablas compartidas con `tenant_id` y base de datos por tenant. Criterios usados: nivel de aislamiento, complejidad de migraciones, creación/eliminación de tenants, copias de seguridad, mantenimiento y costos operativos.

La preferencia inicial quedó confirmada al final de la conversación: **un schema por tenant**, con un schema global para la plataforma.

### D-007. Base de datos inicial en Docker
**Estado:** APROBADA

PostgreSQL forma parte del entorno local con Docker. Configuración, persistencia, migraciones, credenciales y respaldos se detallan en `10-ENTORNO-Y-DESPLIEGUE.md`.

### D-008. Stack frontend/backend sin cerrar
**Estado:** SUSTITUIDA por D-043

Se planteó Next.js sin aprobarlo. Tampoco estaban aprobados React con backend independiente, SQLAlchemy ni una estructura de servicios concreta. Esta entrada se conserva para evitar citarla como vigente.

---

## 5. Alcance del MVP

### D-009. El menú y la página pública tienen alcance completo
**Estado:** APROBADA

El MVP incluye menú público y página por restaurante, con identidad visual coherente. El detalle de secciones y edición está en `04-MODULOS.md`.

### D-010. Canales de pedido y gestión interna
**Estado:** APROBADA (resuelve P-02 y C-01)

Se distinguen tres situaciones:

1. **Cliente anónimo en mesa:** escanea el QR (que identifica la mesa), envía solicitudes de servicio (queja, falta algo, quiero algo, pedir la cuenta) y puede registrarse o iniciar sesión desde ahí. No puede crear pedidos ni reservar sin cuenta. Al iniciar el servicio, la mesa queda **bloqueada para reservas** en tiempo real (D-068).
2. **Cliente registrado del restaurante:** puede reservar una mesa y hacer pedidos a domicilio. Su cuenta pertenece a ese restaurante.
3. **Personal:** el mesero registra el pedido presencial por mesa; la cocina lo recibe con el ID de mesa y actualiza la preparación.

El pedido presencial lo registra el mesero, no el cliente. El QR no es un canal de autopedido: identifica la mesa y comunica al cliente con el mesero.

**Motivo:** el cliente físico puede pedir sin cuenta, pero reservar o pedir a domicilio requiere identificación y contacto.

### D-011. La caja física completa queda fuera del MVP
**Estado:** APROBADA · **Aclarada por:** D-070

Lixus no construye un punto de venta (POS) propio: no hay turnos de caja, arqueo, inventario, devoluciones ni facturación fiscal. Los restaurantes ya tienen su sistema de caja y no se duplica esa funcionalidad.

Sí existe una **caja ligera** para registrar la compra, confirmar el pago, imprimir el comprobante y ofrecer su descarga por QR (D-070). No procesa dinero por sí misma.

### D-012. Caja física ≠ facturación de la suscripción SaaS
**Estado:** APROBADA

Excluir la caja del restaurante no exime a Lixus de gestionar el cobro de sus propias suscripciones. Son responsabilidades distintas.

### D-013. Alcance de reservas, mesas y sesiones QR
**Estado:** APROBADA (caja ligera en D-070)

El MVP gestiona reservas, mesas y sesiones QR anónimas. Las reservas requieren cuenta de cliente y mesa concreta; las sesiones QR permiten solicitudes sin cuenta. La caja es ligera y no un POS (D-070); el pago en línea se confirma por webhook con proveedor simulado (D-073).

---

## 6. Restaurantes y cuentas

### D-014. El alta inicial de los restaurantes es manual
**Estado:** APROBADA

Lixus crea el espacio del restaurante y habilita el acceso del propietario. No hay registro público autónomo que active un tenant sin intervención de la plataforma. Sustituye la propuesta anterior de registro autónomo.

### D-015. Separación entre administración de Lixus y del restaurante
**Estado:** APROBADA

Dos ámbitos: administración de la plataforma (aprovisionamiento, soporte, seguridad) y administración del restaurante (operación cotidiana). Ser propietario de un restaurante no otorga acceso global.

### D-016. El rol global se denomina "Lixus"
**Estado:** APROBADA

Se evita la convención `admin` como nombre del rol global. **El nombre es una convención, no una medida de seguridad**: la protección real está en credenciales robustas, permisos, MFA, rate limiting y auditoría (ver `08-SEGURIDAD-Y-ACCESO.md`).

### D-017. Cada restaurante tiene un propietario responsable
**Estado:** APROBADA

El propietario administra su espacio y puede delegar funciones en un administrador. La delegación no alcanza otros restaurantes ni la plataforma global.

### D-018. Roles del personal predefinidos
**Estado:** APROBADA

Roles y permisos definidos por Lixus. No se construye un editor libre de roles. La lista final se ajusta a los módulos del MVP: CEO, administrador, mesero, cajero, cocinero.

### D-019. Cuentas individuales por empleado
**Estado:** APROBADA

Cada empleado usa su propia cuenta para asignar permisos y mantener historial de acciones.

### D-020. El propietario gestiona el acceso del personal
**Estado:** APROBADA

Invitación, asignación de rol, consulta de usuarios y desactivación de accesos.

### D-021. Invitaciones de empleados por enlace seguro
**Estado:** SUSTITUIDA por D-051

Se había previsto enviar un enlace temporal por correo. El flujo vigente usa el correo pre-registrado por el restaurante más un código de verificación en el primer acceso. Los enlaces de un solo uso se conservan solo para recuperación de contraseña.

### D-022. La baja de un empleado no elimina su historial
**Estado:** APROBADA

La cuenta se desactiva, las sesiones se revocan y el historial de pedidos y acciones se conserva.

### D-023. Una persona puede tener cuentas en distintos restaurantes
**Estado:** APROBADA

Cada cuenta pertenece a su espacio y tiene permisos independientes. Compartir correo no concede acceso a otros restaurantes.

---

## 7. Autenticación y seguridad

### D-024. El acceso del personal es independiente del público
**Estado:** APROBADA

El cliente consulta el menú y usa funciones públicas sin cuenta de empleado. El personal tiene autenticación propia para funciones privadas.

### D-025. Correo/contraseña y Google
**Estado:** APROBADA (actualizada)

Se admiten correo y contraseña; Google se ofrece como alternativa para clientes registrados. La recuperación de contraseña usa un enlace de un solo uso enviado por correo. Para cuentas que dependan solo de Google, la recuperación se delega al proveedor. MFA para Lixus se detalla en `08-SEGURIDAD-Y-ACCESO.md`.

### D-026. Google no concede acceso automático a un restaurante
**Estado:** APROBADA

La autenticación externa identifica al usuario. El acceso depende de una relación autorizada con ese tenant y de permisos explícitos.

### D-027. El acceso privilegiado es limitado y auditado
**Estado:** APROBADA · **Precisada por:** D-071

Lixus interviene solo en tareas autorizadas de aprovisionamiento, verificación y administración de la plataforma. Las acciones quedan registradas. **No accede a datos operativos del restaurante** (empleados, clientes, pedidos, reservas, pagos ni configuración).

### D-028. Los requisitos académicos de seguridad se preservan
**Estado:** APROBADA

Autorización en backend, protección de credenciales y sesiones, defensa ante abuso de endpoints, límites de frecuencia e idempotencia en escrituras. Detalle en `08-SEGURIDAD-Y-ACCESO.md` y `09-ROBUSTEZ.md`.

---

## 8. Suscripciones y modelo comercial

### D-029. Lixus ofrece planes de suscripción
**Estado:** APROBADA

Planes Básico, Intermedio y Avanzado. La asignación definitiva de funcionalidades, límites y precios sigue pendiente (P-09).

### D-030. Se prefiere el cobro automático
**Estado:** APROBADA (modelo deseado a futuro)

La pasarela no está seleccionada. Wompi y Stripe Billing son candidatos a evaluar. En el MVP la activación es manual (D-031).

### D-031. Alta del tenant y activación comercial son distintas
**Estado:** APROBADA

El alta es manual, aunque el cobro deseado sea automático. Creación del espacio, activación de la cuenta y estado de la suscripción se gestionan de forma coherente.

### D-032. El impago no elimina datos
**Estado:** APROBADA

Se restringen funciones premium y se permite al propietario gestionar su cuenta. Las reglas exactas de gracia y reactivación están pendientes (P-10).

---

## 9. Página pública y personalización

### D-033. El MVP usa una plantilla configurable
**Estado:** APROBADA

Una plantilla bien diseñada, alimentada por configuración. La arquitectura permite añadir plantillas después.

### D-034. Personalización inicial de identidad y contenido
**Estado:** APROBADA

Logo, colores, textos, imagen principal y visibilidad de secciones. Reordenar libremente todas las secciones es una ampliación, no una obligación del MVP.

---

## 10. Multimedia

### D-035. Cloudflare R2 para almacenamiento multimedia
**Estado:** APROBADA (confirmada en D-059)

Se identificó como opción preferida; quedó confirmada al seleccionarla explícitamente. Los límites y condiciones comerciales deben verificarse antes de presupuestar.

---

## 11. Inteligencia artificial

### D-036. Arquitectura de IA en evaluación
**Estado:** SUSTITUIDA por D-056 y D-057

Se evaluaron Freebuff, Ollama y un enfoque híbrido. La evaluación se cerró: Freebuff no se adopta como proveedor y se inicia con Groq, manteniendo una capa intercambiable.

### D-037. Selección de modelo basada en pruebas reales
**Estado:** APROBADA

Antes de comprometerse con infraestructura o proveedor se prueban tareas representativas midiendo calidad, latencia, recursos, concurrencia y costo.

### D-038. Las escrituras de IA pasan por el backend
**Estado:** APROBADA

La IA interpreta y genera contenido; los cambios de datos se ejecutan mediante herramientas controladas que validan permisos, reglas y auditoría. El prompt no es la frontera de seguridad.

### D-039. Se mide el consumo de IA por restaurante
**Estado:** APROBADA

Se registra consumo desde el inicio, aunque el cobro por IA no forme parte del MVP.

---

## 12. Infraestructura y operación

### D-040. AWS como alternativa de despliegue
**Estado:** APROBADA como dirección (ver D-060)

Se consideró AWS y también un VPS. La arquitectura de producción no está cerrada.

### D-041. Configuración reproducible
**Estado:** APROBADA

Entorno local reproducible con Docker y documentación. Variables de entorno, credenciales de ejemplo, migraciones y ejecución documentadas sin secretos reales.

---

## 13. Decisiones de consolidación técnica

### D-042. Aislamiento definitivo: un schema por tenant
**Estado:** APROBADA · **Sustituye:** propuesta interina de tablas compartidas con `tenant_id`

PostgreSQL con un schema global (`platform`) para tenants, identidades, membresías, planes y auditoría, y **un schema por restaurante** con las tablas de su dominio.

El schema se crea automáticamente al activar el tenant y se nombra con un identificador generado por el servidor (por ejemplo `tenant_<uuid corto>`), nunca con texto libre del cliente.

**Motivo:** aislamiento estructural, alineación con el requisito académico RAC-01 y separación clara de dominios.
**Consecuencias:** hay que resolver migraciones multi-schema, contexto de conexión y pruebas de aislamiento. Ver `03-ARQUITECTURA.md` y `07-MODELO-DATOS.md`.
**Alternativa descartada:** tablas compartidas con `tenant_id` y RLS como mecanismo principal. Se conserva como referencia histórica, no como diseño vigente.

### D-043. Stack definitivo del MVP
**Estado:** APROBADA · **Sustituye a:** D-008

| Capa | Tecnología |
|---|---|
| Frontend | Next.js + TypeScript |
| Backend | FastAPI + Python |
| Base de datos | PostgreSQL 16 |
| ORM | SQLAlchemy 2.x |
| Migraciones | Alembic |
| Caché / límites | Redis |
| Archivos | Cloudflare R2 |
| Entorno | Docker Compose |
| Organización | Monolito modular por dominios |

La API es independiente del frontend. Next.js se usa como aplicación React con capacidades de renderizado para las páginas públicas. La distribución de responsabilidades y la modalidad académica a declarar están en P-01.

### D-044. El tenant se resuelve en el servidor
**Estado:** APROBADA

La API obtiene el tenant de la sesión y de una relación de acceso validada. No acepta un nombre de schema, un `tenant_id` libre ni un rol enviados por el navegador. Cambiar de restaurante emite un token nuevo.

**Consecuencia:** el frontend puede enviar un identificador de tenant solo como intención; la autorización siempre se recalcula en el servidor.

### D-045. Cuatro reglas obligatorias de la capa de datos
**Estado:** APROBADA

1. **La API determina el schema autorizado.** Nunca se usa un nombre de schema proveniente del cliente.
2. **Permisos restringidos en PostgreSQL.** La aplicación no es superusuario ni dueña indiscutible de todos los schemas.
3. **Conexiones seguras.** El contexto del schema se establece y se limpia por transacción al reutilizar el pool; ninguna petición hereda el contexto anterior.
4. **Migraciones automatizadas.** Un proceso actualiza todos los schemas de tenants y falla de forma visible.

**Consecuencia:** estas reglas se prueban explícitamente; no son convenciones opcionales.

### D-046. Identidades globales y perfiles por tenant
**Estado:** APROBADA

La identidad de una persona vive en el schema global (`platform.users`). Su relación con cada restaurante vive en `platform.tenant_memberships`. Los datos propios del negocio (perfil de empleado, perfil de cliente, historial) viven en el schema del tenant.

**Motivo:** permite que la misma persona acceda a varios restaurantes sin compartir datos entre ellos y sin duplicar credenciales.

### D-047. Lenguaje de participantes del negocio
**Estado:** APROBADA

Se distinguen: **CEO del tenant** (comprador/responsable), **administrador del restaurante**, **personal operativo**, **cliente registrado**, **cliente anónimo de mesa**, **visitante público** y **Lixus**.

**Motivo:** "usuario" mezclaba al comprador del SaaS con el cliente del restaurante y generaba requisitos contradictorios.

### D-048. La suscripción pertenece al tenant
**Estado:** APROBADA

El restaurante paga el plan. El personal invitado y los clientes del restaurante no compran licencias. Los límites del plan se aplican al tenant.

### D-049. Sin publicidad ni revelación entre tenants
**Estado:** APROBADA

No existe directorio de restaurantes clientes ni menciones cruzadas por defecto. La página de un restaurante no muestra que otro restaurante usa la plataforma. Tampoco se revela a un tenant qué competidores son clientes.

**Motivo:** es una condición comercial explícita del producto; los restaurantes no aceptarían promocionar a su competencia.

### D-050. Identidad reutilizable sin acceso implícito
**Estado:** APROBADA

Una misma identidad puede existir en varios tenants sin error. Tener cuenta no concede acceso a ningún panel: los permisos se asignan por tenant. Si la misma persona aparece en dos schemas, es un caso válido.

### D-051. Alta de personal con código de verificación
**Estado:** APROBADA · **Sustituye a:** D-021

El CEO o administrador registra al empleado con su correo y su rol. El empleado, en su primer acceso, verifica su identidad con un código de un solo uso. El rol de cliente es predeterminado y no se asigna manualmente como si fuera personal.

**Pendiente:** vigencia del código, límite de intentos y reenvío (ver `08-SEGURIDAD-Y-ACCESO.md`).

### D-052. Sitio público y portal de tenants separados
**Estado:** APROBADA

Se distinguen dos ámbitos:

1. **Sitio público:** páginas de cada restaurante y funciones para sus clientes.
2. **Portal de tenants:** creación, verificación, configuración y administración del restaurante, operado por el CEO y por Lixus.

**Motivo:** separar la identidad pública del restaurante del proceso comercial y administrativo de la plataforma.

### D-053. Mesas y sesiones QR dentro del MVP
**Estado:** APROBADA · **Resuelve:** D-013

Cada mesa tiene un QR con un token opaco que identifica la mesa. Al escanearlo, el cliente abre una sesión anónima y solicita atención con botones (queja, falta algo, quiero algo, pedir la cuenta). El mesero recibe la solicitud con el número de mesa y puede actualizar el estado de la mesa según el ciclo definido en D-068.

El pedido presencial lo registra el mesero y se envía a cocina con el ID de mesa.

**Motivo:** sin mesas no se puede asociar una solicitud o un pedido a un lugar físico.

### D-054. Pedido presencial por mesa, sin datos personales
**Estado:** APROBADA

El pedido presencial se asocia a la mesa y a la sesión, no a los datos del cliente. Los datos personales se solicitan solo para reservas, domicilios, comprobantes por correo o creación de cuenta.

Un cliente registrado puede iniciar sesión desde el QR, pero el pedido de mesa sigue perteneciendo a la mesa, no al perfil del cliente.

### D-055. Cierre y reinicio de la sesión anónima
**Estado:** APROBADA · **Completada por:** D-068

Al confirmar el pago, la sesión se cierra y la mesa se libera automáticamente. El siguiente cliente empieza desde cero. Una mesa solo puede tener una sesión activa.

**Cierre:** la sesión no caduca por tiempo (D-068); volver a escanear el QR reanuda la sesión abierta.

### D-056. Freebuff descartado como proveedor de inferencia
**Estado:** APROBADA · **Sustituye a:** D-036

Freebuff se evaluó como referencia, pero no se adopta como proveedor de inferencia del SaaS: su documentación no garantiza una API pública general para consumir modelos desde una aplicación propia sin credenciales, ni condiciones de uso adecuadas para producción. Se usa como herramienta de apoyo al desarrollo, no como dependencia del producto.

### D-057. Groq como proveedor inicial de IA
**Estado:** APROBADA

Se inicia con Groq y el modelo `openai/gpt-oss-20b`, por cuotas gratuitas utilizables desde el backend, compatibilidad con herramientas y buena latencia. El identificador del modelo se configura por variable de entorno.

**Base de la aprobación:** el usuario aceptó la recomendación y continuó con el diseño. Si las pruebas de calidad en español no son suficientes (D-037), el proveedor se revisa sin cambiar la arquitectura de la capa de IA.

**Consecuencia:** los límites son de la organización, no por tenant; por eso se registra consumo por restaurante y se aplican cuotas propias.

### D-058. Capa de proveedores de IA intercambiables
**Estado:** APROBADA

La aplicación no llama a un proveedor desde el código de negocio. Un servicio en Python centraliza selección de modelo, claves, reintentos clasificados, failover, caché y medición. OpenRouter y Gemini quedan como rutas alternativas.

**Regla:** nunca se reintenta a ciegas; se distingue error temporal, cuota agotada, error de autenticación y respuesta inválida.

### D-059. Cloudflare R2 confirmado
**Estado:** APROBADA · **Actualiza a:** D-035

R2 se usa para imágenes y archivos. Bucket privado, validación de tipo y tamaño en servidor y entrega mediante URL firmada o CDN controlado. La cuota gratuita (10 GB-mes, 1 M operaciones clase A, 10 M clase B, sin cargo de egress) es una referencia sujeta a condiciones vigentes, no una garantía.

### D-060. AWS como destino de despliegue previsto
**Estado:** APROBADA como dirección · **Actualiza a:** D-040

El despliegue productivo apunta a AWS, con posibilidad de VPS según costo y operación. La arquitectura concreta (cómputo, base de datos, red, secretos, respaldos) queda pendiente de diseño (P-14).

### D-061. JWT en cookie httpOnly
**Estado:** APROBADA · **Requisito académico RAC-02**

La sesión se transporta en un JWT firmado dentro de una cookie `HttpOnly`, `Secure` en producción y `SameSite` adecuado. Nunca se guarda en `localStorage`. El token incluye identidad, tenant activo y rol; la autorización se recalcula contra la base de datos.

**Consecuencia:** hay que manejar CSRF, expiración, rotación y revocación (ver `08-SEGURIDAD-Y-ACCESO.md`).

### D-062. Idempotencia obligatoria
**Estado:** APROBADA · **Requisito académico RAC-04**

Al menos dos escrituras idempotentes: **crear tenant**, **crear pedido** y **confirmar pago**. La confirmación del pago también es idempotente porque libera la mesa y no puede ejecutarse dos veces. Se implementan con header `Idempotency-Key`, huella de la petición, almacenamiento del resultado y reproducción de la respuesta original.

**Motivo:** los reintentos y dobles clics no deben duplicar registros.
**Pendiente:** retención exacta y estrategia ante peticiones concurrentes (ver `09-ROBUSTEZ.md`).

### D-063. Rate limiting obligatorio
**Estado:** APROBADA · **Requisito académico RAC-05**

Límite en inicio de sesión y endpoints de creación, con respuesta 429 y `Retry-After`. Se aplica por usuario/tenant con respaldo por IP. La estrategia concreta (token bucket con Redis) y los valores iniciales se documentan en `09-ROBUSTEZ.md`.

### D-064. CI/CD obligatorio
**Estado:** APROBADA · **Requisito académico RAC-07**

Pipeline que instala dependencias, ejecuta lint, pruebas y build, y falla si algo está mal. Se valora construir la imagen Docker y publicarla.

### D-065. Dos estrategias de renderizado
**Estado:** APROBADA · **Requisito académico RAC-09**

La página pública usa generación estática/ISR y el panel privado usa renderizado en cliente. La justificación y el mapeo por pantalla están en `03-ARQUITECTURA.md`. La modalidad académica a declarar sigue pendiente (P-01).

### D-066. README con evidencias de sustentación
**Estado:** APROBADA · **Requisito académico RAC-08**

El `README.md` documenta nicho, arquitectura multitenant, arranque, resolución del tenant, idempotencia, rate limiting y estrategias de renderizado. Se complementa con la guía de sustentación de `12-ENTREGABLES-Y-EVALUACION.md`.

### D-067. Cuenta del cliente requerida para reservas y domicilios
**Estado:** APROBADA

Un cliente necesita una cuenta en ese restaurante (perfil `customers` del schema del tenant) para reservar una mesa o hacer un pedido a domicilio. La cuenta es del tenant, no una cuenta global con acceso a todos los restaurantes.

El visitante anónimo de mesa no necesita cuenta; puede crear una o iniciar sesión desde el QR si quiere reservar o pedir a domicilio después.

**Consecuencia:** el flujo público de reserva y domicilio exige autenticación de cliente; la disponibilidad y el menú se pueden consultar sin cuenta. Una misma identidad puede tener perfil en varios tenants sin compartir datos.

### D-068. Ciclo de vida de la mesa y liberación automática
**Estado:** APROBADA · **Completa:** D-055

Estados operativos: `available`, `occupied`, `pending_payment`, `reserved`, `inactive`.

- Abrir sesión con un QR válido → `occupied` y la mesa deja de estar disponible para reservas en tiempo real.
- El cliente pide la cuenta o el mesero inicia el cobro → `pending_payment`.
- Pago **en línea** confirmado por el proveedor mediante webhook → la mesa pasa a `available` automáticamente, sin intervención del mesero (D-073).
- Pago **en efectivo** confirmado por el mesero o cajero → la mesa pasa a `available` al registrar el pago.
- **Cancelación en efectivo** (el cliente se va sin pagar) → única liberación manual del mesero, con motivo.
- Reserva vigente → `reserved`; al sentar al cliente → `occupied`; cancelación o no-show → `available` (si no hay sesión abierta).

**La sesión no caduca por tiempo.** Termina por pago confirmado o por cancelación manual en efectivo. Volver a escanear el QR reanuda la misma sesión abierta; no crea una nueva.

**Motivo:** el estado de la mesa debe reflejar una condición real (ocupada o pagada), no un temporizador.
**Consecuencia:** la transición se ejecuta en una transacción con bloqueo; no se permite cambiar el estado a un valor arbitrario por API.

### D-069. Pedido a domicilio como canal separado
**Estado:** APROBADA

Canal `delivery` para clientes registrados del tenant. Requiere `customer_id`, dirección y teléfono; no tiene mesa ni sesión. La cocina lo recibe igual que el pedido presencial, con su propio identificador.

Estados propuestos: `confirmed → in_preparation → ready → out_for_delivery → delivered` (+ `cancelled`).

**Pendiente P-23:** costo de envío, cobertura, quién entrega y si el pago es en línea o contra entrega.

### D-070. Caja ligera con comprobante simple
**Estado:** APROBADA · **Resuelve:** P-03 y C-02

La caja registra la compra y el pago, imprime el comprobante y genera un **QR de descarga** del comprobante. No es un POS: no hay turnos, arqueo, inventario, devoluciones ni facturación fiscal. No se almacenan datos de tarjeta.

- El comprobante es un documento simple, con numeración por tenant y token de descarga; no tiene validez fiscal.
- La confirmación del pago (efectivo o en línea) libera la mesa según D-068.
- El pago en efectivo lo confirma el mesero o cajero; la cancelación en efectivo es la única liberación manual.

**Confirmación en línea:** resuelta en D-073 (webhook firmado y proveedor simulado en el MVP).

### D-071. Límites del administrador global Lixus
**Estado:** APROBADA · **Resuelve:** parte de P-05

Lixus administra la plataforma, no los restaurantes.

**Puede:**
- Ver metadatos del tenant: nombre, estado, plan y fechas.
- Verificar y activar tenants.
- Desactivar o suspender un tenant para que no siga usando el servicio.
- Gestionar planes y suscripciones.

**No puede:**
- Ver ni exportar empleados, clientes, pedidos, reservas, pagos o configuración del restaurante.
- Eliminar al CEO ni cambiar su contraseña.
- Suplantar usuarios.
- Borrar los datos del tenant al desactivarlo: toda la información se conserva.

Toda acción de Lixus queda auditada.

**Pendiente:** la matriz de permisos interna del restaurante sigue en P-05.

### D-072. Sin impuestos, propinas ni descuentos en el MVP
**Estado:** APROBADA · **Resuelve:** P-18

Los pedidos no aplican impuestos, propinas ni descuentos. El total es la suma de las líneas más, si corresponde, el costo de envío.

Los estados del pedido son los documentados en `04-MODULOS.md`; no se agregan cálculos fiscales. Si más adelante se requieren impuestos o propinas, se incorporan como configuración del tenant y se calculan en el servidor.

### D-073. Confirmación de pago en línea por webhook firmado
**Estado:** APROBADA · **Resuelve:** P-24

El MVP **no integra una pasarela real**. Se define una interfaz `PaymentProvider` con dos implementaciones:

1. **Sandbox (MVP):** una página de pago local, disponible solo en desarrollo, que al confirmar envía un **webhook firmado** a la API. No mueve dinero real.
2. **Proveedor real (producción):** adaptador para la pasarela que se elija (por ejemplo Wompi o Stripe), con el mismo contrato. La selección queda para la fase de despliegue.

Flujo de confirmación:

1. La caja o el cliente crea el pago con método `online`; queda en `pending`.
2. El cliente paga en la página del proveedor (sandbox en el MVP).
3. El proveedor envía `POST /webhooks/payments/{provider}` con `event_id`, `payment_id`, monto y estado.
4. La API verifica la firma HMAC, la marca de tiempo y el `event_id` único.
5. En una transacción, marca el pago `paid`, cierra la sesión de mesa con `payment_confirmed` y deja la mesa `available`.
6. Genera el comprobante simple para que la caja lo imprima.

**Reglas:**
- La confirmación no depende del mesero; el mesero solo interviene en efectivo o en cancelación.
- Un evento repetido no duplica el pago ni vuelve a liberar la mesa.
- No se almacenan datos de tarjeta.
- Los endpoints de sandbox se desactivan en producción.

**Motivo:** cumple el desbloqueo automático exigido sin asumir el costo y la complejidad de una pasarela real en una entrega de una semana.

---

## 14. Decisiones sustituidas y aclaradas

| Tema | Decisión vigente | Idea anterior descartada |
|---|---|---|
| Aislamiento | Schema por tenant (D-042) | Tablas compartidas con `tenant_id` como diseño del MVP |
| Stack | Next.js + FastAPI (D-043) | React + Vite; backend y frontend "por decidir" |
| Alta de restaurantes | Manual (D-014) | Registro autónomo inicial |
| Invitación de empleados | Correo pre-registrado + código (D-051) | Enlace temporal de invitación |
| Caja física | POS completo fuera del MVP; caja ligera para registro y comprobante (D-011, D-070) | POS propio |
| Pedidos | Solicitudes QR + pedido del mesero; domicilio y reserva con cuenta (D-010, D-067, D-069) | Cliente podía crear pedidos en línea sin cuenta |
| Administrador global | Sin acceso a datos operativos del restaurante (D-071) | Acceso excepcional auditado a datos del tenant |
| Impuestos | Sin impuestos, propinas ni descuentos (D-072) | Cálculo fiscal dentro del pedido |
| Página pública | Plantilla configurable (D-033) | Constructor visual libre |
| Roles | Predefinidos (D-018) | Editor general de permisos |
| IA | Groq + proveedores intercambiables (D-057, D-058) | Freebuff y Ollama como solución |
| Proveedor de pagos | Cobro automático deseado, proveedor pendiente | Wompi o Stripe como selección final |
| Almacenamiento | R2 confirmado (D-059) | Proveedor por decidir |
| Pago en línea | Webhook firmado + proveedor simulado en el MVP (D-073) | Pasarela real integrada desde el inicio |

---

## 15. Contradicciones y su estado

Las contradicciones se dejan explícitas para que no se implementen dos versiones distintas del producto. Una contradicción resuelta se conserva para no reabrirla por error.

| ID | Conflicto | Estado |
|---|---|---|
| C-01 | D-010 decía que el cliente podía realizar pedidos en línea; D-053/D-054 describen solicitudes por QR y pedidos tomados por el mesero. | Resuelta por D-010, D-067 y D-069 |
| C-02 | D-011 excluía la caja física; la conversación posterior incluye caja, pagos y comprobantes con QR. | Resuelta por D-070: caja ligera, sin POS |
| C-03 | El stack Next.js + FastAPI no encaja literalmente en la Opción A ni B del enunciado. | Pendiente P-01 |
| C-04 | D-025 admite Google para clientes; no está definido si los empleados también pueden usarlo. | Pendiente P-12 |
| C-05 | D-030 aspira a cobro automático; el MVP activa planes manualmente. | Coexistencia aceptada (D-031) |

---

## 16. Reglas para mantener este registro

1. Una propuesta no se convierte en decisión aprobada sin confirmación explícita.
2. Cuando una decisión cambia, se actualiza su estado y se conserva el motivo del cambio.
3. Toda decisión debe ser coherente con el enunciado y con el alcance del MVP.
4. Las decisiones de seguridad y aislamiento se reflejan también en los requisitos y las pruebas.
5. Las dudas no resueltas viven en `05-PENDIENTES.md`, no en este registro.
6. Los cambios importantes se anotan en `06-HISTORIAL.md`.
7. Si una decisión contradice a otra, se registra el conflicto; no se elige en silencio.

---

**Fin de `02-DECISIONES.md`.**
