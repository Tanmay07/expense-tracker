"""initial experimentation platform schema

Revision ID: 8e9f0b1c2d3e
Revises:
Create Date: 2026-06-30 12:06:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "8e9f0b1c2d3e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "exp_features",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("feature_type", sa.String(), nullable=False),
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column(
            "dependencies", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_exp_features_name"), "exp_features", ["name"], unique=True)

    op.create_table(
        "exp_feature_flags",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("feature_id", sa.String(), nullable=False),
        sa.Column("flag_type", sa.String(), nullable=False),
        sa.Column("is_enabled", sa.Boolean(), nullable=True),
        sa.Column("default_value", sa.Boolean(), nullable=True),
        sa.Column("rollout_percentage", sa.Float(), nullable=True),
        sa.Column(
            "targeting_rules_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["feature_id"],
            ["exp_features.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_exp_feature_flags_feature_id"),
        "exp_feature_flags",
        ["feature_id"],
        unique=False,
    )

    op.create_table(
        "exp_rollouts",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("feature_id", sa.String(), nullable=False),
        sa.Column("current_stage", sa.String(), nullable=False),
        sa.Column(
            "stage_metadata_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("is_paused", sa.Boolean(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["feature_id"],
            ["exp_features.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_exp_rollouts_feature_id"), "exp_rollouts", ["feature_id"], unique=False
    )

    op.create_table(
        "exp_experiments",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("experiment_type", sa.String(), nullable=False),
        sa.Column(
            "variants_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "weights_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "target_metrics", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "exp_experiment_results",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("experiment_id", sa.String(), nullable=False),
        sa.Column(
            "results_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("winning_variant_id", sa.String(), nullable=True),
        sa.Column("calculated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["experiment_id"],
            ["exp_experiments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_exp_experiment_results_experiment_id"),
        "exp_experiment_results",
        ["experiment_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_exp_experiment_results_experiment_id"),
        table_name="exp_experiment_results",
    )
    op.drop_table("exp_experiment_results")
    op.drop_table("exp_experiments")
    op.drop_index(op.f("ix_exp_rollouts_feature_id"), table_name="exp_rollouts")
    op.drop_table("exp_rollouts")
    op.drop_index(
        op.f("ix_exp_feature_flags_feature_id"), table_name="exp_feature_flags"
    )
    op.drop_table("exp_feature_flags")
    op.drop_index(op.f("ix_exp_features_name"), table_name="exp_features")
    op.drop_table("exp_features")
