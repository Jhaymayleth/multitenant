# Áreas del frontend

**Estado:** Vigente
**Última revisión:** 26 de noviembre de 2026
**Dueño:** Ingeniería
**Decisiones:** D-102, D-108

## 1. Tres caras, un solo frontend

| Área | Ruta base | Usuario | Objetivo |
|---|---|---|---|
| Web pública | `/r/{slug}` (D-124) | Visitante y comensal | Ver menú, información y reservar |
| Panel del CEO | `/admin` | CEO y personal | Operar el restaurante |
| Portal Lixus | `/portal` y `/solicita` | Equipo Lixus y solicitante | Administrar la plataforma y captar |

## 2. Estructura actual

```text
frontend/src/app/
├── (auth)/login
├── (ceo-portal)/admin
│   ├── page.tsx
│   ├── menu
│   ├── mesas
│   ├── pedidos
│   └── configuracion
├── (lixus)/solicita
├── (lixus)/portal
│   ├── page.tsx
│   ├── tenants
│   └── planes
└── (public-site)/menu
    ├── reservas
    └── mesa/[token]
```

## 3. Principios de interfaz

1. **Operación primero:** la pantalla principal del panel es el estado del día, no un dashboard decorativo.
2. **Pocos toques:** el mesero registra un pedido con el mínimo de pasos.
3. **Estado visible:** mesa, pedido y pago se entienden de un vistazo.
4. **Errores claros:** qué pasó y qué hacer.
5. **Móvil primero en operación:** el mesero y el personal de cocina usan teléfono o tablet.
6. **Español:** toda la interfaz, salvo decisión contraria.

## 4. Autenticación en el frontend

- El login envía credenciales a `/api/v1/auth/login`.
- La cookie la maneja el navegador; el frontend no guarda tokens.
- Las rutas privadas verifican sesión en el servidor y en el cliente.
- El panel del CEO exige rol y tenant activo.
- El portal Lixus exige credencial de plataforma.

## 5. Estado actual

- Las páginas son estáticas y no consumen la API.
- No existe `src/lib/api.ts`.
- El login no tiene `onSubmit`.
- `/admin` no tiene guard.
- No hay estados de carga, error ni vacío.
- No hay componentes compartidos.

## 6. Deuda de frontend

- Conectar la API.
- Crear cliente HTTP con manejo de errores.
- Guards de sesión y rol.
- Sistema de componentes.
- Pruebas de interfaz.
- Accesibilidad.

Ver `07-calidad/deuda-tecnica.md`.
