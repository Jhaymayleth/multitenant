"""Alembic env para schemas tenant_<id>."""
import os
import sys
from logging.config import fileConfig

from sqlalchemy import MetaData, engine_from_config, pool, text

from alembic import context

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.core.config import Settings
from app.core.database import Base
import app.menus.models  # noqa: F401
import app.tables.models  # noqa: F401
import app.orders.models  # noqa: F401
import app.reservations.models  # noqa: F401
import app.payments.models  # noqa: F401
import app.sites.models  # noqa: F401
import app.staff.models  # noqa: F401

settings = Settings()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.database_url)

# Schema objetivo (pasado via -x schema=tenant_xxx)
xargs = context.get_x_argument(as_dictionary=True)
schema = xargs.get("schema", "tenant_aaaaaaaaaaaa")

# Solo tablas tenant (sin schema fijo)
target_metadata = MetaData()
for table in Base.metadata.tables.values():
    if table.schema not in ("platform",):
        # excluir tablas de platform; tenant tables have schema None
        if table.schema is None:
            table.to_metadata(target_metadata)

SAFE = __import__("re").compile(r"^tenant_[a-f0-9]{12}$")
if not SAFE.match(schema):
    raise ValueError(f"Schema de tenant invalido: {schema}")


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=schema,
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
            version_table_schema=schema,
        )
        with context.begin_transaction():
            connection.execute(text(f'SET search_path TO "{schema}"'))
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
