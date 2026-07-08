"""initial analytics platform schema

Revision ID: 9f0a1b2c3d4e
Revises:
Create Date: 2026-06-30 12:20:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "9f0a1b2c3d4e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "analytics_experiments",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column("business_objective", sa.String(), nullable=False),
        sa.Column("hypothesis", sa.String(), nullable=False),
        sa.Column("feature_id", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_analytics_experiments_name"),
        "analytics_experiments",
        ["name"],
        unique=True,
    )

    op.create_table(
        "analytics_guardrails",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("experiment_id", sa.String(), nullable=False),
        sa.Column("primary_metric", sa.String(), nullable=False),
        sa.Column(
            "guardrail_metrics", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("min_sample_size", sa.Integer(), nullable=False),
        sa.Column("minimum_detectable_effect", sa.Float(), nullable=False),
        sa.Column("confidence_threshold", sa.Float(), nullable=True),
        sa.Column("statistical_method", sa.String(), nullable=True),
        sa.Column(
            "auto_stop_conditions",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["experiment_id"],
            ["analytics_experiments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_analytics_guardrails_experiment_id"),
        "analytics_guardrails",
        ["experiment_id"],
        unique=False,
    )

    op.create_table(
        "analytics_kpi_catalog",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("kpi_name", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("formula", sa.String(), nullable=False),
        sa.Column("refresh_policy", sa.String(), nullable=True),
        sa.Column("target_value", sa.Float(), nullable=True),
        sa.Column("alert_threshold", sa.Float(), nullable=True),
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("kpi_name"),
    )

    op.create_table(
        "analytics_insights",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("insight_type", sa.String(), nullable=False),
        sa.Column("severity", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column(
            "metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("generated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "analytics_reports",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("report_type", sa.String(), nullable=False),
        sa.Column(
            "content_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("generated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("analytics_reports")
    op.drop_table("analytics_insights")
    op.drop_table("analytics_kpi_catalog")
    op.drop_index(
        op.f("ix_analytics_guardrails_experiment_id"), table_name="analytics_guardrails"
    )
    op.drop_table("analytics_guardrails")
    op.drop_index(
        op.f("ix_analytics_experiments_name"), table_name="analytics_experiments"
    )
    op.drop_table("analytics_experiments")
