# Métricas

**Estado:** Vigente (D-144)
**Última revisión:** 27 de noviembre de 2026
**Dueño:** Producto / Negocio
**Decisión:** D-144

## 1. Métrica norte

**Restaurantes que completan un ciclo operativo real cada semana:** un pedido registrado, preparado y cobrado, con la página pública activa.

No se mide por número de pantallas ni por funciones lanzadas. Se mide por restaurantes que usan Lixus para operar.

El marco de métricas está aprobado en D-144. Las metas numéricas se fijan cuando existan datos reales del piloto; mientras tanto, toda celda “POR DEFINIR” significa “sin dato”, no “objetivo acordado”.

## 2. Métricas de producto

| Métrica | Definición | Meta |
|---|---|---|
| Activación | Restaurante que carga menú, mesas y personal, y registra su primer pedido en 7 días | POR DEFINIR |
| Uso semanal | Restaurantes con al menos un pedido y un pago por semana | POR DEFINIR |
| Profundidad | Módulos usados por restaurante (menú, pedidos, reservas, caja, página) | POR DEFINIR |
| Tiempo de alta | Desde la firma hasta la primera operación | POR DEFINIR |
| Errores por servicio | Incidencias que impiden operar | POR DEFINIR |

## 3. Métricas de negocio

| Métrica | Definición | Meta |
|---|---|---|
| MRR | Ingreso recurrente mensual | POR DEFINIR |
| ARPU | MRR / restaurantes activos | POR DEFINIR |
| Churn mensual | Cancelaciones / restaurantes activos | POR DEFINIR |
| Retención a 3 y 6 meses | Restaurantes que siguen pagando | POR DEFINIR |
| CAC | Costo de adquisición por restaurante | POR DEFINIR |
| LTV | Ingreso esperado antes de cancelar | POR DEFINIR |
| Payback | Meses para recuperar CAC | POR DEFINIR |

## 4. Métricas de soporte y confiabilidad

| Métrica | Definición | Meta |
|---|---|---|
| Disponibilidad | Porcentaje de tiempo operativo | POR DEFINIR |
| Tiempo de primera respuesta | Desde el reporte hasta la respuesta | POR DEFINIR |
| Tiempo de resolución | Desde el reporte hasta la solución | POR DEFINIR |
| Incidentes críticos | Caídas o pérdida de datos | Cero tolerancia |
| Restauración probada | Última prueba de backup exitosa | Mensual |

## 5. Métricas de adquisición

- Contactos, demos y pilotos por semana.
- Conversión de demo a piloto.
- Conversión de piloto a pago.
- Canal de origen.
- Motivo de pérdida.

## 6. Instrumentación mínima

1. Registrar eventos de activación y uso en el backend.
2. Separar métricas por tenant sin exponer datos operativos.
3. Panel interno para el equipo Lixus.
4. Revisión semanal de producto y mensual de negocio.
5. No inventar métricas: si no se mide, se escribe “sin dato”.

## 7. Cadencia

| Revisión | Frecuencia | Quién |
|---|---|---|
| Operación y soporte | Semanal | Operación |
| Producto y activación | Semanal | Producto |
| Negocio y caja | Mensual | Dueño |
| Roadmap | Trimestral | Dueño + Producto |
