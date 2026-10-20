"""create posts table

Revision ID: 26cd710b93f8
Revises:
Create Date: 2026-10-20 08:24:25.636349

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "26cd710b93f8"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
  op.create_table(
    "posts",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("title", sa.String(), nullable=False),
    sa.Column("content", sa.String(), nullable=False),
    sa.Column("published", sa.Boolean(), nullable=False),
    sa.Column("created_at", TIMESTAMP(), nullable=False),
    # sa.Column("owner_id", sa.Integer(), nullable=False),
    # sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
  )
  # """Upgrade schema."""


def downgrade() -> None:
  op.drop_table("posts")
  # """Downgrade schema."""
