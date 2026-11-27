# Estrategia de pruebas

**Estado:** Parcial
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería

## 1. Pirámide

| Nivel | Qué prueba | Herramienta | Estado |
|---|---|---|---|
| Unitario | Reglas, cálculos, validaciones | pytest | Mínimo |
| Integración | API + PostgreSQL + Redis | pytest | Parcial |
| Seguridad | Aislamiento, permisos, sesión | pytest | Parcial |
| Contrato | Esquemas de entrada y salida | pytest | No |
| Frontend | Componentes y flujos | Por definir | No |
| End-to-end | Login, pedido, cobro, reserva | Playwright (propuesto) | No |
| Manual | Operación real con piloto | Checklist | No |

## 2. Pruebas obligatorias del backend

### Aislamiento

La matriz completa y su ejecución en CI están en [`aislamiento.md`](aislamiento.md) (BL-08).

- Usuario de A no lee datos de B.
- Token de A no abre ruta de B.
- `schema_name` inválido se rechaza.
- `search_path` no se filtra entre peticiones concurrentes.

### Autenticación

- Login correcto e incorrecto.
- Cookie `httpOnly`.
- Ruta privada sin sesión → 401.
- Empleado desactivado → sin acceso.
- Cambio de tenant emite token nuevo.

### Pedidos

- Pedido sin líneas → rechazo.
- Total calculado en servidor.
- Precio congelado.
- Pedido de otro tenant → rechazo.
- Cambio de estado permitido por rol.

### Pagos

- Pago duplicado → rechazo.
- Confirmación libera mesa.
- Comprobante con token válido y vencido.
- Webhook sin firma → rechazo.

### Robustez

- Idempotencia: misma clave, mismo cuerpo → misma respuesta.
- Misma clave, cuerpo distinto → 409.
- Rate limit: exceso → 429 con `Retry-After`.
- Redis caído → degradación controlada.

### Reservas

- Solapamiento → 409.
- Disponibilidad pública.
- No-show registrado.

## 3. Pruebas de frontend

- Login y guard.
- Formulario de menú.
- Pedido con líneas.
- Cobro y comprobante.
- Estados de carga, error y vacío.
- Accesibilidad con teclado.

## 4. Pruebas manuales

Antes de cada release:

1. Crear un tenant.
2. Cargar menú y mesas.
3. Registrar un pedido.
4. Verlo en cocina.
5. Cobrar y descargar comprobante.
6. Reservar desde la página pública.
7. Verificar aislamiento con dos tenants.
8. Restaurar un backup en entorno aislado.

## 5. Cobertura

- No hay medición actual.
- Propuesta: 70 % en servicios y 50 % global.
- La cobertura no sustituye pruebas de comportamiento.

## 6. CI

- Ruff y pytest en backend.
- Lint y build en frontend.
- Build de imágenes.
- Faltan pruebas de frontend, cobertura y mypy.

## 7. Regla

Una feature no se marca `EN PRODUCCIÓN` si no tiene al menos una prueba automatizada de su flujo crítico o una verificación manual documentada.
