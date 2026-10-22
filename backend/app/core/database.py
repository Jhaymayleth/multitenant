"""Configuración de base de datos multitenant (SQLAlchemy).

Basado en:
- docs/02-DECISIONES.md (D-042: Schema por tenant)
- docs/03-ARQUITECTURA.md (Sección 2.4: search_path con SET LOCAL por transacción)
- docs/07-MODELO-DATOS.md

Regla clave:
Cada transacción de tenant ejecuta `set_config('search_path', :sp, true)` (SET LOCAL),
asegurando que el cambio de schema no contamine las conexiones reutilizadas en el pool.
"""

from __future__ import annotations

import re
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import Settings

SAFE_SCHEMA_REGEX = re.compile(r"^tenant_[a-f0-9]{12}$")

settings = Settings()

def get_database_url() -> str:
    return settings.database_url

engine = create_engine(
    get_database_url(),
    pool_size=settings.db_pool_min_size,
    max_overflow=settings.db_pool_max_size - settings.db_pool_min_size,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos ORM de SQLAlchemy."""
    pass


def set_tenant_schema(session: Session, schema_name: str) -> None:
    """Configura el search_path local a la transacción para el schema del tenant.
    
    Usa set_config(..., true) que equivale a SET LOCAL en PostgreSQL.
    Solo aplica durante la transacción activa, evitando fuga entre conexiones del pool.
    """
    if not SAFE_SCHEMA_REGEX.match(schema_name):
        raise ValueError(f"Nombre de schema de tenant inválido: {schema_name}")

    # Prioridad: schema del tenant, luego platform (global), luego public
    search_path = f'"{schema_name}", platform, public'
    session.execute(
        text("SELECT set_config('search_path', :sp, true)"),
        {"sp": search_path},
    )


def get_db() -> Generator[Session, None, None]:
    """Generador de sesión de base de datos para inyección de dependencias."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
