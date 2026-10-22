"""Módulos de la API de Lixus.

Desde aquí se organizan los routers por dominio una vez estén listos:
plataforma, auth, menú, sitios, pedidos, reservas, pagos, webhooks, etc.
"""

from app.api.router import api_router

__all__ = ["api_router"]
