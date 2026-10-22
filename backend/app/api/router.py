from __future__ import annotations

from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.platform import router as platform_router
from app.api.auth import router as auth_router
from app.api.menus import router as menus_router
from app.api.sites import router as sites_router
from app.api.orders import router as orders_router
from app.api.reservations import router as reservations_router
from app.api.payments import router as payments_router
from app.api.webhooks import router as webhooks_router
from app.api.lixus_requests import router as lixus_requests_router

api_router = APIRouter()

# ---- Plataforma y Lixus ----
api_router.include_router(platform_router)
api_router.include_router(auth_router)
api_router.include_router(lixus_requests_router)

# ---- Tenant ----
api_router.include_router(menus_router)
api_router.include_router(sites_router)
api_router.include_router(orders_router)
api_router.include_router(reservations_router)
api_router.include_router(payments_router)
api_router.include_router(webhooks_router)
