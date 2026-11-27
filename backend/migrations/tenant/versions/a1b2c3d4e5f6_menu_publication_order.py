"""Añade publicación y orden a los productos del menú.

Revision ID: a1b2c3d4e5f6
Revises: d6a072ef02e3
Create Date: 2026-11-27

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "d6a072ef02e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "menu_products",
        sa.Column("display_order", sa.SmallInteger(), nullable=False, server_default="0"),
    )
    op.add_column(
        "menu_products",
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.alter_column("menu_products", "display_order", server_default=None)
    op.alter_column("menu_products", "is_published", server_default=None)


def downgrade() -> None:
    op.drop_column("menu_products", "is_published")
    op.drop_column("menu_products", "display_order")
