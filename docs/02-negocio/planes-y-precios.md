# Planes y precios

**Estado:** Borrador
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Producto / Negocio
**Decisión abierta:** PD-07

> Documento corporativo. Se genera también en `.docx` cuando se cierre el contenido.
> **No hay precios aprobados.** Las cifras se escriben solo después de validarlas con clientes. La estructura de tres planes está aprobada en D-139.

## 1. Estructura propuesta

Tres planes aprobados en su forma, con nombres provisionales:

| Capacidad | Básico | Pro | Plus |
|---|---|---|---|
| Menú y categorías | Sí | Sí | Sí |
| Página pública | Sí | Sí | Sí |
| Mesas y QR | Hasta un límite por definir | Hasta un límite por definir | Sin límite operativo razonable |
| Pedidos y cocina | Sí | Sí | Sí |
| Reservas | No | Sí | Sí |
| Cobro por pasarela del restaurante y comprobantes | No | Sí | Sí |
| Personal y roles | Hasta un límite por definir | Hasta un límite por definir | Hasta un límite por definir |
| Reportes | Básicos | Operativos | Operativos + exportación |
| Almacenamiento de imágenes | Límite por definir | Límite por definir | Límite por definir |
| Soporte | Horario estándar | Horario estándar | Prioritario |
| Precio mensual | POR DEFINIR | POR DEFINIR | POR DEFINIR |

## 2. Límites que deben definirse

- Número de mesas por plan.
- Número de empleados por plan.
- Número de productos y categorías.
- Almacenamiento de imágenes.
- Número de reservas o pedidos al mes, si se decide limitar.
- Usuarios simultáneos.
- Retención de reportes.

Los límites deben expresarse en lenguaje del restaurante (“hasta 20 mesas”), no en unidades técnicas.

## 3. Moneda y ciclo

- **Moneda:** POR DEFINIR (depende de PD-02).
- **Ciclo:** mensual por defecto; anual con descuento a definir.
- **Cobro:** anticipado.
- **Facturación:** electrónica local, según jurisdicción.
- **Impuestos:** se muestran en la factura según la ley aplicable.

## 4. Implementación

- Onboarding estándar: incluido en el primer mes.
- Migración de menú desde Excel o PDF: tarifa única POR DEFINIR (se cobra según D-143).
- Capacitación adicional: tarifa por sesión POR DEFINIR.
- Integraciones a medida: cotización separada.

## 5. Prueba, cancelación y reembolso

| Tema | Propuesta | Estado |
|---|---|---|
| Prueba | Sin prueba gratuita; se paga desde el primer día (D-141) | APROBADA |
| Fin de prueba | No aplica | APROBADA |
| Cancelación | Al final del periodo pagado (D-142) | APROBADA |
| Reembolso | Solo por fallo atribuible a Lixus (D-142) | APROBADA |
| Reactivación | Inmediata al pagar | POR DEFINIR |
| Datos al cancelar | Conservación y exportación según contrato | POR DEFINIR |

## 6. Cómo validar el precio

1. Entrevistar al menos cinco restaurantes del segmento.
2. Preguntar por el costo actual de los errores y del tiempo perdido.
3. Presentar tres opciones de precio, no una.
4. Medir intención de compra, no solo agrado.
5. Probar con un piloto pagado antes de publicar tarifas.

## 7. Reglas de publicación

- No se publica un precio sin aprobación del dueño.
- No se promete “sin límites” si existe un límite técnico.
- No se comparan precios de competidores sin fuente y fecha.
- Todo cambio de precio se registra en `00-gobierno/decisiones.md`.
