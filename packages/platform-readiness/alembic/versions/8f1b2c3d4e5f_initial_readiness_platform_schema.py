"""initial readiness platform schema

Revision ID: 8f1b2c3d4e5f
Revises:
Create Date: 2026-06-30 12:20:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "8f1b2c3d4e5f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "readiness_architecture_fitness",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("component_name", sa.String(), nullable=False),
        sa.Column("compliance_score", sa.Float(), nullable=False),
        sa.Column("violations", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("last_scanned_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_readiness_architecture_fitness_component_name"),
        "readiness_architecture_fitness",
        ["component_name"],
        unique=False,
    )

    op.create_table(
        "readiness_security_certification",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("component_name", sa.String(), nullable=False),
        sa.Column("security_score", sa.Float(), nullable=False),
        sa.Column(
            "vulnerabilities", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("is_certified", sa.Boolean(), nullable=True),
        sa.Column("last_scanned_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_readiness_security_certification_component_name"),
        "readiness_security_certification",
        ["component_name"],
        unique=False,
    )

    op.create_table(
        "readiness_performance_certification",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("endpoint", sa.String(), nullable=False),
        sa.Column("p99_latency_ms", sa.Float(), nullable=False),
        sa.Column("requests_per_second", sa.Float(), nullable=False),
        sa.Column("error_rate", sa.Float(), nullable=False),
        sa.Column("is_certified", sa.Boolean(), nullable=True),
        sa.Column("last_tested_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_readiness_performance_certification_endpoint"),
        "readiness_performance_certification",
        ["endpoint"],
        unique=False,
    )

    op.create_table(
        "readiness_chaos_experiments",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("scenario_name", sa.String(), nullable=False),
        sa.Column("target_component", sa.String(), nullable=False),
        sa.Column("recovery_time_ms", sa.Float(), nullable=True),
        sa.Column("success", sa.Boolean(), nullable=True),
        sa.Column("executed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "readiness_cost_projections",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("component_name", sa.String(), nullable=False),
        sa.Column("monthly_forecast_usd", sa.Float(), nullable=False),
        sa.Column(
            "optimization_recommendations",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("calculated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "readiness_production_score",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("version_tag", sa.String(), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("is_go", sa.Boolean(), nullable=True),
        sa.Column(
            "risk_register", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "remediation_plan", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("calculated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_readiness_production_score_version_tag"),
        "readiness_production_score",
        ["version_tag"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_readiness_production_score_version_tag"),
        table_name="readiness_production_score",
    )
    op.drop_table("readiness_production_score")
    op.drop_table("readiness_cost_projections")
    op.drop_table("readiness_chaos_experiments")
    op.drop_index(
        op.f("ix_readiness_performance_certification_endpoint"),
        table_name="readiness_performance_certification",
    )
    op.drop_table("readiness_performance_certification")
    op.drop_index(
        op.f("ix_readiness_security_certification_component_name"),
        table_name="readiness_security_certification",
    )
    op.drop_table("readiness_security_certification")
    op.drop_index(
        op.f("ix_readiness_architecture_fitness_component_name"),
        table_name="readiness_architecture_fitness",
    )
    op.drop_table("readiness_architecture_fitness")
