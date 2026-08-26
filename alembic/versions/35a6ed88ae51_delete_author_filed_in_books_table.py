"""delete author filed in books table

Revision ID: 35a6ed88ae51
Revises: d87828fb6d25
Create Date: 2026-08-20 12:56:17.887177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35a6ed88ae51'
down_revision: Union[str, Sequence[str], None] = 'd87828fb6d25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('books', 'author')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('books', sa.Column('author', sa.String(255), nullable=False))
