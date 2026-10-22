"""Errores y handlers de excepciones del backend.

Aquí se define el formato uniforme de error y los handlers base.
Más adelante se registra AppError, los errores de validación y los de negocio.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(Exception)(_default_exception_handler)


async def _default_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Error interno del servidor",
            }
        },
    )


class AppError(Exception):
    def __init__(self, *, code: str, message: str, status_code: int = 400, details=None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )
