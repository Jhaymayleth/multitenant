# Backlog priorizado

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Producto

Prioridad: **P0** bloquea al primer cliente que paga; **P1** necesario para operar con comodidad; **P2** mejora o expansión.

## P0 — Primer cliente que paga

| ID | Feature | Resultado esperado | Estado | Depende de |
|---|---|---|---|---|
| BL-01 | Frontend conectado | Login y panel consumen la API real; ver [especificación](../05-frontend/cliente-api.md) | NO INICIADO | — |
| BL-02 | Identidad y sesión | Login, logout, guards y recuperación | PARCIAL | BL-01 |
| BL-03 | Menú | CRUD completo y publicación | PARCIAL | BL-01 |
| BL-04 | Pedidos | Líneas, total en servidor y estados | PARCIAL | BL-03 |
| BL-05 | Mesas y QR | Mesa, sesión y solicitudes | PARCIAL | BL-03 |
| BL-06 | Página pública | Menú, información y publicación | PARCIAL | BL-03 |
| BL-07 | Onboarding | Alta verificada y acceso del CEO | PARCIAL | BL-02 |
| BL-08 | Aislamiento | Pruebas negativas entre tenants | PARCIAL | — |
| BL-09 | Errores y validación | Mensajes comprensibles y request_id | NO INICIADO | BL-01 |
| BL-10 | Backups | Copia y restauración probadas | PARCIAL | — |

## P1 — Operación diaria

| ID | Feature | Resultado esperado | Estado | Depende de |
|---|---|---|---|---|
| BL-11 | Reservas | Disponibilidad, solapamiento y no-show | PARCIAL | BL-05 |
| BL-12 | Cobro de pedidos | Pasarela del restaurante, cierre de mesa y comprobante | NO INICIADO | BL-04 |
| BL-13 | Personal y roles | Invitación, permisos y revocación | PARCIAL | BL-02 |
| BL-14 | Correo transaccional | Invitaciones, códigos y avisos | NO INICIADO | BL-02 |
| BL-15 | Resumen del CEO | Estado del día y pendientes | NO INICIADO | BL-04, BL-12 |
| BL-16 | Rate limiting | Límites en login y escrituras | NO INICIADO | — |
| BL-17 | Idempotencia | Pedidos y cobros sin duplicados | PARCIAL | BL-04, BL-12 |
| BL-18 | CSRF y revocación | Sesión segura y cierre real | NO INICIADO | BL-02 |
| BL-19 | Auditoría | Registro de acciones administrativas | NO INICIADO | BL-02 |
| BL-20 | Soporte | Horario, canal y registro de casos | NO INICIADO | — |

## P2 — Crecimiento

| ID | Feature | Resultado esperado | Estado | Depende de |
|---|---|---|---|---|
| BL-21 | Suscripción y facturación | Cobro mensual y estados de cuenta | NO INICIADO | PD-07, PD-08 |
| BL-22 | Pasarelas de cobro | Suscripción (D-140) y pedidos (D-145), sin mezclar dinero | NO INICIADO | PD-08 |
| BL-23 | Reportes | Ventas, productos y ocupación | NO INICIADO | BL-12 |
| BL-24 | Notificaciones | Avisos automáticos por correo o WhatsApp | NO INICIADO | BL-14 |
| BL-25 | Multi-sucursal | Varias sedes por tenant | NO INICIADO | PD-25 |
| BL-26 | IA | Descripciones y asistencia con permisos | NO INICIADO | PD-26 |
| BL-27 | API e integraciones | Acceso para terceros | NO INICIADO | BL-21 |
| BL-28 | Segundo idioma | Interfaz en inglés | NO INICIADO | PD-19 |

## Cómo se prioriza

1. ¿Desbloquea el primer cliente que paga? → P0.
2. ¿Evita perder un cliente activo? → P0 o P1.
3. ¿Reduce costo de soporte o riesgo operativo? → P1.
4. ¿Abre ingresos nuevos? → P2, salvo que un cliente lo pague.
5. ¿Es “fácil” pero no cambia nada? → no entra.

## Próximas diez acciones

1. Conectar login y panel a la API.
2. Cerrar CRUD de menú.
3. Implementar pedidos con líneas y total.
4. Implementar sesión QR y solicitudes.
5. Publicar la página pública.
6. Completar onboarding y verificación.
7. Añadir guards y manejo de errores.
8. Probar aislamiento y permisos.
9. Verificar backup y restauración.
10. Definir precios y contrato para el piloto.
