# Modelo de negocio

**Estado:** Borrador
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Producto / Negocio
**Decisiones abiertas:** PD-07, PD-08, PD-09, PD-30

> Documento corporativo. Se genera también en `.docx` cuando se cierre el contenido.

## 1. Cómo gana dinero Lixus

Lixus cobra una **suscripción mensual por restaurante**. El restaurante paga por usar la plataforma; su personal y sus clientes no pagan licencia.

Fuentes de ingreso previstas:

1. Suscripción mensual o anual por tenant.
2. Implementación o migración de datos, solo cuando el cliente la necesita.
3. Servicios adicionales acordados (contenido, capacitación, integraciones), fuera del producto base.

No se cobra comisión por pedido en la versión inicial. No se procesan pagos de clientes finales. No se venden datos ni publicidad.

## 2. Por qué suscripción y no comisión

- El restaurante necesita un costo predecible.
- La comisión por pedido castiga al restaurante que más vende y desincentiva el uso.
- El valor está en la operación diaria, no en una transacción aislada.
- La suscripción permite invertir en soporte y estabilidad.

## 3. Estructura de costos

| Costo | Naturaleza | Control |
|---|---|---|
| Infraestructura (cómputo, RDS, Redis, almacenamiento) | Variable con el número de tenants | Derecho de uso, límites por plan y monitoreo |
| Correo transaccional | Variable | Proveedor con capa gratuita y control de envíos |
| Soporte | Fijo y variable | Documentación, onboarding repetible y horario definido |
| Adquisición | Variable | Venta directa y referidos; sin publicidad masiva al inicio |
| Legal y contable | Fijo | Revisión externa anual |
| Desarrollo | Fijo | Equipo pequeño y alcance cerrado |

Las cifras concretas están por definir. No se presentan números sin facturas, cotizaciones o datos reales.

## 4. Economía unitaria (marco)

Para saber si el negocio funciona se deben medir:

- **ARPU:** ingreso medio por restaurante al mes.
- **CAC:** costo de adquirir un restaurante.
- **Margen bruto:** ingreso menos infraestructura, correo y soporte directo.
- **Churn:** restaurantes que cancelan por mes.
- **LTV:** ingreso esperado por restaurante antes de cancelar.
- **Payback:** meses para recuperar el CAC.

Las metas numéricas están en `02-negocio/metricas.md` y se fijan cuando existan datos reales.

## 5. Lógica de precios

- Precio basado en valor, no en costo.
- Tres planes como máximo para evitar parálisis.
- Límites claros: mesas, personal, almacenamiento y funciones.
- El plan inicial debe ser suficientemente completo para operar; no se cobra por funciones básicas como el menú o la página pública.
- El precio se valida con entrevistas antes de publicarse.

Detalle en `02-negocio/planes-y-precios.md`.

## 6. Política comercial

| Tema | Propuesta | Estado |
|---|---|---|
| Prueba | Sin prueba gratuita; implantación acompañada desde el primer día (D-141) | APROBADA |
| Cobro | Mensual; anual con descuento a definir | POR DEFINIR |
| Cancelación | Al final del periodo contratado (D-142) | APROBADA |
| Reembolso | Solo por fallo atribuible a Lixus (D-142) | APROBADA |
| Impuestos | Facturación local según jurisdicción | POR DEFINIR |
| Descuento de lanzamiento | No se aplica (D-143) | APROBADA |

## 7. Qué tiene que ser verdad

1. El restaurante percibe valor en la primera semana.
2. El costo de soporte por restaurante baja con el onboarding repetible.
3. El churn mensual se mantiene bajo.
4. El precio cubre infraestructura, soporte y adquisición.
5. El producto no depende de una sola persona para operar.

## 8. Riesgos del modelo

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Precio demasiado bajo | No cubre soporte | Validar disposición a pagar antes de publicar |
| Cliente que exige desarrollo a medida | Distorsiona el producto | Alcance cerrado y tarifa de implementación |
| Churn por falta de adopción | Ingreso inestable | Onboarding y métricas de uso |
| Dependencia de un proveedor | Costo o continuidad | Capa de abstracción y plan B |
| Impago | Flujo de caja | Cobro anticipado y suspensión definida |
