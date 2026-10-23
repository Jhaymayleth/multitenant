"""Alembic env para el schema global platform."""
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import MetaData, engine_from_config, pool

# Asegurar que el paquete app sea importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import app.audit.models  # noqa: F401
import app.platform.models  # noqa: F401  (registra modelos en Base.metadata)
from app.core.config import Settings
from app.core.database import Base

settings = Settings()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL desde settings (respeta .env)
config.set_main_option("sqlalchemy.url", settings.database_url)

# Solo tablas del schema platform
target_metadata = MetaData()
for table in Base.metadata.tables.values():
    if table.schema == "platform":
        table.to_metadata(target_metadata)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema="platform",
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema="platform",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
