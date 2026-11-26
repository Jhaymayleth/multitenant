# Feature: mesas y QR (frontend)

**Estado:** PARCIAL
**Dueño:** Ingeniería
**Documento backend:** `04-backend/features/mesas-qr.md`

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

- Disponible.
- Ocupada.
- Pendiente de pago.
- Reservada.
- Inactiva.

Cada estado tiene color, texto y acción permitida.

## 4. Flujos

### Abrir mesa

1. El mesero toca la mesa.
2. Se crea o reanuda la sesión.
3. La mesa pasa a ocupada.

### Solicitud del cliente

1. El cliente escanea el QR.
2. Elige “llamar al mesero”, “falta algo” o “pedir la cuenta”.
3. El mesero ve la solicitud con hora y mesa.

### Cerrar mesa

1. Se confirma el pago.
2. La mesa pasa a disponible.
3. La sesión se cierra.

## 5. Criterios de aceptación

- [ ] El salón muestra el estado actualizado.
- [ ] El QR se descarga e imprime.
- [ ] El cliente ve su mesa correcta.
- [ ] La solicitud llega al panel.
- [ ] Una mesa ocupada no se abre dos veces.
- [ ] El mesero puede liberar con motivo.

## 6. Estado actual

La página es informativa. El endpoint público del QR devuelve un mensaje fijo y no consulta la base de datos.
