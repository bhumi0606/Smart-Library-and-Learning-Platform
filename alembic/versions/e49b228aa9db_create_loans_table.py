"""create loans table

Revision ID: e49b228aa9db
Revises: 333851f00a92
Create Date: 2026-08-20 10:37:43.683901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e49b228aa9db'
down_revision: Union[str, Sequence[str], None] = '333851f00a92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "loans",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("member_id", sa.Integer, sa.ForeignKey("members.id"), nullable=False),
        sa.Column("book_id", sa.Integer, sa.ForeignKey("books.id"), nullable=False),
        sa.Column("issued_at", sa.DateTime, nullable=False),
        sa.Column("due_date", sa.DateTime, nullable=False),
        sa.Column("return_date", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("loans")
