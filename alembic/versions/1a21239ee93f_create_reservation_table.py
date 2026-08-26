"""create reservation table

Revision ID: 1a21239ee93f
Revises: 8ecaf613a4ce
Create Date: 2026-08-24 22:28:14.202993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a21239ee93f'
down_revision: Union[str, Sequence[str], None] = 'f1a20e989839'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "reservations",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            index=True,
        ),

        sa.Column(
            "member_id",
            sa.Integer(),
            sa.ForeignKey("members.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),

        sa.Column(
            "book_id",
            sa.Integer(),
            sa.ForeignKey("books.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),

        sa.Column(
            "reserved_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.Column(
            "status",
            sa.String(20),
            nullable=False,
            server_default="active",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("reservations")
