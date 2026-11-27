# Deuda técnica

**Estado:** Vigente
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Ingeniería

Prioridad: **P0** bloquea vender u operar; **P1** afecta calidad o seguridad; **P2** mejora.

| ID | Deuda | Evidencia | Impacto | Prioridad |
|---|---|---|---|---|
| RT-01 | Frontend sin conexión a la API | Sin `fetch`, sin `lib/api.ts` | No hay producto visible | P0 |
| RT-02 | Pedidos sin líneas ni total | `orders/service.py` crea `total_cents=0` | No se puede cobrar | P0 |
| RT-03 | Rate limiting ausente | Solo variables de configuración | Abuso y fuerza bruta | P0 |
| RT-04 | Idempotencia incompleta | Solo alta de tenant | Duplicados en pedidos y cobros | P0 |
| RT-05 | Sesión sin `Secure` | `auth/router.py` | Riesgo en producción | P0 |
| RT-06 | Sin CSRF | No hay implementación | Escrituras cruzadas | P0 |
| RT-07 | Sin revocación de sesión | Logout solo borra cookie | Empleado desactivado conserva token | P1 |
| RT-08 | `switch-tenant` stub | No emite token | No se puede cambiar de restaurante | P1 |
| RT-09 | `/auth/me` genérico | Nombre hardcodeado | UI incorrecta | P1 |
| RT-10 | Personal huérfano | `user_id` aleatorio | Empleado no puede entrar | P1 |
| RT-11 | Cobros no confirman | Endpoint stub | No se libera mesa | P1 |
| RT-12 | Comprobante siempre 404 | Endpoint stub | No hay comprobante | P1 |
| RT-13 | QR sin sesión real | Endpoint devuelve mensaje | No hay solicitudes | P1 |
| RT-14 | Sitio público no publica | `is_published` nunca cambia | Página siempre 404 | P1 |
| RT-15 | Webhook sin firma | No valida HMAC | Eventos falsos | P1 |
| RT-16 | Sin auditoría de escritura | Tabla vacía | Sin trazabilidad | P1 |
| RT-17 | Rol de BD con privilegios amplios | App conecta como dueño | Riesgo de cruce | P1 |
| RT-18 | Migración inicial con downgrade incorrecto | Crea `alembic_version` | Rollback roto | P2 |
| RT-19 | Sin seeds | Planes vacíos en base nueva | Demo y alta manual | P2 |
| RT-20 | Errores inconsistentes | `detail` vs `error` | UI no muestra mensajes | P1 |
| RT-21 | Sin `request_id` | Handler 500 genérico | Difícil diagnosticar | P1 |
| RT-22 | Backups sin restaurar | Sin evidencia | Riesgo de pérdida | P0 |
| RT-23 | Sin staging | Solo local y producción | Riesgo de release | P1 |
| RT-24 | Token de runner expuesto en documentación antigua | `VARIABLES_ENTORNO.md` | Seguridad | P0 |
| RT-25 | Código y modelos sin uso | Modelos y esquemas huérfanos | Mantenimiento | P2 |
| RT-26 | CORS con `localhost` fijo | `main.py` | Configuración incorrecta | P2 |
| RT-27 | Búsqueda de menú sin proveedor dedicado | Solo `ILIKE`, sin `SearchProvider` (D-162) | Búsqueda limitada al crecer el catálogo | P1 |

## Orden recomendado

1. RT-01, RT-02: producto visible y pedido cobrable.
2. RT-03, RT-04, RT-05, RT-06: seguridad y robustez.
3. RT-10, RT-11, RT-12, RT-13, RT-14: operación diaria.
4. RT-22, RT-24: continuidad y secreto.
5. RT-27 cuando el catálogo o el número de tenants lo justifique.
6. Resto.

## Regla

La deuda P0 se atiende antes de añadir una feature nueva. La deuda P1 se planifica en el mismo trimestre. La P2 no bloquea pero se registra.
