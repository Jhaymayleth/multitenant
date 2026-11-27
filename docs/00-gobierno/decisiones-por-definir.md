# Decisiones por definir

**Estado:** Vigente
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Producto

Cada fila es una pregunta abierta. El default es una propuesta del PO, no una decisión. Ninguna se implementa como definitiva hasta pasar a `decisiones.md`.

**Nota:** la parte legal (PD-14 a PD-17 y PD-28) queda diferida hasta que la aplicación funcione y sea revisada por abogado. No se toma como decisiones lo respondido en la entrevista sobre este tema.

**Nota (D-151):** el foco es el MVP. Las preguntas abiertas de negocio y operación (PD-04, PD-07, PD-08, PD-12, PD-13, PD-18, PD-23 y PD-29) también quedan diferidas; no bloquean el desarrollo.

| ID | Área | Pregunta | Impacto | Default propuesto | Estado |
|---|---|---|---|---|---|
| PD-04 | Mercado | ¿Quién decide la compra y quién influye? | Guion comercial y onboarding | Dueño o gerente; influyen administrador y contador | POR DEFINIR |
| PD-07 | Negocio | ¿Precios, moneda y ciclo de cobro de los tres planes? | Ingresos y posicionamiento | Estructura de tres planes aprobada en D-139; cifras, moneda y ciclo por validar con cinco entrevistas | POR DEFINIR |
| PD-08 | Negocio | ¿Qué pasarelas y cómo se factura? | Operación, contrato y legal | Suscripción por pasarela de Lixus (D-140); pedidos por pasarela propia del restaurante (D-145); proveedores y factura por definir | POR DEFINIR |
| PD-12 | Operación | ¿Horario de soporte y SLA? | Expectativa del cliente | Lunes a sábado 9:00–19:00; respuesta < 4 h laborables; crítico < 1 h | POR DEFINIR |
| PD-13 | Operación | ¿Quién hace qué dentro de Lixus? | Responsabilidad y escalamiento | Fundador/producto, ingeniería, operación/soporte y comercial; al inicio pueden coincidir | POR DEFINIR |
| PD-14 | Legal | ¿Jurisdicción y figura legal? | Contratos, impuestos, datos | Colombia, SAS; confirmar con abogado. Diferido hasta que la app funcione | POR DEFINIR |
| PD-15 | Legal | ¿Régimen de protección de datos aplicable? | Privacidad y contratos | Ley 1581 de Colombia y habeas data; confirmar con abogado. Diferido | POR DEFINIR |
| PD-16 | Legal | ¿Cuánto se conservan datos, auditoría, comprobantes y backups? | Cumplimiento y costo | Operativos mientras haya cuenta + 30 días; auditoría 12 meses; comprobantes 5 años; backups 30 días | POR DEFINIR |
| PD-17 | Legal | ¿Términos, cookies y facturación revisados? | Venta y confianza | Borradores revisados por abogado | POR DEFINIR |
| PD-18 | Marca | ¿Cuál es el dominio exacto y la identidad visual definitiva? | Percepción, correos y certificados | Nombre «Lixus», dominio propio (D-130) y tono directo y cercano (D-132) aprobados; falta el dominio exacto y la paleta/logotipo. | POR DEFINIR |
| PD-23 | Operación | ¿Proveedor de correo transaccional? | Invitaciones, códigos y avisos | Resend o Postmark, detrás de una interfaz | POR DEFINIR |
| PD-28 | Legal | ¿Exportación y eliminación de datos de un tenant? | Contratos y operación | Exportación CSV/JSON bajo solicitud; eliminación a los 30 días de cancelar, salvo obligación legal | POR DEFINIR |
| PD-29 | Operación | ¿RPO, RTO y retención de backups? | Continuidad | RPO 24 h, RTO 4 h, backups diarios por 30 días | POR DEFINIR |

## Cerradas

| ID | Decisión | Fecha |
|---|---|---|
| PD-01 | Misión, visión y promesa aprobadas en D-129 | 2026-11-26 |
| PD-19 | Solo español en la versión inicial (D-123) | 2026-11-26 |
| PD-20 | WCAG 2.1 AA en flujos críticos (D-131) | 2026-11-26 |
| PD-21 | URL pública por ruta `/r/{slug}` (D-124) | 2026-11-26 |
| PD-02 | Colombia y Barranquilla como mercado de arranque (D-135, D-136) | 2026-11-27 |
| PD-03 | Cliente ideal: una sede, 5–30 mesas, 3–20 empleados (D-137) | 2026-11-27 |
| PD-05 | Competencia principal: papel/Excel/WhatsApp y POS local (D-138) | 2026-11-27 |
| PD-09 | Sin prueba gratuita; cancelación al final del periodo y sin reembolso salvo fallo (D-141, D-142) | 2026-11-27 |
| PD-30 | Sin descuento de lanzamiento; implementación solo con migración (D-143) | 2026-11-27 |
| PD-10 | Marco de métricas sin metas numéricas hasta tener datos (D-144) | 2026-11-27 |
| PD-06 | Alcance de la versión vendible aprobado (D-121) | 2026-11-27 |
| PD-22 | Matriz de permisos sin cajero aprobada (D-145, D-146) | 2026-11-27 |
| PD-24 | Domicilio con zonas, tarifa fija y entrega propia (D-147) | 2026-11-27 |
| PD-25 | Multi-sucursal fuera de la versión inicial (D-122, D-121) | 2026-11-27 |
| PD-26 | IA fuera de la versión inicial y sin fecha (D-121) | 2026-11-27 |
| PD-27 | Impuestos, propinas y descuentos fuera del cálculo (D-113) | 2026-11-27 |
| PD-11 | Alta asistida con verificación manual y acceso en 48 h (D-149) | 2026-11-27 |
