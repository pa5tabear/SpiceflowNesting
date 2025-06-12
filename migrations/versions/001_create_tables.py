"""initial tables"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False, unique=True),
        sa.Column("url", sa.String, nullable=False),
    )
    op.create_table(
        "listings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("source_id", sa.Integer, sa.ForeignKey("sources.id")),
        sa.Column("source_uid", sa.String, nullable=False),
        sa.Column("url", sa.String, nullable=False),
        sa.Column("title", sa.String),
        sa.Column("price", sa.Integer),
        sa.Column("beds", sa.Float),
        sa.Column("baths", sa.Float),
        sa.Column("sqft", sa.Integer),
        sa.Column("lat", sa.Float),
        sa.Column("lon", sa.Float),
        sa.Column("amenities", sa.String),
        sa.Column("first_seen", sa.DateTime, nullable=False),
        sa.Column("last_seen", sa.DateTime, nullable=False),
        sa.UniqueConstraint("source_id", "source_uid", name="uix_source_uid"),
    )
    op.create_table(
        "scores",
        sa.Column(
            "listing_id", sa.Integer, sa.ForeignKey("listings.id"), primary_key=True
        ),
        sa.Column("score", sa.Float),
        sa.Column("subscores", sa.String),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("scores")
    op.drop_table("listings")
    op.drop_table("sources")
