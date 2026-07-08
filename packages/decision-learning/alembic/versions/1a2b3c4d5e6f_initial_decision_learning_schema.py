"""Initial decision learning schema

Revision ID: 1a2b3c4d5e6f
Revises:
Create Date: 2026-06-29 13:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = "1a2b3c4d5e6f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure vector extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Decision Memory
    op.create_table(
        "decision_memory",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("decision_id", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("action_type", sa.String(), nullable=True),
        sa.Column("evidence_json", sa.JSON(), nullable=True),
        sa.Column("context_snapshot_json", sa.JSON(), nullable=True),
        sa.Column("policy_snapshot_json", sa.JSON(), nullable=True),
        sa.Column("timeline_snapshot_version", sa.Integer(), nullable=True),
        sa.Column("knowledge_graph_snapshot_version", sa.Integer(), nullable=True),
        sa.Column("simulation_snapshot_id", sa.String(), nullable=True),
        sa.Column("financial_metrics_json", sa.JSON(), nullable=True),
        sa.Column("prompt_version", sa.String(), nullable=True),
        sa.Column("model_version", sa.String(), nullable=True),
        sa.Column("execution_outcome", sa.String(), nullable=True),
        sa.Column("user_feedback_score", sa.Float(), nullable=True),
        sa.Column("embedding", Vector(1536), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_decision_memory_id"), "decision_memory", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_decision_memory_decision_id"),
        "decision_memory",
        ["decision_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_decision_memory_user_id"), "decision_memory", ["user_id"], unique=False
    )
    op.create_index(
        op.f("ix_decision_memory_action_type"),
        "decision_memory",
        ["action_type"],
        unique=False,
    )

    # Learning Patterns
    op.create_table(
        "learning_patterns",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("pattern_type", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("evidence_events", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_learning_patterns_id"), "learning_patterns", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_learning_patterns_user_id"),
        "learning_patterns",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_learning_patterns_pattern_type"),
        "learning_patterns",
        ["pattern_type"],
        unique=False,
    )

    # Adaptive Personalizations
    op.create_table(
        "adaptive_personalizations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("preferred_strategies_json", sa.JSON(), nullable=True),
        sa.Column("communication_style", sa.String(), nullable=True),
        sa.Column("risk_preference", sa.String(), nullable=True),
        sa.Column("recommendation_frequency", sa.String(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_adaptive_personalizations_id"),
        "adaptive_personalizations",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_adaptive_personalizations_user_id"),
        "adaptive_personalizations",
        ["user_id"],
        unique=True,
    )

    # Policy Decision Cache
    op.create_table(
        "policy_decision_cache",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("decision_id", sa.String(), nullable=True),
        sa.Column("policy_version", sa.Integer(), nullable=True),
        sa.Column("context_snapshot_id", sa.String(), nullable=True),
        sa.Column("evaluation_result", sa.String(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("is_valid", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_policy_decision_cache_id"),
        "policy_decision_cache",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_policy_decision_cache_decision_id"),
        "policy_decision_cache",
        ["decision_id"],
        unique=False,
    )

    # Decision Predictions
    op.create_table(
        "decision_predictions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("decision_id", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("acceptance_probability", sa.Float(), nullable=True),
        sa.Column("completion_probability", sa.Float(), nullable=True),
        sa.Column("expected_roi", sa.Float(), nullable=True),
        sa.Column("risk_reduction", sa.Float(), nullable=True),
        sa.Column("confidence_interval_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_decision_predictions_id"), "decision_predictions", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_decision_predictions_decision_id"),
        "decision_predictions",
        ["decision_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_decision_predictions_user_id"),
        "decision_predictions",
        ["user_id"],
        unique=False,
    )

    # Financial DNA Profiles
    op.create_table(
        "financial_dna_profiles",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("investor_type", sa.String(), nullable=True),
        sa.Column("saver_type", sa.String(), nullable=True),
        sa.Column("debt_discipline_score", sa.Float(), nullable=True),
        sa.Column("risk_appetite_score", sa.Float(), nullable=True),
        sa.Column("impulse_spending_index", sa.Float(), nullable=True),
        sa.Column("goal_discipline_score", sa.Float(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_financial_dna_profiles_id"),
        "financial_dna_profiles",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_financial_dna_profiles_user_id"),
        "financial_dna_profiles",
        ["user_id"],
        unique=True,
    )

    # Behavioral Evolutions
    op.create_table(
        "behavioral_evolutions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("evolution_type", sa.String(), nullable=True),
        sa.Column("previous_value", sa.String(), nullable=True),
        sa.Column("new_value", sa.String(), nullable=True),
        sa.Column("reasoning", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_behavioral_evolutions_id"),
        "behavioral_evolutions",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_behavioral_evolutions_user_id"),
        "behavioral_evolutions",
        ["user_id"],
        unique=False,
    )

    # Continuous Learnings
    op.create_table(
        "continuous_learnings",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("learning_type", sa.String(), nullable=True),
        sa.Column("target_id", sa.String(), nullable=True),
        sa.Column("weight_adjustments_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_continuous_learnings_id"), "continuous_learnings", ["id"], unique=False
    )

    # Learning Replays
    op.create_table(
        "learning_replays",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=True),
        sa.Column("replay_data_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_learning_replays_id"), "learning_replays", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_learning_replays_session_id"),
        "learning_replays",
        ["session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_learning_replays_session_id"), table_name="learning_replays")
    op.drop_index(op.f("ix_learning_replays_id"), table_name="learning_replays")
    op.drop_table("learning_replays")

    op.drop_index(op.f("ix_continuous_learnings_id"), table_name="continuous_learnings")
    op.drop_table("continuous_learnings")

    op.drop_index(
        op.f("ix_behavioral_evolutions_user_id"), table_name="behavioral_evolutions"
    )
    op.drop_index(
        op.f("ix_behavioral_evolutions_id"), table_name="behavioral_evolutions"
    )
    op.drop_table("behavioral_evolutions")

    op.drop_index(
        op.f("ix_financial_dna_profiles_user_id"), table_name="financial_dna_profiles"
    )
    op.drop_index(
        op.f("ix_financial_dna_profiles_id"), table_name="financial_dna_profiles"
    )
    op.drop_table("financial_dna_profiles")

    op.drop_index(
        op.f("ix_decision_predictions_user_id"), table_name="decision_predictions"
    )
    op.drop_index(
        op.f("ix_decision_predictions_decision_id"), table_name="decision_predictions"
    )
    op.drop_index(op.f("ix_decision_predictions_id"), table_name="decision_predictions")
    op.drop_table("decision_predictions")

    op.drop_index(
        op.f("ix_policy_decision_cache_decision_id"), table_name="policy_decision_cache"
    )
    op.drop_index(
        op.f("ix_policy_decision_cache_id"), table_name="policy_decision_cache"
    )
    op.drop_table("policy_decision_cache")

    op.drop_index(
        op.f("ix_adaptive_personalizations_user_id"),
        table_name="adaptive_personalizations",
    )
    op.drop_index(
        op.f("ix_adaptive_personalizations_id"), table_name="adaptive_personalizations"
    )
    op.drop_table("adaptive_personalizations")

    op.drop_index(
        op.f("ix_learning_patterns_pattern_type"), table_name="learning_patterns"
    )
    op.drop_index(op.f("ix_learning_patterns_user_id"), table_name="learning_patterns")
    op.drop_index(op.f("ix_learning_patterns_id"), table_name="learning_patterns")
    op.drop_table("learning_patterns")

    op.drop_index(op.f("ix_decision_memory_action_type"), table_name="decision_memory")
    op.drop_index(op.f("ix_decision_memory_user_id"), table_name="decision_memory")
    op.drop_index(op.f("ix_decision_memory_decision_id"), table_name="decision_memory")
    op.drop_index(op.f("ix_decision_memory_id"), table_name="decision_memory")
    op.drop_table("decision_memory")
