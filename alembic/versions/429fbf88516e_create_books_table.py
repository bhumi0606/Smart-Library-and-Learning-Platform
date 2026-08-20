"""create books table

Revision ID: 429fbf88516e
Revises: 927f080484e6
Create Date: 2026-08-20 10:28:25.651689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '429fbf88516e'
down_revision: Union[str, Sequence[str], None] = '927f080484e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "books",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("author", sa.String(255), nullable=False),
        sa.Column("published_date", sa.Date, nullable=True),
        sa.Column("isbn", sa.String(13), unique=True, nullable=False),
        sa.Column("book_type", sa.String(100), nullable=True),
        sa.Column("status", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("books")
