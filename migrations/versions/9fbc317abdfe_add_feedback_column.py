"""add feedback column"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "9fbc317abdfe"
down_revision = "8c5ef4639df1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("scores", sa.Column("feedback", sa.Integer()))


def downgrade() -> None:
    op.drop_column("scores", "feedback")
