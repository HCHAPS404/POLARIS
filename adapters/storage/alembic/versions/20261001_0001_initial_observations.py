"""Initial observations + assessment_snapshots tables.

Revision ID: 20261001_0001
Revises:
Create Date: 2026-10-01
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "20261001_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table(
        "observations",
        sa.Column("observation_id", sa.String(length=64), primary_key=True),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("observed_at", sa.String(length=32), nullable=False),
        sa.Column("observed_property", sa.String(length=64), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_observations_run_id", "observations", ["run_id"])
    op.create_table(
        "assessment_snapshots",
        sa.Column("run_id", sa.String(length=64), primary_key=True),
        sa.Column("fixture_id", sa.String(length=128), nullable=False),
        sa.Column("snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_table(
        "schema_meta",
        sa.Column("key", sa.String(length=64), primary_key=True),
        sa.Column("value", sa.Text(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("schema_meta")
    op.drop_table("assessment_snapshots")
    op.drop_index("ix_observations_run_id", table_name="observations")
    op.drop_table("observations")
