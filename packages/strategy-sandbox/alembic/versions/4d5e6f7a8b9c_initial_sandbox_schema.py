"""initial sandbox schema

Revision ID: 4d5e6f7a8b9c
Revises:
Create Date: 2026-06-30 11:40:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "4d5e6f7a8b9c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sandbox_validation_profiles",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("profile_type", sa.String(), nullable=False),
        sa.Column("required_stages", sa.ARRAY(sa.String()), nullable=False),
        sa.Column(
            "pass_criteria_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "failure_thresholds_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "scoring_weights_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("timeout_seconds", sa.Integer(), nullable=True),
        sa.Column("approval_requirements", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "sandbox_runs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("asset_id", sa.String(), nullable=False),
        sa.Column("profile_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("current_stage", sa.String(), nullable=True),
        sa.Column(
            "stage_results_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["sandbox_validation_profiles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "sandbox_fitness_scores",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=False),
        sa.Column("financial_impact", sa.Float(), nullable=True),
        sa.Column("risk_adjusted_return", sa.Float(), nullable=True),
        sa.Column("goal_completion_probability", sa.Float(), nullable=True),
        sa.Column("policy_compliance", sa.Float(), nullable=True),
        sa.Column("downside_risk", sa.Float(), nullable=True),
        sa.Column("simulation_stability", sa.Float(), nullable=True),
        sa.Column("historical_consistency", sa.Float(), nullable=True),
        sa.Column("explainability_quality", sa.Float(), nullable=True),
        sa.Column("ai_confidence", sa.Float(), nullable=True),
        sa.Column("execution_complexity", sa.Float(), nullable=True),
        sa.Column("composite_score", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["sandbox_runs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("run_id"),
    )

    op.create_table(
        "sandbox_benchmarks",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=False),
        sa.Column("benchmark_type", sa.String(), nullable=False),
        sa.Column("reference_id", sa.String(), nullable=True),
        sa.Column(
            "regression_report_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "improvement_analysis_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["sandbox_runs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("run_id"),
    )

    op.create_table(
        "sandbox_prompt_validations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=False),
        sa.Column("hallucination_resistance", sa.Float(), nullable=True),
        sa.Column("policy_compliance", sa.Float(), nullable=True),
        sa.Column("tool_selection_accuracy", sa.Float(), nullable=True),
        sa.Column("output_consistency", sa.Float(), nullable=True),
        sa.Column("explainability", sa.Float(), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("token_usage", sa.Integer(), nullable=True),
        sa.Column("model_compatibility", sa.ARRAY(sa.String()), nullable=True),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["sandbox_runs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("run_id"),
    )

    op.create_table(
        "sandbox_replay_snapshots",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=False),
        sa.Column(
            "input_snapshot_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "timeline_snapshot_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "knowledge_graph_snapshot_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("digital_twin_version", sa.String(), nullable=True),
        sa.Column("prompt_version", sa.String(), nullable=True),
        sa.Column("model_version", sa.String(), nullable=True),
        sa.Column("policy_version", sa.String(), nullable=True),
        sa.Column("simulation_seed", sa.String(), nullable=False),
        sa.Column(
            "validation_configuration_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["sandbox_runs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("run_id"),
    )

    op.create_table(
        "sandbox_certifications",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=False),
        sa.Column("asset_id", sa.String(), nullable=False),
        sa.Column("certification_level", sa.String(), nullable=False),
        sa.Column("granted_at", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column(
            "review_schedule_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["sandbox_runs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("run_id"),
    )


def downgrade() -> None:
    op.drop_table("sandbox_certifications")
    op.drop_table("sandbox_replay_snapshots")
    op.drop_table("sandbox_prompt_validations")
    op.drop_table("sandbox_benchmarks")
    op.drop_table("sandbox_fitness_scores")
    op.drop_table("sandbox_runs")
    op.drop_table("sandbox_validation_profiles")
