"""Esquemas base y uniformes para respuestas de la API.

Basado en docs/04-MODULOS.md y docs/09-ROBUSTEZ.md.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict | list | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    message: str | None = None


class MessageResponse(BaseModel):
    message: str

