# Feature: auditoría

**Estado:** NO INICIADO
**Dueño:** Ingeniería
**Decisiones:** D-112, D-117
**Documento frontend:** `05-frontend/features/auditoria.md`

## 1. Objetivo

Saber quién hizo qué en la plataforma, especialmente en las acciones privilegiadas de Lixus.

## 2. Alcance

- Alta, verificación y activación de tenants.
- Cambios de rol y desactivación de personal.
- Accesos de Lixus a metadatos.
- Cambios de plan.
- Acciones de IA que escriban datos.
- Incidentes de seguridad.

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-211 | Toda acción privilegiada se registra. |
| RN-212 | El registro incluye actor, tenant, acción, fecha y resultado. |
| RN-213 | No se registran contraseñas, tokens ni datos sensibles. |
| RN-214 | El registro no se edita desde la aplicación. |
| RN-215 | La retención se define en PD-16. |

## 4. API

| Método | Ruta | Estado |
|---|---|---|
| GET | `/audit` | Implementado, solo lectura |
| GET | `/tenant/audit` | No existe |

## 5. Datos

- `platform.audit_log`: actor, tenant, acción, entidad, resultado, metadata.
- `tenant.audit_log`: opcional para acciones locales.

## 6. Criterios de aceptación

- [ ] Crear un tenant deja registro.
- [ ] Verificar un tenant deja registro.
- [ ] Cambiar un rol deja registro.
- [ ] Un acceso de Lixus deja registro.
- [ ] El registro se consulta con filtros.
- [ ] No se puede borrar desde la aplicación.

## 7. Estado

El endpoint de lectura existe, pero nada escribe en la tabla. La protección es la misma clave de plataforma.
