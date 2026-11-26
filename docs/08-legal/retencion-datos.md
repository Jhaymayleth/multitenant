# Política de retención de datos

**Estado:** Borrador
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Legal / Ingeniería

> **BORRADOR — requiere revisión de un abogado en la jurisdicción que se defina.**
> Los plazos son propuestas y deben validarse contra la ley aplicable.

## 1. Principio

Se conserva solo lo necesario para prestar el servicio, cumplir la ley y atender reclamos. Cuando deja de ser necesario, se elimina o se anonimiza.

## 2. Plazos propuestos

| Dato | Retención | Motivo |
|---|---|---|
| Cuenta y datos del restaurante | Mientras haya contrato + 30 días | Continuidad y reactivación |
| Menú, mesas, personal | Mientras haya contrato + 30 días | Operación |
| Pedidos y pagos | 5 años o plazo fiscal aplicable | Contabilidad y reclamos |
| Comprobantes | 5 años o plazo fiscal aplicable | Respaldo |
| Reservas | 2 años | Historial y reclamos |
| Logs técnicos | 90 días | Diagnóstico |
| Auditoría | 12 meses | Seguridad |
| Backups | 30 días | Recuperación |
| Solicitudes de soporte | 2 años | Historial |
| Cookies de sesión | 60 minutos | Seguridad |

## 3. Cancelación

1. El cliente solicita la cancelación.
2. Se conserva el acceso de lectura por el periodo acordado.
3. Se exportan los datos si se solicita.
4. Al vencer el periodo, se elimina o anonimiza.
5. Se conserva lo exigido por ley.

## 4. Eliminación

- La eliminación es lógica primero y física después.
- Los backups se purgan en su ventana.
- La eliminación de un tenant requiere autorización y registro.
- No se elimina un dato con obligación legal de conservación.

## 5. Exportación

- Formato CSV o JSON.
- Incluye menú, pedidos, reservas y configuración.
- No incluye secretos ni datos de otros tenants.
- Se entrega por canal seguro.

## 6. Responsabilidades

| Rol | Responsabilidad |
|---|---|
| Cliente | Solicitar cancelación o eliminación |
| Soporte | Registrar la solicitud |
| Ingeniería | Ejecutar y verificar |
| Legal | Validar excepciones |

## 7. Registro

Toda eliminación de tenant se registra con fecha, solicitante, motivo y resultado.
