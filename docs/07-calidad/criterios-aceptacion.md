# Criterios de aceptación

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Producto / Ingeniería
**Decisión:** D-125

## 1. Definición de terminado

Una feature está terminada cuando:

1. Cumple su objetivo y sus reglas de negocio.
2. Tiene validación en el backend.
3. Respeta el aislamiento y los permisos.
4. Tiene estados de carga, error y vacío en el frontend.
5. Tiene prueba automatizada o verificación manual documentada.
6. Está documentada en backend y frontend.
7. Se probó en local y en CI.
8. No deja deuda P0 sin registrar.

## 2. Criterios globales de la versión vendible

- [ ] Un restaurante nuevo se crea, verifica y opera sin SQL manual.
- [ ] Dos tenants están aislados, incluso con intentos cruzados.
- [ ] El CEO carga menú, mesas y personal.
- [ ] El mesero registra un pedido con total correcto.
- [ ] Cocina ve y actualiza el pedido.
- [ ] El cobro se confirma por webhook, libera la mesa y emite comprobante.
- [ ] El cliente consulta la página y reserva.
- [ ] La sesión es httpOnly, Secure y con CSRF.
- [ ] Hay rate limiting en login y escrituras.
- [ ] Hay idempotencia en pedidos y pagos.
- [ ] Hay backup y restauración probados.
- [ ] El cliente firma términos y privacidad.

## 3. Criterios por feature

Cada ficha en `04-backend/features/` y `05-frontend/features/` tiene su propia lista. No se acepta una feature con criterios vacíos.

## 4. Criterios de release

- CI verde.
- Migraciones probadas.
- Backup reciente.
- Variables de entorno revisadas.
- Healthcheck correcto.
- Rollback posible.
- Changelog actualizado.
- Cliente informado si hay cambio visible.

## 5. Criterios de rechazo

- Funciona solo en local.
- Depende de un dato cargado a mano.
- Expone datos de otro tenant.
- No tiene manejo de error.
- No se puede explicar al cliente.
- Promete algo que no existe.

## 6. Regla de estado

`EN PRODUCCIÓN` exige uso real. `PARCIAL` es lo que existe pero no cumple. `NO INICIADO` es lo que está en alcance sin código. `PLANIFICADO` es futuro. `DESCARTADO` es decisión explícita.
