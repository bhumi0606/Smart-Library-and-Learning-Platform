"""create book_authors table

Revision ID: b0c8660470da
Revises: 74e1dba9cbdc
Create Date: 2026-08-20 10:35:38.235153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0c8660470da'
down_revision: Union[str, Sequence[str], None] = '74e1dba9cbdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "book_authors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("book_id", sa.Integer, sa.ForeignKey("books.id"), nullable=False),
        sa.Column("author_id", sa.Integer, sa.ForeignKey("authors.id"), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("book_authors")
