"""add run table"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "8c5ef4639df1"
down_revision = "72356bc9b2a0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "runs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("started_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("runs")
