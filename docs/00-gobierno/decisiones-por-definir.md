# Decisiones por definir

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Producto

Cada fila es una pregunta abierta. El default es una propuesta del PO, no una decisión. Ninguna se implementa como definitiva hasta pasar a `decisiones.md`.

| ID | Área | Pregunta | Impacto | Default propuesto | Estado |
|---|---|---|---|---|---|
| PD-02 | Mercado | ¿País y ciudad de arranque? | Precio, legal, soporte, cobro | Colombia, una ciudad piloto | POR DEFINIR |
| PD-03 | Mercado | ¿Qué tamaño y tipo de restaurante es el cliente ideal? | Producto, precio, ventas | Una sede, 5–30 mesas, 3–20 empleados, operación de mesa y domicilio | POR DEFINIR |
| PD-04 | Mercado | ¿Quién decide la compra y quién influye? | Guion comercial y onboarding | Dueño o gerente; influyen administrador y contador | POR DEFINIR |
| PD-05 | Mercado | ¿Cuál es la competencia real y su precio? | Propuesta de valor y pricing | POS locales, cuadernos/Excel/WhatsApp, plataformas de reservas, constructores web | POR DEFINIR |
| PD-06 | Producto | ¿Cuál es el alcance cerrado de la versión que se vende? | Backlog y fecha de lanzamiento | D-121 | POR DEFINIR |
| PD-07 | Negocio | ¿Planes, precios, moneda y ciclo de cobro? | Ingresos y posicionamiento | Tres planes mensuales; cifras a validar con cinco entrevistas | POR DEFINIR |
| PD-08 | Negocio | ¿Cómo se cobra y se factura? | Operación y legal | Transferencia/PSE y factura electrónica local; pasarela de suscripción después | POR DEFINIR |
| PD-09 | Negocio | ¿Prueba gratuita, cancelación y reembolso? | Conversión y riesgo | 14 días de prueba; cancelación al final del periodo; sin reembolso proporcional salvo fallo | POR DEFINIR |
| PD-10 | Negocio | ¿Qué métricas y metas definen el éxito? | Dirección y reportes | Activación en 7 días, churn mensual < 3 %, MRR y NPS | POR DEFINIR |
| PD-11 | Operación | ¿Cómo es el alta y la verificación de un restaurante? | Time-to-value y riesgo | Formulario, llamada de 20 min, documentos del negocio, revisión manual, alta en 48 h | POR DEFINIR |
| PD-12 | Operación | ¿Horario de soporte y SLA? | Expectativa del cliente | Lunes a sábado 9:00–19:00; respuesta < 4 h laborables; crítico < 1 h | POR DEFINIR |
| PD-13 | Operación | ¿Quién hace qué dentro de Lixus? | Responsabilidad y escalamiento | Fundador/producto, ingeniería, operación/soporte y comercial; al inicio pueden coincidir | POR DEFINIR |
| PD-14 | Legal | ¿Jurisdicción y figura legal? | Contratos, impuestos, datos | Colombia, SAS; confirmar con abogado | POR DEFINIR |
| PD-15 | Legal | ¿Régimen de protección de datos aplicable? | Privacidad y contratos | Ley 1581 de Colombia y habeas data; confirmar | POR DEFINIR |
| PD-16 | Legal | ¿Cuánto se conservan datos, auditoría, comprobantes y backups? | Cumplimiento y costo | Operativos mientras haya cuenta + 30 días; auditoría 12 meses; comprobantes 5 años; backups 30 días | POR DEFINIR |
| PD-17 | Legal | ¿Términos, cookies y facturación revisados? | Venta y confianza | Borradores revisados por abogado | POR DEFINIR |
| PD-18 | Marca | ¿Cuál es el dominio exacto y la identidad visual definitiva? | Percepción, correos y certificados | Nombre «Lixus» y dominio propio aprobados (D-130); falta el dominio exacto y la paleta/logotipo. | POR DEFINIR |
| PD-21 | Producto | ¿URL pública por ruta o subdominio? | DNS, TLS, marca | `/r/{slug}` en la versión inicial | POR DEFINIR |
| PD-22 | Producto | ¿Matriz definitiva de permisos del restaurante? | Autorización y UI | La propuesta de `04-backend/features/personal-permisos.md` | POR DEFINIR |
| PD-23 | Operación | ¿Proveedor de correo transaccional? | Invitaciones, códigos y avisos | Resend o Postmark, detrás de una interfaz | POR DEFINIR |
| PD-24 | Producto | ¿Reglas de domicilio: cobertura, tarifa y entrega? | Módulo de domicilios | Zonas, tarifa fija, entrega propia, pago registrado | POR DEFINIR |
| PD-25 | Producto | ¿Multi-sucursal en la versión inicial? | Modelo de datos y UI | Fuera de la versión inicial | POR DEFINIR |
| PD-26 | Producto | ¿IA dentro de la versión inicial? | Costo, riesgo y foco | Fuera; evaluar después con proveedor y límites | POR DEFINIR |
| PD-27 | Producto | ¿Impuestos, propinas y descuentos? | Caja y comprobantes | Fuera; el restaurante los maneja aparte | POR DEFINIR |
| PD-28 | Legal | ¿Exportación y eliminación de datos de un tenant? | Contratos y operación | Exportación CSV/JSON bajo solicitud; eliminación a los 30 días de cancelar, salvo obligación legal | POR DEFINIR |
| PD-29 | Operación | ¿RPO, RTO y retención de backups? | Continuidad | RPO 24 h, RTO 4 h, backups diarios por 30 días | POR DEFINIR |
| PD-30 | Negocio | ¿Habrá descuento de lanzamiento o cobro de implementación? | Ingreso y adopción | No descontar; cobrar implementación solo si hay migración de datos | POR DEFINIR |

## Cerradas

| ID | Decisión | Fecha |
|---|---|---|
| PD-01 | Misión, visión y promesa aprobadas en D-129 | 2026-11-26 |
| PD-19 | Solo español en la versión inicial (D-123) | 2026-11-26 |
| PD-20 | WCAG 2.1 AA en flujos críticos (D-131) | 2026-11-26 |
