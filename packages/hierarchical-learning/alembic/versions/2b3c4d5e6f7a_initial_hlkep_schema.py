"""Initial HLKEP schema

Revision ID: 2b3c4d5e6f7a
Revises:
Create Date: 2026-06-30 14:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = "2b3c4d5e6f7a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure vector extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Global Learning
    op.create_table(
        "hlkep_global_learning",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("topic", sa.String(), nullable=True),
        sa.Column("aggregated_knowledge_json", sa.JSON(), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("sample_size", sa.Integer(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_hlkep_global_learning_topic"),
        "hlkep_global_learning",
        ["topic"],
        unique=False,
    )

    # Regional Learning
    op.create_table(
        "hlkep_regional_learning",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("region_id", sa.String(), nullable=True),
        sa.Column("topic", sa.String(), nullable=True),
        sa.Column("regional_knowledge_json", sa.JSON(), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("sample_size", sa.Integer(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.Column("overrides_global", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_hlkep_regional_learning_region_id"),
        "hlkep_regional_learning",
        ["region_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_hlkep_regional_learning_topic"),
        "hlkep_regional_learning",
        ["topic"],
        unique=False,
    )

    # Household Learning
    op.create_table(
        "hlkep_household_learning",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("household_id", sa.String(), nullable=True),
        sa.Column("topic", sa.String(), nullable=True),
        sa.Column("household_knowledge_json", sa.JSON(), nullable=True),
        sa.Column("member_permissions_json", sa.JSON(), nullable=True),
        sa.Column("consensus_score", sa.Float(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_hlkep_household_learning_household_id"),
        "hlkep_household_learning",
        ["household_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_hlkep_household_learning_topic"),
        "hlkep_household_learning",
        ["topic"],
        unique=False,
    )

    # Household Consensus
    op.create_table(
        "hlkep_household_consensus",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("household_id", sa.String(), nullable=True),
        sa.Column("conflict_topic", sa.String(), nullable=True),
        sa.Column("competing_preferences_json", sa.JSON(), nullable=True),
        sa.Column("resolved_consensus_json", sa.JSON(), nullable=True),
        sa.Column("explainability_text", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_hlkep_household_consensus_household_id"),
        "hlkep_household_consensus",
        ["household_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_hlkep_household_consensus_conflict_topic"),
        "hlkep_household_consensus",
        ["conflict_topic"],
        unique=False,
    )

    # Personal Learning
    op.create_table(
        "hlkep_personal_learning",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("topic", sa.String(), nullable=True),
        sa.Column("personal_knowledge_json", sa.JSON(), nullable=True),
        sa.Column("financial_dna_snapshot", sa.JSON(), nullable=True),
        sa.Column("semantic_embedding", Vector(1536), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("decay_rate", sa.Float(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_hlkep_personal_learning_user_id"),
        "hlkep_personal_learning",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_hlkep_personal_learning_topic"),
        "hlkep_personal_learning",
        ["topic"],
        unique=False,
    )

    # Knowledge Promotion
    op.create_table(
        "hlkep_knowledge_promotion",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("source_scope", sa.String(), nullable=True),
        sa.Column("target_scope", sa.String(), nullable=True),
        sa.Column("source_id", sa.String(), nullable=True),
        sa.Column("topic", sa.String(), nullable=True),
        sa.Column("proposed_knowledge_json", sa.JSON(), nullable=True),
        sa.Column("promotion_status", sa.String(), nullable=True),
        sa.Column("evidence_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_hlkep_knowledge_promotion_topic"),
        "hlkep_knowledge_promotion",
        ["topic"],
        unique=False,
    )

    # Consent Profiles
    op.create_table(
        "hlkep_consent_profiles",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("allow_anonymous_aggregation", sa.Boolean(), nullable=True),
        sa.Column("allow_household_sharing", sa.Boolean(), nullable=True),
        sa.Column("data_residency_region", sa.String(), nullable=True),
        sa.Column("opted_out_topics", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("federated_learning_opt_in", sa.Boolean(), nullable=True),
        sa.Column("differential_privacy_budget", sa.Float(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_hlkep_consent_profiles_user_id"),
        "hlkep_consent_profiles",
        ["user_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_hlkep_consent_profiles_user_id"), table_name="hlkep_consent_profiles"
    )
    op.drop_table("hlkep_consent_profiles")

    op.drop_index(
        op.f("ix_hlkep_knowledge_promotion_topic"),
        table_name="hlkep_knowledge_promotion",
    )
    op.drop_table("hlkep_knowledge_promotion")

    op.drop_index(
        op.f("ix_hlkep_personal_learning_topic"), table_name="hlkep_personal_learning"
    )
    op.drop_index(
        op.f("ix_hlkep_personal_learning_user_id"), table_name="hlkep_personal_learning"
    )
    op.drop_table("hlkep_personal_learning")

    op.drop_index(
        op.f("ix_hlkep_household_consensus_conflict_topic"),
        table_name="hlkep_household_consensus",
    )
    op.drop_index(
        op.f("ix_hlkep_household_consensus_household_id"),
        table_name="hlkep_household_consensus",
    )
    op.drop_table("hlkep_household_consensus")

    op.drop_index(
        op.f("ix_hlkep_household_learning_topic"), table_name="hlkep_household_learning"
    )
    op.drop_index(
        op.f("ix_hlkep_household_learning_household_id"),
        table_name="hlkep_household_learning",
    )
    op.drop_table("hlkep_household_learning")

    op.drop_index(
        op.f("ix_hlkep_regional_learning_topic"), table_name="hlkep_regional_learning"
    )
    op.drop_index(
        op.f("ix_hlkep_regional_learning_region_id"),
        table_name="hlkep_regional_learning",
    )
    op.drop_table("hlkep_regional_learning")

    op.drop_index(
        op.f("ix_hlkep_global_learning_topic"), table_name="hlkep_global_learning"
    )
    op.drop_table("hlkep_global_learning")
