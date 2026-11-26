# 01 — Requerimientos del proyecto Lixus

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Línea base para iniciar el desarrollo
**Fuentes:** `Enunciado Proyecto Integrador SaaS Multitenant.pdf` (vinculante) y conversación de requerimientos (`Preguntas de requerimientos multitenant.pdf`)
**Última actualización:** 22 de octubre de 2026

---

## 1. Propósito y jerarquía de fuentes

Este documento define **qué debe hacer** el sistema y **cómo se comprueba** que está bien hecho.

Las fuentes se usan en este orden de prioridad:

1. **El enunciado académico.** Es vinculante. Si una decisión de producto lo contradice, prevalece el enunciado o se corrige la decisión.
2. **Las decisiones aprobadas** en `02-DECISIONES.md`.
3. **Las propuestas** de la conversación, que solo son requisito cuando están marcadas como aprobadas.

La conversación aporta alcance comercial y de producto; el enunciado aporta la arquitectura mínima evaluable. Este documento mantiene ambas cosas separadas para no confundir "lo que quisiéramos construir" con "lo que se evalúa".

---

## 2. Objetivo del sistema

Lixus permite que varios restaurantes independientes (tenants) usen una misma aplicación para:

- administrar su operación (menú, personal, mesas, pedidos, reservas);
- publicar una página propia con su identidad visual;
- gestionar su plan comercial con Lixus;
- usar asistencia de inteligencia artificial con permisos acotados.

Cada restaurante ve **únicamente** sus datos. La separación se garantiza en la base de datos y en el backend, no en la interfaz.

---

## 3. Actores

| Actor | Alcance | Suscripción |
|---|---|---|
| **CEO del tenant** | Contrata el servicio, administra su restaurante, delega y gestiona al personal. | La paga (a nombre del tenant) |
| **Administrador del restaurante** | Personal con funciones delegadas por el CEO. | No paga |
| **Personal operativo** (mesero, cajero, cocinero) | Usa el panel privado según su rol. | No paga |
| **Cliente registrado** | Crea cuenta en un restaurante para reservas, comprobantes o funciones habilitadas. | No paga |
| **Cliente anónimo de mesa** | Sesión temporal abierta al escanear el QR de una mesa. | No paga ni se registra |
| **Visitante público** | Consulta páginas y menús sin cuenta. | No aplica |
| **Lixus** | Administración global de la plataforma: verificación de negocios, activación de tenants, planes, soporte auditado. | No aplica |

> **Regla de lenguaje:** "usuario" es ambiguo y no se usa como término de negocio. Se habla de CEO, personal, cliente registrado y cliente anónimo.

---

## 4. Requisitos académicos obligatorios (RAC)

Estos requisitos provienen del enunciado y **no son negociables**. Cada uno tiene evidencia exigible en la sustentación.

### RAC-01. Multitenencia con un schema por tenant

- PostgreSQL como base de datos.
- Un schema compartido (`platform`) con la información global: tenants y usuarios.
- Un schema independiente por cada tenant con las tablas de su dominio.
- Al registrarse/activarse un tenant, el sistema crea su schema y sus tablas automáticamente.
- En cada petición, el sistema identifica el tenant del usuario y opera solo sobre su schema.
- Un usuario de un tenant no puede leer ni modificar datos de otro.

**Evidencia:** dos tenants de prueba, intento de acceso cruzado rechazado, demostración en vivo de creación de schema.
**Documentos:** `03-ARQUITECTURA.md`, `07-MODELO-DATOS.md`.

### RAC-02. Autenticación y sesión

- Registro e inicio de sesión.
- Sesión mediante JWT guardado en **cookie `httpOnly`**, nunca en `localStorage`.
- Rutas protegidas en backend y frontend.
- El token permite resolver el tenant del usuario.

**Evidencia:** inspección de la cookie en el navegador, petición sin token → 401, petición con token de otro tenant → 403.

### RAC-03. Dominio de negocio

- Entre 2 y 3 entidades por tenant con CRUD completo.
- Validación de datos de entrada en el backend.
- Uso de ORM (SQLAlchemy) para el acceso a datos.

**Evidencia:** CRUD de menú/categorías/productos y pedidos.

### RAC-04. Idempotencia (obligatorio)

- Al menos **dos** operaciones de escritura idempotentes.
- Clave enviada por el cliente (`Idempotency-Key`).
- Repetir la petición con la misma clave devuelve el resultado original sin volver a ejecutar.
- Prueba: misma petición dos veces → un solo registro.
- Explicar dónde se guardan las claves y cuánto tiempo se conservan.

**Evidencia:** prueba automatizada y demostración con `curl`.
**Documento:** `09-ROBUSTEZ.md`.

### RAC-05. Rate limiting (obligatorio)

- Límite al menos en inicio de sesión y en endpoints de creación.
- Al excederse: **429** con header `Retry-After`.
- Explicar la estrategia elegida (ventana fija, deslizante o token bucket) y por qué.
- Se valora aplicar el límite por usuario o tenant, no solo por IP.

**Evidencia:** prueba que excede el límite y recibe 429 con `Retry-After`.
**Documento:** `09-ROBUSTEZ.md`.

### RAC-06. Docker

- `docker-compose.yml` que levante el proyecto con un comando.
- `.env.example` con las variables necesarias, sin secretos reales.

**Documento:** `10-ENTORNO-Y-DESPLIEGUE.md`.

### RAC-07. CI/CD

- Pipeline que instale dependencias, ejecute lint o build y falle si algo está mal.
- Se valora que ejecute pruebas y construya la imagen Docker.

**Documento:** `10-ENTORNO-Y-DESPLIEGUE.md`.

### RAC-08. Documentación

`README.md` con: nicho elegido, descripción del sistema, diagrama/descripción de la arquitectura multitenant, cómo levantar el proyecto, cómo se resuelve el tenant en cada petición, cómo se implementaron idempotencia y rate limiting y por qué.

### RAC-09. Estrategias de renderizado

- **Opción B (Next.js fullstack):** al menos dos estrategias distintas entre SSR, CSR y SSG, cada una en una pantalla donde tenga sentido, justificadas.
- **Opción A (React):** el frontend es CSR; explicar ventajas y limitaciones.

> **Pendiente crítico:** la arquitectura elegida (Next.js + FastAPI independiente) no coincide literalmente con la Opción A ni con la Opción B. Debe declararse la modalidad al docente. Ver `05-PENDIENTES.md` (P-01).

### RAC-10. Sustentación

Todo el código debe poder explicarse y modificarse en vivo (por ejemplo, cómo se crea el schema de un tenant o cómo se elige la conexión en cada petición).

**Documento:** `12-ENTREGABLES-Y-EVALUACION.md`.

---

## 5. Requisitos funcionales

### RF-01. Aprovisionamiento y activación de tenants

- Registrar un restaurante con datos de identidad del negocio y de su responsable.
- Verificar el negocio antes de activarlo; la activación inicial la realiza Lixus.
- Crear automáticamente el schema del tenant, sus tablas y su usuario CEO.
- Registrar auditoría de la creación, verificación y activación.
- No permitir operar módulos privados antes de la activación.
- Eliminar un tenant no debe ser una operación automática: requiere cancelación explícita y política de retención.

**Criterio de aceptación:** un tenant nuevo queda operativo con su schema y su CEO puede iniciar sesión.
**Pendiente:** documentos y flujo de verificación (P-04).

### RF-02. Autenticación y sesión

- Registro e inicio de sesión con correo y contraseña.
- Inicio de sesión con Google para clientes registrados (y personal, si se habilita).
- Recuperación de contraseña mediante enlace de un solo uso.
- Verificación de correo.
- Sesión con JWT en cookie `httpOnly`; cierre de sesión que invalida la cookie.
- Bloqueo de rutas privadas sin sesión válida.

**Criterio de aceptación:** un empleado desactivado no puede volver a entrar con su token anterior.

### RF-03. Acceso multi-tenant y cambio de restaurante

- Una identidad puede tener acceso a varios tenants con permisos distintos.
- El acceso se valida contra una relación de acceso por tenant (membresía técnica).
- Cambiar de tenant emite un token nuevo; no se reutiliza el contexto anterior.
- Sin relación de acceso válida, un usuario no puede invocar rutas de ese tenant aunque conozca su identificador.

**Criterio de aceptación:** un usuario de A no puede operar en B alterando la URL, el body o un header de tenant.

### RF-04. Personal, perfiles y roles

- El CEO crea empleados y les asigna un rol predefinido.
- El empleado con correo previamente registrado se verifica con un código en su primer acceso.
- El CEO puede delegar funciones administrativas.
- El rol de cliente es predeterminado y **no** puede asignarse manualmente como si fuera un empleado.
- Desactivar un empleado revoca sus sesiones y conserva su historial.
- Roles del MVP: CEO/propietario, administrador, mesero, cajero, cocinero. Rol global: Lixus.

**Pendiente:** matriz definitiva de permisos (P-05).

### RF-05. Menú y categorías

- CRUD de categorías y productos.
- Campos estándar: nombre, descripción, precio, imagen, disponibilidad, publicación.
- Ordenar productos dentro del menú.
- Impedir operar productos de otro tenant.
- El menú público muestra solo lo publicado y disponible.

**Criterio de aceptación:** CRUD completo con validación de precio, nombre y categoría.

### RF-06. Mesas y sesiones QR

- CRUD de mesas con código/número, zona y estado operativo.
- Generar un QR por mesa con un token opaco que identifica la mesa.
- El cliente escanea y obtiene botones de solicitud: queja, falta algo, quiero algo, pedir la cuenta.
- Puede registrarse o iniciar sesión desde la sesión QR, sin que sea obligatorio.
- El mesero recibe la solicitud con número de mesa, hora y estado.
- El mesero puede actualizar el estado de la mesa: disponible, ocupada, pendiente de pago, reservada, inactiva.
- Al confirmar el pago (en línea o efectivo), la mesa pasa a disponible; el mesero solo la libera manualmente si el cliente cancela en efectivo.
- Una mesa solo puede tener una sesión activa.
- Un QR antiguo no reabre una sesión cerrada; inicia una nueva si la mesa está libre.

**Regla de cierre:** la sesión no caduca por tiempo; termina por pago confirmado o cancelación en efectivo (D-068).

### RF-07. Pedidos

- El mesero registra el pedido presencial asociado a una mesa y su sesión.
- Líneas con producto, cantidad, precio congelado y notas.
- Estados operativos y de pago independientes.
- La cocina recibe el pedido con el ID de mesa y actualiza la preparación.
- Los clientes registrados pueden crear pedidos a domicilio con dirección y teléfono, sin mesa.
- Consulta y actualización según rol.
- Trazabilidad de cambios de estado.
- El total se calcula en el servidor.

**Criterio de aceptación:** los pedidos de mesa y de domicilio no se mezclan; el total y los precios se calculan y verifican en el servidor.

### RF-08. Reservas

- Solo un cliente con cuenta en ese restaurante puede reservar.
- La reserva incluye fecha, hora, duración, número de personas y mesa.
- Estados: solicitada, confirmada, atendida, completada, cancelada, no presentada.
- Evitar solapamientos sobre la misma mesa.
- El personal puede gestionar reservas según su rol.
- La disponibilidad puede consultarse sin cuenta; reservar exige iniciar sesión.

**Pendiente:** tolerancia y política de no-show (P-07).

### RF-09. Caja ligera, pagos y comprobantes

- La caja registra la compra y el pago (efectivo o en línea), imprime el comprobante y genera un QR de descarga.
- El comprobante es simple, con numeración por tenant y token temporal; no tiene validez fiscal.
- No se almacenan datos de tarjeta ni se opera un POS con turnos, arqueo o inventario.
- La confirmación del pago libera la mesa (D-068).
- El pago en línea se confirma mediante un **webhook firmado** del proveedor; en el MVP el proveedor es simulado (D-073).
- Enviar el comprobante por correo cuando el cliente lo solicite.
- Ofrecer al cliente la creación de su cuenta en el restaurante.

> El webhook usa firma HMAC y `event_id` único. La pasarela real queda para producción. Nada de esto es obligatorio para el enunciado.

### RF-10. Página pública y personalización

- Una plantilla configurable con secciones: hero, menú, información, galería, contacto y horarios.
- Edición de logo, colores, textos, imagen principal y visibilidad de secciones.
- Publicación y despublicación.
- El contenido de un restaurante no puede mezclarse con el de otro.

**Pendiente:** URL/subdominio y reordenamiento de secciones (P-06).

### RF-11. Suscripciones y planes

- Planes Básico, Intermedio y Avanzado definidos como capacidades y cuotas configurables.
- Activación manual por Lixus en la primera etapa.
- Límites combinados: funcionalidades, personal, almacenamiento y consumo de IA.
- Al vencer: se conservan los datos, se restringen funciones premium y se permite renovar.

**Pendiente:** matriz de planes y precios (P-09).

### RF-12. Inteligencia artificial

- Generar y mejorar descripciones de productos y del restaurante.
- Asistir en la configuración inicial.
- Responder consultas sobre datos a los que el usuario ya tiene acceso.
- Registrar consumo por tenant (proveedor, modelo, tokens, latencia).
- Toda escritura se ejecuta mediante herramientas del backend con validación de permisos.

**Criterio de aceptación:** una consulta de IA nunca devuelve datos de otro tenant, incluso con un prompt malicioso.

### RF-13. Auditoría

- Registrar acciones administrativas: activación de tenants, cambios de roles, accesos de Lixus, cambios de plan, acciones de IA que escriben datos.
- Los registros no contienen contraseñas, tokens ni datos sensibles innecesarios.

### RF-14. Perfil del cliente registrado

- Consultar sus reservas y comprobantes dentro del restaurante.
- Sus datos no se comparten con otros tenants.
- Puede eliminar su cuenta según la política de retención (pendiente).

---

## 6. Requisitos no funcionales

| ID | Requisito |
|---|---|
| RNF-01 | **Aislamiento:** ninguna consulta puede ejecutarse contra el schema de otro tenant; se aplica en backend y base de datos. |
| RNF-02 | **Autorización:** cada operación privada verifica identidad, membresía y permiso en el servidor. |
| RNF-03 | **Validación:** todo dato de entrada se valida y normaliza en el backend; nunca se confía en precios, roles ni identificadores enviados por el cliente. |
| RNF-04 | **Sesiones:** expiración, revocación y cookies `httpOnly`, `Secure` en producción y `SameSite` adecuado. |
| RNF-05 | **Robustez:** idempotencia en escrituras críticas y rate limiting en autenticación y creación. |
| RNF-06 | **Reproducibilidad:** entorno local con Docker Compose, variables en `.env.example` y migraciones versionadas. |
| RNF-07 | **Auditoría y observabilidad:** logs estructurados, eventos de auditoría y errores sin filtrar secretos. |
| RNF-08 | **Rendimiento:** respuestas del panel por debajo de 500 ms en entorno local con datos de prueba; consultas indexadas por claves de búsqueda. |
| RNF-09 | **Mantenibilidad:** monolito modular, linting, tipado y pruebas automatizadas en CI. |
| RNF-10 | **Privacidad:** no se comparten datos personales entre tenants ni se expone la cartera de clientes de la plataforma. |
| RNF-11 | **Archivos:** validación de tipo y tamaño en servidor, almacenamiento privado y acceso mediante URL firmada. |
| RNF-12 | **SEO y accesibilidad de la página pública:** HTML renderizado en servidor/estático, metadatos por restaurante y contraste legible. |

---

## 7. Reglas de negocio

| ID | Regla |
|---|---|
| RN-01 | Cada restaurante es un tenant independiente; su información vive en su propio schema. |
| RN-02 | La suscripción pertenece al tenant. El personal y los clientes no pagan licencia. |
| RN-03 | Un tenant no conoce ni puede descubrir qué otros restaurantes usan la plataforma. |
| RN-04 | Consultar la página pública y el menú no requiere cuenta ni autorización. |
| RN-05 | Acceder al panel privado exige una relación de acceso activa con ese tenant. |
| RN-06 | Los permisos se otorgan por tenant y no se heredan entre restaurantes. |
| RN-07 | El rol de cliente es predeterminado; el CEO no puede asignarlo como si fuera personal. |
| RN-08 | Un empleado con correo pre-registrado se verifica con un código de un solo uso en su primer acceso. |
| RN-09 | Los pedidos presenciales se registran por mesa y no requieren datos personales del cliente. |
| RN-10 | Los datos personales del cliente se solicitan solo cuando la operación lo exige (reserva, comprobante por correo, cuenta). |
| RN-11 | Una mesa tiene una sola sesión anónima activa; al cerrarla se reinicia para el siguiente cliente. |
| RN-12 | Los precios y nombres de productos se congelan en la línea del pedido al confirmarlo. |
| RN-13 | La caja registra el pago y emite un comprobante simple; no procesa dinero ni emite documentos fiscales (D-070). |
| RN-14 | Si el plan vence, los datos se conservan y solo se restringen funciones premium. |
| RN-15 | La IA usa los permisos del usuario que la invoca y nunca actúa como administrador. |
| RN-16 | Las acciones de Lixus sobre datos de un tenant deben ser limitadas, justificadas y auditadas. |
| RN-17 | Los registros históricos de pedidos y pagos no se eliminan al desactivar usuarios o mesas. |
| RN-18 | Un mismo correo puede existir en tenants distintos sin conflicto; no implica compartir datos. |
| RN-19 | Para reservar una mesa o pedir a domicilio se requiere una cuenta en ese restaurante. |
| RN-20 | El pedido presencial lo crea el mesero; el cliente anónimo solo envía solicitudes. |
| RN-21 | La mesa se libera al confirmar el pago (en línea o efectivo); la única liberación manual es la cancelación en efectivo (D-068). |
| RN-22 | La cocina recibe el ID de mesa y el detalle del pedido, no los datos personales del cliente. |

---

## 8. Fuera de alcance de la primera versión

- Procesamiento real de pagos con pasarela (fuera del MVP; D-073 usa proveedor simulado) y facturación fiscal.
- POS completo: turnos de caja, arqueo, inventario y devoluciones.
- Cobro automático de suscripciones (la activación es manual).
- Inventario y control de stock.
- Constructor visual libre de páginas y campos personalizados configurables.
- Múltiples plantillas públicas para elegir.
- Aplicación móvil nativa.
- Directorio público de restaurantes clientes.
- Gestión de reparto propio y logística de domicilios.
- Microservicios, base de datos por tenant y multi-región.

> Excluir algo del MVP no lo elimina de la visión del producto; queda en `05-PENDIENTES.md` como evolución.

---

## 9. Criterios de aceptación globales

La entrega se considera aceptada cuando:

- [ ] `docker compose up` levanta frontend, API, PostgreSQL y Redis sin pasos manuales ocultos.
- [ ] Un tenant nuevo se crea con su schema y sus tablas desde la aplicación.
- [ ] Dos tenants de prueba mantienen sus datos aislados, incluso con intentos de acceso cruzado.
- [ ] La sesión se guarda en cookie `httpOnly` y las rutas privadas están protegidas.
- [ ] El CRUD de menú y pedidos funciona con validación en el servidor.
- [ ] Dos escrituras son idempotentes y la prueba demuestra un solo registro.
- [ ] El login y la creación de pedidos aplican rate limiting con 429 y `Retry-After`.
- [ ] El pipeline de CI falla ante lint, test o build incorrectos.
- [ ] El `README.md` responde los cinco puntos del enunciado.
- [ ] Un cliente anónimo envía solicitudes por QR sin crear cuenta.
- [ ] Un cliente registrado reserva una mesa y crea un pedido a domicilio.
- [ ] Al confirmar el pago, la mesa queda disponible automáticamente.
- [ ] La caja registra un pago, imprime el comprobante y el QR de descarga funciona.
- [ ] Un webhook firmado marca el pago como pagado y libera la mesa sin intervención del mesero.
- [ ] La página pública y el panel usan al menos dos estrategias de renderizado justificadas.

---

## 10. Trazabilidad

| Requisito | Decisión asociada | Documento de diseño |
|---|---|---|
| RAC-01 / RF-01 | D-042, D-045 | `03-ARQUITECTURA.md`, `07-MODELO-DATOS.md` |
| RAC-02 / RF-02 | D-061 | `08-SEGURIDAD-Y-ACCESO.md` |
| RAC-03 / RF-05, RF-07 | D-043 | `04-MODULOS.md`, `07-MODELO-DATOS.md` |
| RAC-04 | D-062 | `09-ROBUSTEZ.md` |
| RAC-05 | D-063 | `09-ROBUSTEZ.md` |
| RAC-06, RAC-07 | D-064 | `10-ENTORNO-Y-DESPLIEGUE.md` |
| RAC-08, RAC-09 | D-065, D-066 | `12-ENTREGABLES-Y-EVALUACION.md` |
| RF-06, RF-07 | D-053, D-054, D-055, D-068, D-069 | `04-MODULOS.md` |
| RF-08 | D-067, D-068 | `04-MODULOS.md`, `07-MODELO-DATOS.md` |
| RF-09 | D-070, D-073 | `04-MODULOS.md`, `09-ROBUSTEZ.md` |
| RF-12 | D-056, D-057, D-058 | `04-MODULOS.md`, `08-SEGURIDAD-Y-ACCESO.md` |

---

**Fin de `01-REQUERIMIENTOS.md`.**
