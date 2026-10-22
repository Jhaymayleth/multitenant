"""Punto de entrada de la API de Lixus.

Configura la aplicación FastAPI, middlewares de seguridad, CORS con soporte de cookies
y monta los routers de dominio según la arquitectura multitenant decidida.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import Settings
from app.core.errors import AppError, app_error_handler, register_exception_handlers
from app.health.router import router as health_router

settings = Settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 1. Configuración de CORS con credenciales permitidas (HttpOnly cookies)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            settings.next_public_app_url,
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Manejo de excepciones uniforme
    register_exception_handlers(app)
    app.add_exception_handler(AppError, app_error_handler)

    # 3. Health check directo en la raíz para Docker / orquestadores
    app.include_router(health_router)

    # 4. Enrutador principal versionado bajo /api/v1
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
