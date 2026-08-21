"""add role field in members table

Revision ID: 472c4c70d9ec
Revises: 35a6ed88ae51
Create Date: 2026-08-21 13:22:38.528791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '472c4c70d9ec'
down_revision: Union[str, Sequence[str], None] = '35a6ed88ae51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "members",
        sa.Column("role", sa.String(100), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "members",
        sa.Column("role", sa.String(100), nullable=False)
    )