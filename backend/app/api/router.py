"""Router principal de la API de Lixus.

Agrupa todos los dominios de negocio definidos en docs/03-ARQUITECTURA.md:
- Global/Platform: Lixus, planes, aprovisionamiento, auditoría
- Auth & Sesión: login, cookies httpOnly, cambio de tenant
- Tenant Operativo: menú, mesas y QR, pedidos, reservas, caja ligera, personal, configuración
- Público: páginas públicas del restaurante, resolución por subdominio, solicitudes QR
- Webhooks: eventos externos firmados
"""

from __future__ import annotations

from fastapi import APIRouter

from app.audit.router import router as audit_router
from app.auth.router import router as auth_router
from app.health.router import router as health_router
from app.menus.router import router as menus_router
from app.orders.router import router as orders_router
from app.payments.router import router as payments_router
from app.platform.router import router as platform_router
from app.public.router import router as public_router
from app.reservations.router import router as reservations_router
from app.sites.router import router as sites_router
from app.staff.router import router as staff_router
from app.tables.router import router as tables_router
from app.webhooks.router import router as webhooks_router

api_router = APIRouter()

# 1. Monitoreo y salud
api_router.include_router(health_router)

# 2. Plataforma global (Lixus SaaS)
api_router.include_router(platform_router)
api_router.include_router(audit_router)

# 3. Autenticación y sesión
api_router.include_router(auth_router)

# 4. Módulos de gestión del tenant (CEO, meseros, cajeros, cocineros)
api_router.include_router(menus_router)
api_router.include_router(tables_router)
api_router.include_router(orders_router)
api_router.include_router(reservations_router)
api_router.include_router(payments_router)
api_router.include_router(staff_router)
api_router.include_router(sites_router)

# 5. Endpoints públicos y webhooks
api_router.include_router(public_router)
api_router.include_router(webhooks_router)
