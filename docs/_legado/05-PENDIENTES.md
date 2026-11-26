# 05 — Pendientes, contradicciones y riesgos abiertos

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Registro vivo
**Última actualización:** 22 de octubre de 2026

---

## 1. Cómo se usa

Aquí viven **solo** los asuntos sin resolver. Lo aprobado está en `02-DECISIONES.md` y no se reabre sin motivo.

Cada pendiente indica:

- **Impacto:** qué se bloquea si no se decide.
- **Recomendación:** la opción sugerida, que **no** es una decisión hasta que se confirme.
- **Bloquea:** si impide empezar a programar esa parte.

Prioridad: **Alta** (bloquea el MVP o la entrega), **Media** (afecta calidad o alcance), **Baja** (evolución).

---

## 2. Tabla resumen

| ID | Tema | Prioridad | Bloquea |
|---|---|---|---|
| P-01 | Modalidad académica a declarar (A/B) | Alta | CIERRE |
| P-04 | Verificación empresarial | Media | Activación de tenants |
| P-05 | Matriz interna de permisos del restaurante | Alta | Personal y autorización |
| P-06 | URL pública y alcance de personalización | Media | Página pública |
| P-07 | Recurso reservable y solapamientos | Media | Reservas |
| P-09 | Planes, precios y pasarela | Baja | Suscripciones |
| P-10 | Vencimiento, gracia y reactivación | Media | Suscripciones |
| P-11 | Proveedor de correo transaccional | Alta | Invitaciones y recuperación |
| P-12 | Google para empleados | Baja | Autenticación |
| P-13 | Retención de auditoría y datos personales | Media | Cumplimiento |
| P-14 | Arquitectura de despliegue en AWS | Media | Producción |
| P-15 | Antivirus de archivos | Baja | Archivos |
| P-16 | Contraseñas de Lixus y rotación de secretos | Media | Seguridad |
| P-17 | Cabeceras CSP y hardening del frontend | Media | Seguridad |
| P-19 | Cuotas numéricas de almacenamiento e IA | Media | Planes/IA |
| P-20 | Multi-sucursal por tenant | Baja | Evolución |
| P-21 | Automatización con n8n | Baja | Opcional |
| P-22 | Multiplicidad de plantillas públicas | Baja | Evolución |
| P-23 | Domicilios: cobertura, costo y entrega | Media | Domicilios |

---

## 3. Detalle por pendiente

### P-01. Modalidad académica a declarar (Opción A u Opción B)
**Prioridad:** Alta · **Bloquea:** cierre de la entrega

El enunciado ofrece dos modalidades:

- **A:** backend independiente en el lenguaje elegido + frontend React.
- **B:** Next.js fullstack, API y frontend en el mismo proyecto.

El stack aprobado (Next.js + FastAPI independiente) combina ambas: es un frontend React/Next con un backend separado. La evaluación de renderizado depende de la modalidad declarada.

**Opciones**
1. Declarar **Opción A** y presentar Next.js como frontend React; explicar que el SSR/SSG de las páginas públicas es una mejora sobre el CSR mínimo exigido.
2. Declarar **Opción B** y asumir que la API de Next.js también exista, aunque la lógica principal esté en FastAPI. Es más difícil de defender y duplica capas.
3. Consultar al docente si un stack híbrido es aceptable.

**Recomendación:** Opción A, declarada por escrito al docente, con justificación de Next.js como framework React y del backend Python independiente. Confirmar antes de la sustentación.

---

### P-02. Canal de pedidos del cliente final — **RESUELTO**
**Cierre:** 22 de octubre de 2026 · **Decisiones:** D-010, D-067, D-069

Se definió el modelo definitivo:

- **Cliente anónimo en mesa:** escanea el QR, envía solicitudes al mesero y puede registrarse o iniciar sesión desde ahí. No crea pedidos.
- **Cliente con cuenta en el restaurante:** puede reservar una mesa y pedir a domicilio.
- **Mesero:** registra el pedido presencial por mesa; cocina lo recibe con el ID de mesa.

El QR identifica la mesa y comunica al cliente con el mesero; no es un canal de autopedido. La alternativa de carrito en línea para el cliente físico queda descartada para el MVP.

---

### P-03. Caja, pagos y comprobantes — **RESUELTO**
**Cierre:** 22 de octubre de 2026 · **Decisión:** D-070

Se elige **caja ligera**: registra la compra y el pago, imprime el comprobante y genera un QR de descarga. No hay POS, turnos, arqueo, inventario ni facturación fiscal. No se almacenan datos de tarjeta.

El **pago en línea** se resolvió con webhook firmado y proveedor simulado (D-073). Esto no afecta a la suscripción SaaS, que es un flujo distinto (D-012).

---

### P-04. Verificación empresarial
**Prioridad:** Media · **Bloquea:** activación de tenants

Falta definir: documentos aceptados (RUT, cámara de comercio, identificación), quién revisa, plazos, motivos de rechazo y apelación. También si el correo debe ser de dominio corporativo y cómo se comprueba.

**Recomendación:** para el MVP, revisión manual por Lixus con un formulario y un campo de motivo. No bloquear el desarrollo: el estado `pending_verification` ya existe.

---

### P-05. Matriz interna de permisos del restaurante
**Prioridad:** Alta · **Bloquea:** autorización

**Resuelto parcialmente (D-071):** el administrador global **Lixus** no accede a datos operativos del restaurante, no elimina CEOs, no cambia contraseñas y no borra datos al desactivar. Solo administra la plataforma.

Queda definir la matriz **interna** de cada restaurante: qué puede el administrador delegado, el mesero, el cajero y el cocinero; quién edita el menú, quién cierra pedidos, quién ve datos de clientes y si el admin puede gestionar personal.

**Recomendación:** aprobar el borrador de `04-MODULOS.md` con estos ajustes: el admin gestiona menú, personal y operación, pero no el plan ni al CEO; el mesero gestiona mesas, pedidos y reservas; el cajero registra pagos, confirma y emite comprobantes; el cocinero solo cambia estados de preparación y no ve datos personales.

---

### P-06. URL pública y alcance de personalización
**Prioridad:** Media · **Bloquea:** página pública

**Opciones**
1. `midominio.com/r/{slug}` (más simple, un dominio, sin comodines).
2. `{slug}.midominio.com` (más profesional, requiere DNS comodín y certificado comodín).
3. Dominio personalizado por restaurante (fuera del MVP).

También queda abierto si el propietario podrá reordenar secciones.

**Recomendación:** opción 1 para el MVP, con el `slug` ya modelado; migrar a subdominios después no cambia el modelo de datos. Reordenar secciones: no en el MVP.

---

### P-07. Recurso reservable y solapamientos
**Prioridad:** Media · **Bloquea:** reservas

La reserva ocupa una **mesa concreta** (confirmado en P-02). Falta definir duración mínima, tolerancia, zona horaria y política de no-show.

**Recomendación:** aplicar la restricción de exclusión de `09-ROBUSTEZ.md` sobre `table_id` y franja; tolerancia de 15 minutos y no-show manual.

---

### P-08. Ciclo de la sesión QR — **RESUELTO**
**Cierre:** 22 de octubre de 2026 · **Decisión:** D-068

La sesión **no caduca por tiempo**: es una condición. Al iniciar el servicio, la mesa se bloquea para reservas en tiempo real. Se libera cuando:

- se confirma un pago en línea: automáticamente, sin intervención del mesero; o
- se confirma un pago en efectivo: al registrarlo; o
- el cliente cancela en efectivo: el mesero la libera manualmente con motivo.

Volver a escanear el QR reanuda la sesión abierta; no crea otra. Si la mesa está libre, inicia una nueva.

---

### P-09. Planes, precios y pasarela
**Prioridad:** Baja · **Bloquea:** suscripciones

Faltan capacidades por plan, precios, moneda y proveedor de cobro recurrente (Wompi, Stripe Billing u otro).

**Recomendación:** no inventar precios. Definir primero el catálogo de capacidades; en el MVP, activación manual y sin pasarela. Seleccionar pasarela solo cuando exista un caso de negocio real.

---

### P-10. Vencimiento, gracia y reactivación
**Prioridad:** Media · **Bloquea:** suscripciones

Falta definir el periodo de gracia, los avisos, qué funciones se bloquean, cuánto se conservan los datos y cómo se reactiva.

**Recomendación:** 7 días de gracia con avisos por correo; bloqueo de escrituras premium y conservación total de datos; reactivación inmediata al registrar el pago.

---

### P-11. Proveedor de correo transaccional
**Prioridad:** Alta · **Bloquea:** invitaciones, códigos y recuperación

Se necesita un proveedor para códigos de activación, recuperación de contraseña, comprobantes y avisos de suscripción. En local se usa Mailpit.

**Recomendación:** elegir un proveedor con capa gratuita y API estable; abstraer el envío detrás de una interfaz para poder cambiar. No hardcodear el proveedor.

---

### P-12. Google para empleados
**Prioridad:** Baja · **Bloquea:** nada

**Conflicto C-04.** Está aprobado Google para clientes. Para empleados no se definió. Si se permite, hay que decidir cómo se vincula la identidad con la membresía pre-registrada.

**Recomendación:** no habilitarlo para empleados en el MVP; el flujo por código es suficiente y más fácil de auditar. Reevaluar después.

---

### P-13. Retención de auditoría y datos personales
**Prioridad:** Media · **Bloquea:** cumplimiento

Definir cuánto tiempo se conservan auditoría, datos de clientes, comprobantes y sesiones; cómo se exportan o eliminan datos de un tenant; y qué pasa al cancelar una cuenta.

**Recomendación:** auditoría 12 meses, datos operativos mientras el tenant esté activo, exportación en CSV/JSON bajo solicitud, eliminación con periodo de gracia. No es requisito académico, pero debe quedar escrito.

---

### P-14. Arquitectura de despliegue en AWS
**Prioridad:** Media · **Bloquea:** producción

Falta decidir cómputo (ECS, EC2, VPS), base de datos (RDS o contenedor), red, secretos, CDN, respaldos y presupuesto.

**Recomendación:** para la entrega, local con Docker; si se busca el punto adicional, un VPS con Docker Compose y HTTPS, que es más barato y explicable. AWS queda como evolución documentada.

---

### P-15. Antivirus de archivos
**Prioridad:** Baja · **Bloquea:** nada del MVP

Validar tipo y tamaño no detecta malware incrustado. Un escaneo requiere servicio externo (ClamAV o similar).

**Recomendación:** re-codificar imágenes y aceptar solo formatos raster; dejar el escaneo documentado como mejora.

---

### P-16. Contraseñas de Lixus y rotación de secretos
**Prioridad:** Media · **Bloquea:** seguridad de plataforma

Definir política de contraseña (mínimo 16), MFA obligatorio, rotación de `JWT_SECRET` sin cerrar sesiones masivamente y procedimiento ante filtración.

**Recomendación:** MFA TOTP obligatorio en producción, `JWT_SECRET` rotativo con periodo de gracia de 24 h para tokens antiguos.

---

### P-17. Cabeceras CSP y hardening
**Prioridad:** Media · **Bloquea:** nada

Definir CSP, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` y política de imágenes externas.

**Recomendación:** CSP estricta con nonce en Next.js; permitir imágenes solo desde el CDN propio. Probar que no rompa la página pública.

---

### P-18. Impuestos, propinas y descuentos — **RESUELTO**
**Cierre:** 22 de octubre de 2026 · **Decisión:** D-072

No se aplican impuestos, propinas ni descuentos en el MVP. El total es la suma de las líneas más, si corresponde, el costo de envío. Los estados del pedido son los documentados en `04-MODULOS.md`; los estados de domicilio (`out_for_delivery`, `delivered`) se validan con P-23.

---

### P-19. Cuotas numéricas de almacenamiento e IA
**Prioridad:** Media · **Bloquea:** planes e IA

Faltan cifras: MB por imagen, archivos por tenant, GB totales y límite diario/mensual de tokens de IA.

**Recomendación:** partir conservador (5 MB por imagen, 200 imágenes, 10 GB totales, 200 k tokens/día por tenant) y ajustar con medición real. Guardar los valores en configuración, no en el código.

---

### P-20. Multi-sucursal por tenant
**Prioridad:** Baja · **Bloquea:** nada

No se definió si un restaurante puede tener varias sucursales. Afecta mesas, menú, personal y reportes.

**Recomendación:** un tenant = un local en el MVP. Documentar que una cadena requeriría tenants separados o una entidad `branches` en el futuro.

---

### P-21. Automatización con n8n
**Prioridad:** Baja · **Bloquea:** nada

Punto adicional del enunciado: enviar un correo al crear un tenant, notificar eventos o generar reportes. Implica webhooks, reintentos e idempotencia del consumidor.

**Recomendación:** implementarlo solo si los requisitos obligatorios están completos y probados. Un webhook firmado con reintentos y log es suficiente para demostrarlo.

---

### P-22. Multiplicidad de plantillas públicas
**Prioridad:** Baja · **Bloquea:** nada

El MVP usa una plantilla configurable. Añadir más implica un selector y variantes de componentes.

**Recomendación:** no implementarlo ahora; dejar la configuración desacoplada del componente para permitirlo después.

---

### P-23. Domicilios: cobertura, costo y entrega
**Prioridad:** Media · **Bloquea:** módulo de domicilios

El canal `delivery` está aprobado, pero faltan sus reglas operativas: zonas de cobertura, costo de envío (fijo o por zona), quién entrega (personal o tercero), estados de entrega, pago contra entrega o en línea, y qué pasa si el cliente no recibe.

**Recomendación:** dirección y teléfono obligatorios; tarifa fija configurable por tenant; estados `ready → out_for_delivery → delivered`; sin gestión de flota (el restaurante entrega con su propio personal); pago registrado, no procesado en el restaurante (D-073).

---

### P-24. Confirmación del pago en línea — **RESUELTO**
**Cierre:** 22 de octubre de 2026 · **Decisión:** D-073

Se definió explicitamente cómo se confirma el pago en línea dentro del MVP:

- **No** es una pasarela real que mueva dinero por el proyecto.
- **No** es un registro manual en caja por parte del mesero.
- **Sí** es un webhook firmado que proviene de un **proveedor simulado (sandbox)**: un flujo de pago local de desarrollo que, al confirmar, envía un evento firmado a la API.

La API valida la firma HMAC, la marca de tiempo y el `event_id` único, marca el pago `paid`, cierra la sesión de mesa con `payment_confirmed` y deja la mesa `available`, todo sin que el mesero intervenga. Si luego se elige una pasarela real para producción, se adapta por detrás de la misma interfaz `PaymentProvider`; la entrega académica no la integra y no almacena datos de tarjeta.

---

## 4. Riesgos técnicos que deben validarse antes de programar

| ID | Riesgo | Validación | Documento |
|---|---|---|---|
| RT-01 | El ORM no maneja bien schemas dinámicos y migraciones | PoC con dos schemas y una migración nueva | `03-ARQUITECTURA.md` |
| RT-02 | El pool de conexiones filtra el `search_path` | Prueba concurrente A/B | `03-ARQUITECTURA.md` |
| RT-03 | Aislamiento solo en frontend | Pruebas IDOR automatizadas | `08-SEGURIDAD-Y-ACCESO.md` |
| RT-04 | Reservas con doble reserva por carrera | Restricción de exclusión + prueba concurrente | `09-ROBUSTEZ.md` |
| RT-05 | Duplicados por reintentos | Prueba de idempotencia | `09-ROBUSTEZ.md` |
| RT-06 | IA devuelve datos de otro tenant | Pruebas de inyección de prompt | `08-SEGURIDAD-Y-ACCESO.md` |
| RT-07 | Redis caído deja el sistema sin límites | Prueba de degradación controlada | `09-ROBUSTEZ.md` |
| RT-08 | Alcance excesivo para una semana | Congelar módulos y priorizar CRUD + robustez | `11-PLAN-DE-IMPLEMENTACION.md` |

---

## 5. Decisiones que NO están pendientes

Para evitar reabrir lo ya resuelto:

- El aislamiento es **schema por tenant** (D-042). No se reevalúa salvo fallo de la PoC.
- El stack es **Next.js + FastAPI + PostgreSQL + SQLAlchemy + Alembic + Redis + R2** (D-043).
- La sesión va en **cookie httpOnly** (D-061).
- El alta de tenants es **manual** (D-014).
- No hay **directorio de restaurantes clientes** (D-049).
- Freebuff **no** es proveedor de IA del producto (D-056).
- La IA **no** escribe directamente en la base de datos (D-038).
- El cliente anónimo **no crea pedidos**: solo envía solicitudes por QR (D-010).
- Reservar y pedir a domicilio exige **cuenta en ese restaurante** (D-067).
- La mesa se libera **automáticamente al confirmar el pago** (D-068).
- El pedido presencial lo registra el **mesero**, no el cliente (D-010).
- La caja es **ligera**: registra pago, imprime comprobante y ofrece QR de descarga; no es un POS (D-070).
- **Lixus no accede** a datos operativos del restaurante ni borra información al desactivar (D-071).
- **No se aplican** impuestos, propinas ni descuentos (D-072).
- El pago en línea se confirma por **webhook firmado** con proveedor simulado; no hay pasarela real en el MVP (D-073).

---

**Fin de `05-PENDIENTES.md`.**
