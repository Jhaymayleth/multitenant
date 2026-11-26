# Feature: plataforma y tenants

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Decisiones:** D-103, D-107, D-112, D-117
**Documento frontend:** `05-frontend/features/plataforma-tenants.md`

## 1. Objetivo

Permitir que Lixus dé de alta, verifique, active y administre restaurantes sin tocar la base de datos manualmente.

## 2. Alcance

- Crear un tenant con schema aislado.
- Listar y consultar tenants.
- Verificar y activar o cancelar.
- Consultar planes.
- Registrar la acción en auditoría (pendiente).

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-101 | El slug es único y legible; no se reutiliza. |
| RN-102 | El schema lo genera el servidor; el cliente no lo elige. |
| RN-103 | Un tenant no opera hasta estar `active`. |
| RN-104 | La verificación es manual en la versión inicial. |
| RN-105 | Desactivar no borra datos. |
| RN-106 | Lixus no accede a datos operativos del tenant. |
| RN-107 | El alta es idempotente con `Idempotency-Key`. |

## 4. Ciclo de estado

```text
provisioning → pending_verification → active
                     │                    │
                     └→ cancelled         └→ suspended → active
provisioning → provisioning_failed
```

## 5. API

| Método | Ruta | Estado |
|---|---|---|
| POST | `/platform/tenants` | Implementado |
| GET | `/platform/tenants` | Implementado |
| GET | `/platform/tenants/{id}` | Implementado |
| POST | `/platform/tenants/{id}/verify` | Implementado |
| GET | `/platform/plans` | Implementado |

Protección: `X-Platform-Admin-Key` (interina).

## 6. Datos

- `platform.tenants`: nombre, slug, schema, estado, contacto, moneda, zona horaria.
- `platform.tenant_memberships`: owner inicial.
- `platform.tenant_verifications`: evidencia y estado.
- `platform.idempotency_keys`: alta idempotente.
- `platform.audit_log`: pendiente de escritura.

## 7. Criterios de aceptación

- [ ] Un tenant creado por API queda `pending_verification`.
- [ ] Al aprobarlo queda `active` y su CEO puede iniciar sesión.
- [ ] El schema contiene todas las tablas del tenant.
- [ ] Repetir el alta con la misma clave no crea otro tenant.
- [ ] Sin clave de plataforma, la ruta responde 403.
- [ ] Un owner de tenant no puede listar otros tenants.
- [ ] La verificación queda auditada con usuario y fecha.

## 8. Dependencias

- `identidad-sesion` para el acceso del CEO.
- `auditoria` para el registro.
- `suscripciones` para el plan contratado.

## 9. Riesgos

- El aprovisionamiento ejecuta DDL y subprocess; un fallo deja recursos parciales.
- La clave compartida no identifica al operador.
- No hay limpieza automática de tenants fallidos.
