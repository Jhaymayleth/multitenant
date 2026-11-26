# 04 — Módulos funcionales y reglas de negocio

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Línea base para implementación; la matriz de permisos es un borrador para aprobación
**Última actualización:** 22 de octubre de 2026

---

## 1. Cómo usar este documento

Cada módulo describe: propósito, entidades, operaciones, reglas y criterios de aceptación. Las rutas de API son una propuesta de contrato; el prefijo base es `/api/v1`.

Convención de permisos:

| Símbolo | Significado |
|---|---|
| ✔ | Permitido |
| ◐ | Permitido con restricción indicada |
| — | Denegado |

---

## 2. Matriz de permisos (borrador)

| Capacidad | CEO | Admin | Mesero | Cajero | Cocinero | Lixus |
|---|---|---|---|---|---|---|
| Configurar el restaurante | ✔ | ◐ delegado | — | — | — | — |
| Gestionar plan y suscripción | ✔ | — | — | — | — | ◐ activar |
| Gestionar personal y roles | ✔ | ◐ sin el rol CEO | — | — | — | — |
| Ver personal | ✔ | ✔ | — | — | — | — |
| CRUD categorías y productos | ✔ | ✔ | ◐ solo lectura | ◐ solo lectura | ◐ solo lectura | — |
| Publicar página pública | ✔ | ◐ delegado | — | — | — | — |
| CRUD mesas y QR | ✔ | ✔ | ◐ generar QR | — | — | — |
| Abrir / cerrar sesión de mesa | ✔ | ✔ | ✔ | ◐ cobro | — | — |
| Atender solicitudes de mesa | ✔ | ✔ | ✔ | ◐ cobro | — | — |
| Crear y editar pedidos | ✔ | ✔ | ✔ | ◐ cobro | — | — |
| Cambiar estado de preparación | ✔ | ✔ | ◐ | — | ✔ | — |
| Registrar pago | ✔ | ✔ | — | ✔ | — | — |
| Emitir comprobante | ✔ | ✔ | — | ✔ | — | — |
| CRUD reservas | ✔ | ✔ | ✔ | ◐ cobro | — | — |
| Ver datos de clientes | ✔ | ✔ | ◐ solo de su mesa | ◐ comprobante | — | — |
| Usar asistentes de IA | ✔ | ✔ | ◐ según plan | ◐ según plan | — | — |
| Crear / verificar tenants | — | — | — | — | — | ✔ |
| Acceder a datos de un tenant | — | — | — | — | — | — |
| Ver auditoría | ◐ de su tenant | — | — | — | — | ◐ solo eventos de plataforma |

**Pendiente P-05:** aprobar esta matriz y traducirla a permisos atómicos en el backend.

> **Clientes:** no forman parte de esta matriz de personal. Un cliente registrado solo puede reservar y pedir a domicilio en el restaurante donde tiene cuenta; un cliente anónimo solo envía solicitudes por QR.
>
> **Lixus:** no accede a datos operativos del restaurante. Solo ve metadatos del tenant, verifica, activa, desactiva y gestiona planes; no elimina CEOs ni cambia contraseñas (D-071).

---

## 3. Módulo: plataforma y tenants

**Propósito:** crear y administrar los espacios de restaurante sin exponer datos internos.

**Entidades:** `tenants`, `tenant_verifications`, `plans`, `subscriptions`, `subscription_invoices`.

**Operaciones (Lixus)**

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/platform/tenants` | Crear tenant + schema (idempotente) |
| GET | `/platform/tenants` | Listar con filtros de estado |
| GET | `/platform/tenants/{id}` | Detalle y estado de aprovisionamiento |
| POST | `/platform/tenants/{id}/verify` | Aprobar o rechazar verificación |
| POST | `/platform/tenants/{id}/activate` | Activar cuenta y plan inicial |
| POST | `/platform/tenants/{id}/suspend` | Suspender por impago o incidente |
| PATCH | `/platform/subscriptions/{id}` | Cambiar plan o vigencia |
| GET | `/platform/audit` | Consultar auditoría |

**Reglas**

1. El schema se genera en servidor; el cliente no propone nombres.
2. La creación es idempotente mediante `Idempotency-Key`.
3. La verificación y la activación son pasos separados y auditados.
4. Suspender un tenant no borra sus datos.
5. Lixus no navega datos de negocio sin motivo registrado.
6. El correo del responsable es comercial y debe verificarse.

**Criterios de aceptación**

- Crear un tenant produce schema, tablas y usuario CEO utilizable.
- Reintentar la creación con la misma clave devuelve el mismo tenant.
- Un tenant sin verificar no puede operar módulos privados.

---

## 4. Módulo: identidad y sesión

**Propósito:** autenticar personas y emitir una sesión segura.

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/auth/register` | Registro de cliente en un tenant |
| POST | `/auth/login` | Inicio de sesión (rate limited) |
| POST | `/auth/logout` | Cierre de sesión |
| POST | `/auth/refresh` | Renovación de sesión |
| POST | `/auth/verify-code` | Código de activación de empleado |
| POST | `/auth/forgot-password` | Solicitud de recuperación |
| POST | `/auth/reset-password` | Cambio con enlace de un solo uso |
| GET | `/auth/me` | Identidad, tenant activo y permisos |
| POST | `/auth/switch-tenant` | Cambiar de restaurante y emitir token nuevo |

**Reglas**

1. Contraseña con Argon2id; mínimo 12 caracteres.
2. JWT en cookie `httpOnly`; nunca en `localStorage`.
3. El token contiene `sub`, `tenant_id`, `role`, `jti`, `iat`, `exp`, `iss`, `aud`.
4. Cada petición revalida membresía y estado del usuario.
5. Cambiar de tenant exige membresía activa y emite un token nuevo.
6. Un usuario desactivado no puede refrescar la sesión.
7. El login falla con mensaje genérico, sin revelar si el correo existe.
8. Google identifica, pero no concede acceso a ningún tenant.

**Criterios de aceptación**

- La cookie no es legible desde JavaScript.
- Un token de un tenant no sirve para otro.
- El código de activación caduca y tiene límite de intentos.

---

## 5. Módulo: personal y permisos

**Propósito:** administrar quién trabaja en el restaurante y qué puede hacer.

**Entidades:** `platform.users`, `platform.tenant_memberships`, `staff_profiles`, `verification_codes`.

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/staff` | Listar personal |
| POST | `/tenant/staff` | Pre-registrar empleado con correo y rol |
| PATCH | `/tenant/staff/{id}` | Editar perfil o rol |
| POST | `/tenant/staff/{id}/disable` | Desactivar y revocar sesiones |
| POST | `/tenant/staff/{id}/resend-code` | Reenviar código de activación |

**Reglas**

1. Solo el CEO y el admin delegado gestionan personal.
2. El rol `owner` no se asigna desde la interfaz.
3. El rol de cliente no se asigna como si fuera personal.
4. El correo pre-registrado debe coincidir; el código confirma la identidad.
5. Desactivar revoca membresía y sesiones, y conserva historial.
6. No se puede degradar o desactivar al último CEO activo.
7. Un empleado no puede cambiar su propio rol.

**Criterios de aceptación**

- Un empleado nuevo se activa con código y define su contraseña.
- Un empleado desactivado pierde acceso inmediatamente.
- Un admin no puede crear otro owner.

---

## 6. Módulo: menú y categorías

**Propósito:** construir la oferta del restaurante y publicarla.

**Entidades:** `menu_categories`, `menu_products`.

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/menu/categories` | Listar |
| POST | `/tenant/menu/categories` | Crear |
| PATCH | `/tenant/menu/categories/{id}` | Editar |
| DELETE | `/tenant/menu/categories/{id}` | Desactivar |
| GET | `/tenant/menu/products` | Listar con filtros |
| POST | `/tenant/menu/products` | Crear |
| PATCH | `/tenant/menu/products/{id}` | Editar |
| DELETE | `/tenant/menu/products/{id}` | Desactivar |
| POST | `/tenant/menu/products/{id}/image` | Subir imagen |
| GET | `/public/{slug}/menu` | Menú público |

**Reglas**

1. Nombre obligatorio, 2–80 caracteres; descripción máxima 500.
2. Precio entero en centavos, mayor o igual a cero.
3. Un producto inactivo no aparece en la página pública.
4. Eliminar una categoría no elimina productos: los deja sin categoría.
5. Las imágenes se validan en servidor (tipo, tamaño, dimensiones).
6. Todo listado del panel está filtrado por el schema del tenant.

**Criterios de aceptación**

- CRUD completo con validación y errores claros.
- El menú público de A nunca muestra productos de B.
- El precio no puede ser negativo ni enviarse como texto libre.

---

## 7. Módulo: mesas y sesiones QR

**Propósito:** vincular la atención presencial a una mesa sin exigir cuenta al cliente.

**Entidades:** `restaurant_tables`, `table_sessions`, `service_requests`.

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/tables` | Listar mesas y estado |
| POST | `/tenant/tables` | Crear mesa |
| PATCH | `/tenant/tables/{id}` | Editar |
| POST | `/tenant/tables/{id}/qr` | Regenerar token del QR |
| POST | `/tenant/tables/{id}/status` | Cambiar estado con transición permitida |
| GET | `/public/table/{token}` | Abrir o recuperar sesión anónima |
| POST | `/public/table/{token}/requests` | Enviar solicitud (rate limited) |
| GET | `/tenant/table-sessions` | Sesiones activas |
| POST | `/tenant/table-sessions/{id}/close` | Cerrar y reiniciar |
| POST | `/tenant/service-requests/{id}/attend` | Marcar atendida |

**Reglas**

1. El QR contiene un token opaco; nunca el ID interno de la mesa.
2. Una mesa tiene como máximo una sesión abierta (índice único parcial).
3. Estados operativos: `available`, `occupied`, `pending_payment`, `reserved`, `inactive`.
4. Abrir sesión deja la mesa `occupied` y la bloquea para reservas en tiempo real.
5. Pedir la cuenta deja la mesa `pending_payment`; sigue bloqueada.
6. Pago en línea confirmado → la mesa pasa a `available` sin intervención del mesero.
7. Pago en efectivo confirmado por el mesero o cajero → la mesa pasa a `available` al registrarlo.
8. Cancelación en efectivo → única liberación manual del mesero, con motivo.
9. La sesión no caduca por tiempo: termina por pago o por cancelación manual.
10. Las solicitudes no requieren datos personales.
11. Cada sesión puede enviar un número limitado de solicitudes por minuto.
12. Un token de mesa de A no es válido en B.
13. El mesero ve la solicitud con número de mesa, hora y estado.
14. El cliente puede registrarse o iniciar sesión desde el QR; eso no crea un pedido por sí solo.
15. Volver a escanear un QR de una sesión abierta reanuda la misma sesión, no crea otra.

**Criterios de aceptación**

- Escanear el QR abre una sesión anónima funcional.
- Al cerrar la sesión, el mismo QR inicia un flujo limpio.
- Un QR antiguo de una sesión cerrada no reabre la sesión anterior.
- Confirmar el pago deja la mesa disponible sin intervención manual adicional.

---

## 8. Módulo: pedidos

**Propósito:** registrar y seguir la preparación y el cobro de pedidos.

**Entidades:** `orders`, `order_items`.

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/orders` | Listar por estado, mesa, fecha |
| POST | `/tenant/orders` | Crear pedido presencial (idempotente) |
| POST | `/public/{slug}/orders` | Crear pedido a domicilio (cliente registrado) |
| GET | `/tenant/orders/{id}` | Detalle |
| PATCH | `/tenant/orders/{id}` | Editar en estado `draft` |
| POST | `/tenant/orders/{id}/confirm` | Confirmar y congelar precios |
| POST | `/tenant/orders/{id}/status` | Cambiar estado operativo |
| POST | `/tenant/orders/{id}/cancel` | Cancelar con motivo |

**Máquina de estados**

```
draft ──confirm──► confirmed ──► in_preparation ──► ready ──► served ──► closed
   │                    │              │              │          │
   └────cancelled◄──────┴──────────────┴──────────────┴──────────┘
```

Estados de pago, independientes: `unpaid → pending → paid`, con `refunded` como excepción y `not_applicable` para cortesías.

Pedido a domicilio: `confirmed → in_preparation → ready → out_for_delivery → delivered` (+ `cancelled`). No tiene mesa; requiere cliente registrado, dirección y teléfono.

**Reglas**

1. El total se calcula en el servidor; se ignoran precios enviados por el cliente.
2. No se aplican impuestos, propinas ni descuentos (D-072). El total es la suma de líneas más el costo de envío cuando aplique.
4. Al confirmar se congelan nombre, precio unitario y total de cada línea.
5. Un pedido confirmado no se edita: se cancela o se genera uno nuevo.
6. Solo se puede cancelar antes de `served` (o `delivered`), salvo autorización del CEO registrada.
7. Cada cambio de estado se audita con usuario y hora.
8. Un pedido de mesa exige sesión abierta y lo crea el mesero; el cliente no puede autopedir desde el QR.
9. Un pedido a domicilio exige cuenta de cliente en ese restaurante.
10. El pedido llega a cocina con el ID de mesa (presencial) o el identificador de domicilio, y el detalle de líneas.
11. La creación es idempotente con `Idempotency-Key`.
12. El cocinero cambia estados de preparación, no precios ni datos del cliente.

**Criterios de aceptación**

- Dos envíos con la misma clave producen un solo pedido.
- El detalle de A no es accesible desde B cambiando el ID.
- El total coincide con la suma de líneas calculadas en servidor.
- Un usuario sin cuenta no puede crear un pedido a domicilio.
- Cocina ve la mesa asociada al pedido presencial.

---

## 9. Módulo: reservas

**Propósito:** gestionar reservas con datos del cliente y evitar conflictos.

**Entidades:** `reservations`.

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/tenant/reservations` | Listar por fecha y estado |
| POST | `/tenant/reservations` | Crear reserva (idempotente opcional) |
| PATCH | `/tenant/reservations/{id}` | Editar |
| POST | `/tenant/reservations/{id}/status` | Confirmar, cancelar, no-show |
| GET | `/public/{slug}/availability` | Disponibilidad pública |
| POST | `/public/{slug}/reservations` | Crear reserva (cliente registrado) |

**Reglas**

1. Solo un cliente con cuenta en ese restaurante puede reservar; la disponibilidad se consulta sin cuenta.
2. Fecha, hora, número de personas y mesa son obligatorios.
3. No se aceptan reservas en el pasado ni con duración menor a 30 minutos.
4. La mesa no puede solaparse con otra reserva activa.
5. La cancelación conserva el registro y el motivo.
6. Los datos personales solo se usan para gestionar la reserva.
7. Al sentar al cliente, la mesa pasa a `occupied`; al cancelar o no presentarse, vuelve a `available` si no hay sesión abierta.
8. La reserva puede generar un pago registrado (no procesado).

**Criterios de aceptación**

- Dos solicitudes simultáneas para la misma mesa y franja no crean conflicto.
- El estado no salta de `cancelled` a `confirmed` sin nueva reserva.

---

## 10. Módulo: caja ligera, pagos y comprobantes

> **Resuelto (D-070):** la caja registra la compra, confirma el pago, imprime el comprobante y genera un QR de descarga. No es un POS: sin turnos, arqueo, inventario ni facturación fiscal. El pago en línea se confirma por webhook firmado con un proveedor simulado (D-073).

**Entidades:** `payments`, `payment_events`, `receipts`.

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/tenant/orders/{id}/payments` | Registrar pago |
| POST | `/tenant/payments/{id}/confirm` | Confirmar pago y liberar mesa (idempotente) |
| POST | `/tenant/payments/{id}/receipt` | Generar e imprimir comprobante |
| POST | `/tenant/reservations/{id}/payments` | Registrar pago de reserva |
| POST | `/webhooks/payments/{provider}` | Webhook firmado del proveedor |
| GET | `/sandbox/pay/{payment_id}` | Pago simulado (solo desarrollo) |
| GET | `/public/receipts/{token}` | Descargar comprobante con token |
| POST | `/tenant/receipts/{id}/email` | Enviar comprobante por correo |

**Reglas**

1. La caja registra la compra y el pago; el mesero o cajero confirma en efectivo.
2. El pago en línea nace `pending` y solo pasa a `paid` con un evento firmado del proveedor (D-073).
3. No se almacenan datos de tarjeta. En el MVP se usa un proveedor simulado (sandbox) que no mueve dinero real.
4. El webhook se valida por HMAC, marca de tiempo y `event_id` único; repetirlo no duplica el pago.
5. La página de sandbox solo existe en desarrollo y se desactiva en producción.
6. El comprobante se genera al quedar `paid`, con token aleatorio y numeración por tenant; no tiene validez fiscal.
7. La confirmación del pago libera la mesa: automática si es en línea, al registrarla si es efectivo.
8. La cancelación en efectivo es la única liberación manual y exige motivo.
9. La confirmación es idempotente: dos confirmaciones o webhooks simultáneos no liberan ni cobran dos veces.
10. Reembolsos, notas de crédito, turnos y arqueo quedan fuera del MVP.

**Criterios de aceptación**

- Un webhook firmado marca el pago como `paid` y libera la mesa sin acción del mesero.
- Un webhook repetido no duplica el pago ni vuelve a liberar la mesa.
- Una firma inválida se rechaza y no cambia el estado.
- La página de sandbox no está disponible con `APP_ENV=production`.
- El comprobante se imprime y su QR de descarga funciona.

---

## 11. Módulo: página pública

**Propósito:** presentar el restaurante con su identidad, sin filtrar datos privados.

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/public/{slug}` | Configuración pública |
| GET | `/public/{slug}/menu` | Menú publicado |
| GET | `/public/{slug}/availability` | Disponibilidad de reservas |
| PUT | `/tenant/public-site` | Actualizar configuración |
| POST | `/tenant/public-site/publish` | Publicar |
| POST | `/tenant/public-site/unpublish` | Despublicar |

**Reglas**

1. Solo se exponen campos marcados como públicos.
2. El contenido se lee del schema del tenant resuelto por `slug` en `platform.tenants`.
3. Un tenant suspendido muestra una página informativa, no su menú.
4. La publicación invalida la caché de la página.
5. Los colores se validan contra un formato permitido.

**Criterios de aceptación**

- La página de A no renderiza datos de B.
- Despublicar oculta el contenido sin borrar la configuración.
- El HTML público no incluye tokens ni datos internos.

---

## 12. Módulo: suscripciones y capacidades

**Propósito:** controlar qué puede usar cada tenant según su plan, sin esparcir condiciones por el código.

**Entidades:** `plans`, `subscriptions`, `subscription_invoices`.

**Reglas**

1. Las capacidades se declaran como datos (`capabilities` y `limits`) y se evalúan en un único servicio.
2. El MVP activa planes manualmente.
3. Al vencer: se conserva el acceso de lectura y la gestión de cuenta; se bloquean funciones premium.
4. Nunca se elimina el schema por impago.
5. Un límite excedido devuelve 402/403 con mensaje claro, no un error 500.
6. El consumo de IA se mide incluso si no se cobra.

**Criterios de aceptación**

- Cambiar de plan habilita o restringe funciones sin desplegar código.
- Un tenant vencido puede renovar y recuperar el acceso.

---

## 13. Módulo: inteligencia artificial

**Propósito:** asistir sin convertirse en una vía de acceso a datos ajenos.

**Funciones del MVP**

1. Generar o mejorar descripción de un producto.
2. Generar descripción del restaurante.
3. Responder consultas sobre el menú y pedidos del tenant activo.
4. Sugerir textos para la página pública.

**Endpoints**

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/tenant/ai/describe-product` | Generar descripción |
| POST | `/tenant/ai/describe-restaurant` | Generar presentación |
| POST | `/tenant/ai/ask` | Consulta sobre datos autorizados |
| GET | `/tenant/ai/usage` | Consumo del tenant |

**Reglas**

1. El contexto se construye en el backend con el tenant activo.
2. Las herramientas disponibles se limitan al permiso del usuario.
3. La IA no ejecuta DDL ni modifica permisos.
4. Las escrituras se confirman con el usuario y pasan por el servicio del módulo.
5. Se cachean respuestas repetibles (por ejemplo, misma descripción base).
6. Se registra consumo y se aplican cuotas por tenant.
7. Un 429 del proveedor se traduce en un mensaje claro y un fallback controlado.
8. El prompt del usuario nunca se concatena con datos de otro tenant.

**Criterios de aceptación**

- Una instrucción maliciosa no devuelve datos de otro tenant.
- El consumo queda registrado con proveedor, modelo y tokens.
- La aplicación sigue funcionando si el proveedor falla.

---

## 14. Módulo: auditoría

**Propósito:** reconstruir quién hizo qué, especialmente en operaciones sensibles.

**Reglas**

1. Se registra actor, tenant, acción, entidad, IP y fecha.
2. No se registran contraseñas, códigos ni tokens.
3. Los eventos de Lixus incluyen el motivo de la intervención.
4. El registro es de solo lectura desde la aplicación.
5. La retención mínima se define en P-13.

---

## 15. Orden de implementación recomendado

1. Tenants + aprovisionamiento (RF-01).
2. Identidad y sesión (RF-02).
3. Personal y permisos (RF-04).
4. Menú y categorías (RF-05) — **entidad CRUD académica**.
5. Pedidos (RF-07) — **entidad CRUD académica**.
6. Mesas y QR (RF-06).
7. Reservas (RF-08).
8. Página pública (RF-10).
9. Suscripciones (RF-11).
10. IA (RF-12).
11. Caja ligera, confirmación de pago y comprobantes con QR (D-070).

**Riesgo de alcance:** el enunciado exige 2–3 entidades con CRUD completo. Menú y pedidos deben quedar impecables antes de sumar módulos opcionales.

---

**Fin de `04-MODULOS.md`.**
