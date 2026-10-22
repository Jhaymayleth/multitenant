"""Configuración del backend de Lixus.

Aquí se leen variables de entorno y se definen valores por defecto para desarrollo.
Quedan listas las secciones que necesitará el proyecto: app, base de datos,
Redis, JWT, archivos, rate limiting, webhooks de pago, etc.
"""

from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {
        "env_file": [".env", "../.env"],
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    # ---- App ----
    app_env: str = "local"
    app_name: str = "Lixus API"
    app_version: str = "0.1.0"
    debug: bool = False

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v: Any) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on", "debug")
        return bool(v)

    # ---- Servidor ----
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # ---- Frontend y API ----
    next_public_app_url: str = "http://localhost:3000"
    api_base_url: str = "http://localhost:8000"

    # ---- Base de datos ----
    db_host: str = "localhost"
    db_port: int = 5433
    db_user: str = "lixus"
    db_password: str = "changeme_local"
    db_name: str = "platform"
    db_pool_min_size: int = 5
    db_pool_max_size: int = 20

    # ---- Redis ----
    redis_url: str = "redis://localhost:6379/0"

    # ---- JWT y sesión ----
    jwt_secret: str = "changeme_jwt_secret_do_not_use_in_prod"
    jwt_algorithm: str = "HS256"
    jwt_access_token_ttl_minutes: int = 60

    # ---- Desarrollo ----
    dev_password_hash: str = "changeme_do_not_use_in_prod"

    # ---- Archivos ----
    files_max_size_mb: int = 5
    files_allowed_image_types: str = "image/jpeg,image/png,image/webp"

    # ---- Rate limiting ----
    rate_limit_login_per_minute: int = 6
    rate_limit_writes_per_minute: int = 30

    # ---- Pagos / webhooks ----
    payment_webhook_secret: str = "changeme_payment_webhook_secret"
    payment_webhook_endpoint: str = "http://localhost:8000/webhooks/payments/sandbox"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


def get_settings() -> Settings:
    return Settings()
