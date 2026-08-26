"""change book_status column type

Revision ID: 0d0cd48a3a5e
Revises: 1a21239ee93f
Create Date: 2026-08-25 23:08:14.767987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d0cd48a3a5e'
down_revision: Union[str, Sequence[str], None] = '1a21239ee93f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE books
        ALTER COLUMN status TYPE book_status
        USING status::book_status
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE books
        ALTER COLUMN status TYPE VARCHAR
        USING status::text
    """)
