# 08 — Seguridad y control de acceso

**Proyecto:** Lixus — Plataforma SaaS multitenant para restaurantes
**Versión:** 0.2
**Estado:** Diseño base; las decisiones marcadas como pendientes no deben implementarse como definitivas
**Decisiones aplicadas:** D-005, D-024 a D-028, D-044, D-045, D-049, D-051, D-061
**Última actualización:** 22 de octubre de 2026

---

## 1. Principios

1. **El frontend no es una frontera de seguridad.** Ocultar un botón no protege un endpoint.
2. **El servidor decide.** Identidad, tenant, rol y permiso se calculan desde la sesión y la base de datos.
3. **Mínimo privilegio.** Cada rol recibe solo lo necesario para su tarea.
4. **Aislamiento por diseño.** El schema del tenant es el límite; el resto son defensas adicionales.
5. **Todo lo privilegiado se audita.** Especialmente lo que hace Lixus.
6. **Nada sensible en el repositorio.** Secretos por variables de entorno.

---

## 2. Activos y amenazas

| Activo | Amenaza | Control principal |
|---|---|---|
| Datos de un tenant | Acceso cruzado por ID, filtro olvidado o schema incorrecto | Contexto de tenant validado + schema fijo + pruebas negativas |
| Credenciales | Fuerza bruta, reutilización, filtraciones | Argon2id, rate limiting, códigos de un solo uso, MFA para Lixus |
| Sesión | Robo de cookie, XSS, CSRF | `HttpOnly`, `Secure`, `SameSite`, CSRF token, CSP |
| Roles | Escalada de privilegios | Permisos comprobados en servidor; el rol del token se revalida |
| Enlaces de comprobante | Enumeración o acceso no autorizado | Token aleatorio de 256 bits con caducidad |
| Webhook de pago | Evento falso, replay o monto manipulado | HMAC, marca de tiempo, `event_id` único y validación del monto |
| Archivos | Carga de contenido malicioso | Validación de tipo real, límite de tamaño, re-codificación |
| IA | Prompt injection, fuga entre tenants | Contexto acotado, herramientas con permisos, sin SQL libre |
| Operaciones de Lixus | Abuso de privilegios | Permisos separados, MFA, auditoría y motivo |
| Secretos | Exposición en logs o repositorio | Gestión por entorno, revisión de logs, `.gitignore` |

---

## 3. Autenticación

### 3.1 Métodos admitidos

| Método | Quién | Estado |
|---|---|---|
| Correo + contraseña | Personal y clientes | APROBADO (D-025) |
| Google (OIDC) | Clientes registrados; personal por confirmar (P-12) | APROBADO para clientes |
| Código de activación | Empleado pre-registrado por el restaurante | APROBADO (D-051) |
| Enlace de un solo uso | Recuperación de contraseña y verificación de correo | APROBADO |
| MFA (TOTP) | Lixus | Recomendado y exigible en producción |

### 3.2 Registro de clientes

1. El cliente llega desde la página pública o desde el QR de registro en caja.
2. Se registra con correo/contraseña o Google.
3. Se crea `platform.users` y, en el schema del tenant, `customers`.
4. El perfil de cliente **no** otorga permisos de personal.
5. No se comparten datos ni historial con otros tenants.

### 3.3 Contraseñas

- Hash **Argon2id** con parámetros configurables; nunca SHA-256 ni MD5.
- Mínimo 12 caracteres; se rechazan las más comunes y las que contienen el correo.
- No se impone composición artificial de símbolos.
- El cambio de contraseña revoca todas las sesiones activas.
- El hash nunca se registra en logs ni se devuelve por API.

### 3.4 Códigos de verificación

| Aspecto | Regla |
|---|---|
| Formato | 6 dígitos aleatorios |
| Almacenamiento | Solo hash (`verification_codes.code_hash`) |
| Vigencia | 10 minutos |
| Intentos | Máximo 5; luego se invalida |
| Reenvío | Máximo 1 cada 60 segundos y 3 por hora |
| Uso | Un solo uso; al consumirse se marca `consumed_at` |
| Entrega | Correo transaccional |

**Flujo de activación de empleado**

1. El CEO registra el correo y el rol → usuario `pending`, membresía `invited`.
2. El sistema envía un código.
3. El empleado introduce el código, define su contraseña y acepta condiciones.
4. La membresía pasa a `active`; el usuario pasa a `active`; se registra auditoría.

**Pendiente P-12:** definir si el empleado puede usar Google en lugar de contraseña.

### 3.5 Recuperación de cuenta

- Enlace con token aleatorio de un solo uso, hash en base de datos, vigencia de 30 minutos.
- La respuesta es siempre genérica para no revelar si el correo existe.
- Al usarse se invalida y se revocan las sesiones previas.
- Cuentas creadas solo con Google se recuperan desde Google; no se ofrece contraseña local.

### 3.6 Inicio de sesión

- Rate limiting obligatorio (ver `09-ROBUSTEZ.md`).
- Respuesta genérica ante credenciales incorrectas.
- Comparación en tiempo constante cuando aplique.
- Registro de intentos fallidos para detección de abuso.
- Tras 5 fallos para el mismo correo en 15 minutos, se responde 429 aunque la contraseña sea correcta.

---

## 4. Sesión con JWT en cookie

### 4.1 Cookies

| Cookie | Contenido | Atributos |
|---|---|---|
| `lixus_session` | JWT de acceso | `HttpOnly`, `Secure` en producción, `SameSite=Lax`, `Path=/`, `Max-Age` corto |
| `lixus_refresh` | Token de renovación | Igual, `Path=/api/v1/auth`, vigencia mayor |
| `lixus_csrf` | Token CSRF (no sensible) | **No** `HttpOnly`, `SameSite=Lax` |
| `lixus_table` | Sesión anónima de mesa | `HttpOnly`, `Path=/`, vigencia corta |

**Nunca** se usa `localStorage` ni `sessionStorage` para el token (RAC-02).

### 4.2 Contenido del JWT

```json
{
  "iss": "lixus.api",
  "aud": "lixus.web",
  "sub": "3f1c...",
  "tenant_id": "8a2d...",
  "membership_id": "b73e...",
  "role": "waiter",
  "jti": "9f0a...",
  "iat": 1761180000,
  "exp": 1761181800,
  "ver": 4
}
```

- `ver` es la versión de sesión del usuario; si cambia en base de datos, el token deja de ser válido.
- El rol incluido es una comodidad, **no** la fuente de autorización: se revalida contra `tenant_memberships`.
- Para clientes, `role` es `customer` y no existen permisos de panel.

### 4.3 Expiración y revocación

| Evento | Efecto |
|---|---|
| Expiración del acceso (30 min) | Se renueva con `lixus_refresh` |
| Logout | Se borran cookies y se añade `jti` a la lista de revocación |
| Desactivación de empleado | Se incrementa `ver`; todos sus tokens quedan inválidos |
| Cambio de contraseña | Igual que desactivación |
| Cambio de rol | Se emite token nuevo; el anterior se revoca |
| Cambio de tenant | Token nuevo; el anterior no sirve para el nuevo tenant |

La lista de revocación se guarda en Redis con TTL igual al tiempo restante del token.

### 4.4 CSRF

Las cookies se envían automáticamente, así que toda escritura exige:

1. `SameSite=Lax` (bloquea la mayoría de peticiones cross-site).
2. Doble envío: el frontend lee `lixus_csrf` y envía `X-CSRF-Token`; el backend compara.
3. Verificación de `Origin`/`Referer` para métodos no seguros.
4. Los endpoints públicos de solo lectura no requieren token.

### 4.5 Cookie y dominios

- Frontend y API deben compartir la misma eTLD+1 para que la cookie sea de primera parte.
- Si se separan en dominios distintos, Next.js actúa como proxy/BFF y la cookie se emite en el dominio del frontend.
- En local, `Secure=false`; en producción, `Secure=true` y HTTPS obligatorio.

### 4.6 Cambio de tenant

`POST /auth/switch-tenant` recibe el `tenant_id` deseado y:

1. Verifica membresía activa del usuario en ese tenant.
2. Comprueba que el tenant está activo.
3. Emite un JWT nuevo con el tenant elegido.
4. Revoca el token anterior para ese contexto.

El cliente **no** puede cambiar de tenant modificando un header.

---

## 5. Autorización

### 5.1 Cadena de verificación

```
1. ¿Cookie presente y JWT válido?           → 401
2. ¿Usuario activo y versión vigente?        → 401
3. ¿Membresía activa en el tenant del token? → 403
4. ¿Tenant en estado operativo?              → 403
5. ¿Rol/permiso para esta operación?         → 403
6. ¿Recurso pertenece al tenant?             → 404
7. Ejecutar en el schema autorizado
```

El paso 6 devuelve **404** y no 403: no se confirma la existencia de recursos ajenos.

### 5.2 Modelo de permisos

- RBAC con roles predefinidos (D-018) y permisos atómicos por módulo y acción.
- La matriz funcional está en `04-MODULOS.md`; su aprobación definitiva es P-05.
- La comprobación se implementa como dependencia reutilizable, no repetida en cada endpoint.

```python
def require(permission: str):
    async def guard(ctx: TenantCtx = Depends(tenant_context)):
        if permission not in ROLE_PERMISSIONS[ctx.role]:
            raise HTTPException(403, "No autorizado")
        return ctx
    return guard
```

- Las reglas de negocio (por ejemplo, "no degradar al último CEO") viven en el servicio, no en el guard.

### 5.3 Reglas anti-IDOR

1. Toda consulta por ID incluye el schema del tenant en la sesión de base de datos.
2. No se acepta `tenant_id` del cuerpo para decidir el schema.
3. Los listados no permiten filtrar por tenant ajeno.
4. Los IDs de recursos ajenos devuelven 404.
5. Los endpoints de descarga usan tokens opacos, no IDs secuenciales.

### 5.4 Frontend

- El layout privado consulta `/auth/me` y redirige si no hay sesión.
- El menú se construye según permisos, pero **cada endpoint revalida**.
- No se cachean respuestas privadas en CDN.
- `Cache-Control: no-store` en respuestas autenticadas.

---

## 6. Rol global Lixus

| Control | Regla |
|---|---|
| Cuenta | Separada del registro público; creada por aprovisionamiento |
| MFA | Obligatorio en producción |
| Contraseña | Mínimo 16 caracteres, rotación recomendada |
| Sesión | 30 minutos de inactividad |
| Permisos | Solo plataforma: tenants, verificación, planes, auditoría |
| Datos de negocio | **Sin acceso**: solo metadatos del tenant (D-071) |
| Acciones destructivas | Prohibidas sobre datos del restaurante; desactivar no borra |
| Suplantación | Prohibida |

El nombre "Lixus" (D-016) no es una medida de seguridad: no se documenta como control.

---

## 7. Sesión anónima de mesa

| Aspecto | Regla |
|---|---|
| Token del QR | 32 bytes aleatorios; en base solo el hash |
| Vinculación | Token → mesa → sesión abierta |
| Almacenamiento en cliente | Cookie `lixus_table` `HttpOnly` |
| Vigencia | Sin caducidad por tiempo: termina por pago confirmado o cancelación en efectivo (D-068) |
| Datos personales | Ninguno |
| Acciones | Solicitudes y consulta del estado de la sesión |
| Límite | 10 solicitudes por minuto por sesión |
| Reinicio | Al cerrar, se invalidan token y sesión; se emite uno nuevo |
| QR antiguo | Reanuda la sesión abierta si existe; si no, inicia una nueva cuando la mesa está libre |

Riesgo aceptado: cualquiera con el QR puede enviar solicitudes mientras la sesión esté abierta. Se mitiga con límite de solicitudes, cierre por pago y supervisión del mesero.

---

## 8. Seguridad de la IA

1. **El prompt no es una frontera.** El contexto se construye en el backend con el tenant y los permisos del usuario.
2. **Herramientas con allowlist.** La IA solo puede invocar funciones registradas; no genera SQL.
3. **Validación de argumentos.** Cada herramienta valida tipos, pertenencia al tenant y límites.
4. **Confirmación humana** para acciones que modifican datos sensibles.
5. **Sin secretos en el prompt.** Nunca se envían claves, tokens ni datos de otros tenants.
6. **Registro** de prompt (resumido), herramienta, modelo, tokens y resultado.
7. **Pruebas de inyección:** pedir datos de otro tenant, cambiar de rol, ejecutar SQL o saltarse permisos.
8. **Degradación controlada:** si el proveedor falla, la aplicación sigue operativa sin IA.

---

## 9. Archivos y comprobantes

- Bucket privado; sin listado público.
- Validación por magic bytes, no por extensión.
- Formatos: JPEG, PNG, WebP; máximo configurable (inicial 5 MB).
- Re-codificación de imágenes para eliminar metadatos y contenido incrustado.
- Nombre generado (UUID), sin ruta del usuario.
- Entrega por URL firmada de 5–15 minutos o proxy autenticado.
- Comprobantes: token aleatorio, caducidad, límite de descargas y registro de acceso.
- Virus scan: pendiente P-15 (fuera del MVP si no hay servicio disponible).

### 9.1 Webhooks de pago

- Firma **HMAC-SHA256** con `PAYMENT_WEBHOOK_SECRET`; header `X-Payment-Signature: t=<timestamp>,v1=<hmac>`.
- Tolerancia de ±5 minutos; un timestamp viejo se rechaza para evitar replay.
- `provider_event_id` único en `payment_events`: un evento repetido se ignora y responde 200.
- Se valida que el monto y la moneda coincidan con el pago pendiente.
- No se confía en el estado del cuerpo sin firma válida.
- El procesamiento es transaccional: pago, sesión de mesa y comprobante cambian juntos.
- Los endpoints de sandbox solo existen con `APP_ENV != production`.
- Rate limiting por proveedor y por IP; auditoría del evento y del cambio de estado.
- No se almacenan datos de tarjeta ni secretos del proveedor en la base.

---

## 10. Secretos y configuración

| Secreto | Dónde vive |
|---|---|
| `JWT_SECRET` | Variable de entorno (≥ 256 bits) |
| Credenciales de base de datos | Variable de entorno |
| Credenciales de R2 | Variable de entorno |
| `GROQ_API_KEY` | Variable de entorno |
| `PAYMENT_WEBHOOK_SECRET` | Variable de entorno |
| SMTP | Variable de entorno |
| MFA de Lixus | Cifrado en base de datos |

Reglas: `.env` en `.gitignore`, `.env.example` sin valores reales, rotación documentada, secretos nunca en logs ni en mensajes de error.

---

## 11. Auditoría de seguridad

Se registran como mínimo:

- Inicios de sesión fallidos y exitosos (sin contraseña).
- Cambios de contraseña y recuperación.
- Creación, cambio de rol y desactivación de membresías.
- Acciones de Lixus sobre tenants y planes.
- Accesos excepcionales a datos de un tenant.
- Invocación de herramientas de IA que escriben datos.
- Cambios de configuración pública.
- Intentos de acceso cruzado rechazados (métrica).

Formato: actor, tenant, acción, entidad, IP, user agent, timestamp, metadatos sin secretos.

---

## 12. Pruebas de seguridad obligatorias

| ID | Prueba | Resultado esperado |
|---|---|---|
| S-01 | Usuario de A solicita pedido de B por ID | 404 |
| S-02 | Usuario de A envía `tenant_id` de B en el body | Se ignora; opera en A |
| S-03 | Usuario de A manipula `schema_name` en un header | 400/403; nunca se usa |
| S-04 | Token con firma alterada | 401 |
| S-05 | Token expirado | 401 |
| S-06 | Cookie inspeccionada desde JavaScript | No accesible |
| S-07 | Empleado desactivado usa token previo | 401 |
| S-08 | Mesero intenta cambiar roles | 403 |
| S-09 | Empleado intenta asignarse `owner` | 403 |
| S-10 | Petición de escritura sin `X-CSRF-Token` | 403 |
| S-11 | QR de mesa de A usado en B | 404 |
| S-12 | Token de comprobante adivinado | 404 |
| S-13 | Prompt de IA pide datos de otro tenant | Respuesta sin datos ajenos |
| S-14 | Prompt de IA pide ejecutar SQL | Herramienta inexistente; se rechaza |
| S-15 | Subida de archivo con extensión falsa | 400 |
| S-16 | 6 intentos de login en 15 minutos | 429 + `Retry-After` |
| S-17 | Webhook con firma inválida | 401; el pago no cambia |
| S-18 | Webhook repetido con el mismo `event_id` | 200; no duplica pago ni liberación |
| S-19 | Webhook con monto distinto al pago | 422; no se marca pagado |
| S-20 | Acceso a `/sandbox/pay` en producción | 404 |

Estas pruebas forman parte del pipeline de CI.

---

## 13. Pendientes de seguridad

| ID | Tema |
|---|---|
| P-11 | Proveedor de correo transaccional |
| P-12 | Google para empleados |
| P-13 | Retención de auditoría y datos personales |
| P-15 | Análisis antivirus de archivos |
| P-16 | Política de contraseñas de Lixus y rotación de secretos |
| P-17 | Cabeceras CSP y hardening del frontend |

---

**Fin de `08-SEGURIDAD-Y-ACCESO.md`.**
