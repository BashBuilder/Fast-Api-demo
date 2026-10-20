"""add foreign key to post table

Revision ID: d22e1be9fb81
Revises: f493d6e17922
Create Date: 2026-10-20 09:09:25.941175

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d22e1be9fb81"
down_revision: str | Sequence[str] | None = "f493d6e17922"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
  op.add_column(
    "posts",
    sa.Column(
      "owner_id",
      sa.Integer(),
      sa.ForeignKey("users.id", ondelete="CASCADE"),
      nullable=False,
    ),
  )

  # op.create_foreign_key(
  #   "posts_owner_id_fkey",
  #   "posts",
  #   "users",
  #   ["owner_id"],
  #   ["id"],
  #   ondelete="CASCADE",
  # )
  # """Upgrade schema."""


def downgrade() -> None:
  # op.drop_constraint("posts_owner_id_fkey", table_name="posts")
  op.drop_column("posts", "owner_id")
  # """Downgrade schema."""
