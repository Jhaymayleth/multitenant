# Propuesta de valor

**Estado:** Borrador
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Producto

## 1. Promesa central

> Lixus pone en orden la operación diaria del restaurante y le da una página pública profesional, sin obligarlo a comprar un sistema empresarial.

## 2. Pilares

### 2.1 Orden operativo

Menú, mesas, pedidos, cocina y cobro comparten la misma información. El equipo deja de reconstruir lo que pasó y empieza a ver lo que está pasando.

### 2.2 Presencia digital incluida

Cada restaurante tiene una página pública con su marca, menú, horarios y contacto. No es un sitio a medida ni un constructor complejo: es una plantilla que el restaurante personaliza y publica.

### 2.3 Simplicidad operativa

La interfaz está en español, los flujos son cortos y el onboarding es asistido. El restaurante no necesita un administrador de sistemas.

### 2.4 Confianza y aislamiento

Cada restaurante tiene su propio schema. Lixus no comparte datos entre tenants ni los usa para publicidad. La plataforma administra el servicio, no la operación del restaurante.

### 2.5 Precio predecible

Suscripción mensual por restaurante, sin comisión por pedido ni cobros escondidos. El precio exacto está por definir en PD-07.

## 3. Por qué Lixus y no otra cosa

| Alternativa | Lo que falla | Lo que Lixus aporta |
|---|---|---|
| Cuaderno, Excel y WhatsApp | No hay una sola verdad; se pierde información | Datos compartidos entre operación y cobro |
| POS empresarial | Costoso, complejo, pensado para cadenas | Producto enfocado en una sede independiente |
| Plataforma de reservas | Solo cubre reservas | Operación completa y página pública |
| Constructor web | Página bonita sin operación | Página conectada al menú y al restaurante |
| App de reparto | Solo cubre el canal de domicilio | Mesa, pedidos, reservas y página pública; el domicilio lo resuelve el restaurante |

## 4. Pruebas de valor

El valor debe demostrarse con hechos observables, no con adjetivos:

- El restaurante publica su menú y su página en menos de 48 horas.
- El mesero registra un pedido y cocina lo ve sin llamadas.
- El cobro del pedido se confirma y la mesa queda libre sin recalcular.
- El dueño consulta el estado del día desde el panel.
- El cliente reserva o pide sin crear una cuenta en otro sistema.

## 5. Objeciones previsibles

| Objeción | Respuesta |
|---|---|
| “Ya tengo un POS.” | Lixus no reemplaza la contabilidad; ordena la operación y la presencia digital. Se puede integrar después. |
| “Es otra cosa que aprender.” | Onboarding asistido y flujos de una pantalla. Si el equipo sabe usar WhatsApp, sabe usar Lixus. |
| “¿Mis datos están seguros?” | Aislamiento por schema, sesión httpOnly y acceso restringido. La política legal se detalla en `08-legal/`. |
| “¿Y si cierro?” | Los datos se conservan y se pueden exportar. La eliminación se pacta en el contrato. |
| “Es caro.” | El precio se compara contra el costo de los errores y el tiempo perdido, no contra un cuaderno. |

## 6. Lo que no prometemos

- Manejar efectivo, arqueo ni dinero de los pedidos.
- Facturación fiscal.
- Inventario o control de stock.
- Gestión de domicilio y reparto (D-155).
- IA que opere el restaurante sola.
- Múltiples sucursales en la versión inicial.
