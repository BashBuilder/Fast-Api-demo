"""add user table

Revision ID: f493d6e17922
Revises: 26cd710b93f8
Create Date: 2026-10-20 09:03:36.466037

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f493d6e17922"
down_revision: str | Sequence[str] | None = "26cd710b93f8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
  op.create_table(
    "users",
    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
    sa.Column("email", sa.String(), nullable=False),
    sa.Column("password", sa.String(), nullable=False),
    sa.Column(
      "created_at",
      sa.TIMESTAMP(timezone=True),
      server_default=sa.text("now()"),
      nullable=False,
    ),
    sa.UniqueConstraint("email"),
  )


def downgrade() -> None:
  op.drop_table("users")
  """Downgrade schema."""
