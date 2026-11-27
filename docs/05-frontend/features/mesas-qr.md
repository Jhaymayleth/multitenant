# Feature: mesas y QR (frontend)

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/mesas-qr.md`
**Especificación de la feature:** [`mesas-qr-api.md`](../mesas-qr-api.md) (BL-05)
**Decisiones:** D-157, D-158, D-159, D-160

## 1. Objetivo

Que el mesero vea el salón de un vistazo y que el cliente pueda pedir atención desde la mesa sin descargar nada.

## 2. Pantallas

| Pantalla | Ruta | Función |
|---|---|---|
| Salón | `/admin/mesas` | Mapa o lista de mesas |
| Mesa | `/admin/mesas/{id}` | Estado, sesión y solicitudes |
| QR | modal | Descargar o imprimir |
| Mesa del cliente | `/r/{slug}/mesa/{token}` | Solicitudes |

## 3. Estados de mesa

- Disponible: verde, acción «ocupar mesa».
- Ocupada y pendiente de pago: rojo, acción «liberar mesa».
- Reservada: azul, solo si el tenant activó reservas (D-160).
- Inactiva: sin acción.

Las tarjetas se agrupan por piso y zona opcional, con la etiqueta visible generada por el backend (D-157, D-158). El mesero no busca un ID: ve la mesa y toca la acción.

## 4. Flujos

### Abrir mesa

1. El mesero toca «ocupar mesa» en la tarjeta.
2. Se crea o reanuda la sesión.
3. La mesa pasa a ocupada y la tarjeta a rojo.

### Solicitud del cliente

1. El cliente escanea el QR.
2. Elige “llamar al mesero”, “falta algo” o “pedir la cuenta”.
3. El mesero ve la solicitud con hora y mesa.

### Cerrar mesa

1. El mesero toca «liberar mesa» y escribe el motivo.
2. Si hay pedido sin cobrar, el sistema lo bloquea y explica por qué; si se fuerza, queda registrado (D-159).
3. La mesa pasa a disponible, la tarjeta a verde y la sesión se cierra.
4. El cobro confirmado por webhook cierra la mesa sin intervención manual.

## 5. Criterios de aceptación

- [ ] El salón muestra el estado actualizado.
- [ ] El QR se descarga e imprime.
- [ ] El cliente ve su mesa correcta.
- [ ] La solicitud llega al panel.
- [ ] Una mesa ocupada no se abre dos veces.
- [ ] El mesero puede liberar con motivo y sin pedido pendiente.
- [ ] La etiqueta y el color permiten identificar la mesa sin buscar un ID.
- [ ] El esquema de etiquetas y las zonas los configura el restaurante.

## 6. Estado actual

La página es informativa. El endpoint público del QR devuelve un mensaje fijo y no consulta la base de datos.
