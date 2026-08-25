"""create enrollments table

Revision ID: d87828fb6d25
Revises: e49b228aa9db
Create Date: 2026-08-20 12:23:37.937665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd87828fb6d25'
down_revision: Union[str, Sequence[str], None] = 'e49b228aa9db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "enrollments",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("member_id", sa.Integer(),sa.ForeignKey("members.id"), nullable=False),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id"), nullable=False),
        sa.Column("enrolled_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("enrollments")
