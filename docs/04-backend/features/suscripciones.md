# Feature: suscripciones

**Estado:** NO INICIADO
**Dueño:** Ingeniería / Negocio
**Decisiones:** D-101
**Decisiones abiertas:** PD-07, PD-08, PD-09
**Documento frontend:** `05-frontend/features/suscripciones.md`

## 1. Objetivo

Cobrar el plan contratado por cada restaurante y reflejar el estado de la suscripción sin borrar datos.

## 2. Alcance

- Catálogo de planes y capacidades.
- Suscripción por tenant.
- Estado: activa, en gracia, vencida, cancelada.
- Límites por plan.
- Facturas y estado de cuenta.
- Reactivación.

## 3. Reglas de negocio

| ID | Regla |
|---|---|
| RN-191 | La suscripción pertenece al tenant. |
| RN-192 | El personal y los clientes no pagan licencia. |
| RN-193 | Al vencer, se conservan los datos y se restringen funciones premium. |
| RN-194 | La activación inicial es manual en la versión inicial. |
| RN-195 | Un cambio de plan respeta el periodo pagado. |
| RN-196 | No se elimina un tenant por impago sin proceso y aviso. |

## 4. API

| Método | Ruta | Estado |
|---|---|---|
| GET | `/platform/plans` | Implementado |
| POST | `/platform/tenants/{id}/subscription` | No existe |
| GET | `/tenant/subscription` | No existe |
| POST | `/tenant/subscription/cancel` | No existe |

## 5. Datos

- `platform.plans`: nombre, capacidades, límites, precio.
- `platform.subscriptions`: tenant, plan, estado, periodo.
- `platform.subscription_invoices`: factura, monto, estado.

## 6. Criterios de aceptación

- [ ] Un tenant tiene un plan visible.
- [ ] Los límites del plan se aplican en el backend.
- [ ] Al vencer, el tenant conserva datos y pierde funciones premium.
- [ ] El pago reactiva el acceso.
- [ ] La factura se puede consultar.
- [ ] Cambiar de plan no rompe datos.

## 7. Estado

Solo existen modelos y el listado de planes. No hay cobro, facturación ni límites aplicados.
