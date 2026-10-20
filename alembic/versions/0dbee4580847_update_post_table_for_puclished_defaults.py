"""update post table for puclished defaults

Revision ID: 0dbee4580847
Revises: d22e1be9fb81
Create Date: 2026-10-20 09:24:58.406477

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0dbee4580847"
down_revision: str | Sequence[str] | None = "d22e1be9fb81"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
  op.alter_column(
    "posts",
    "published",
    server_default=sa.text("TRUE"),
    nullable=False,
  )

  # """Upgrade schema."""


def downgrade() -> None:
  op.alter_column(
    "posts",
    "published",
    server_default=sa.text("FALSE"),
    nullable=False,
  )
  # """Downgrade schema."""
