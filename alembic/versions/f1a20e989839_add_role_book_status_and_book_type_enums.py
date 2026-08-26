"""add role, book status and book type enums

Revision ID: f1a20e989839
Revises: 472c4c70d9ec
Create Date: 2026-08-22 14:38:26.551933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a20e989839'
down_revision: Union[str, Sequence[str], None] = '472c4c70d9ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    role_enum = sa.Enum(
        "librarian",
        "member",
        name="role"
    )

    book_status_enum = sa.Enum(
        "available",
        "borrowed",
        "lost",
        "damaged",
        name="book_status"
    )

    book_type_enum = sa.Enum(
        "physical",
        "digital",
        name="book_type"
    )

    role_enum.create(op.get_bind(), checkfirst=True)
    book_status_enum.create(op.get_bind(), checkfirst=True)
    book_type_enum.create(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    """Downgrade schema."""
    book_type_enum = sa.Enum(
        "physical",
        "digital",
        name="book_type"
    )

    book_status_enum = sa.Enum(
        "available",
        "borrowed",
        "lost",
        "damaged",
        name="book_status"
    )

    role_enum = sa.Enum(
        "librarian",
        "member",
        name="role"
    )

    book_type_enum.drop(op.get_bind(), checkfirst=True)
    book_status_enum.drop(op.get_bind(), checkfirst=True)
    role_enum.drop(op.get_bind(), checkfirst=True)
