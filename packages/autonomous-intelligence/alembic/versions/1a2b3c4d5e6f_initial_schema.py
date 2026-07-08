"""initial_schema

Revision ID: 1a2b3c4d5e6f
Revises:
Create Date: 2026-07-05 12:00:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1a2b3c4d5e6f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUMs
    sa.Enum("LOW", "MEDIUM", "HIGH", "CRITICAL", name="riskclassification").create(
        op.get_bind()
    )
    sa.Enum(
        "EMERGENCY_FUND",
        "DEBT_REDUCTION",
        "INVESTMENT_GROWTH",
        "SAVINGS",
        "CASH_FLOW",
        "INSURANCE",
        "TAXES",
        "RETIREMENT",
        "TRAVEL",
        "EDUCATION",
        "CUSTOM",
        name="goaltype",
    ).create(op.get_bind())
    sa.Enum(
        "INFORM",
        "RECOMMEND",
        "REQUIRE_APPROVAL",
        "SEMI_AUTOMATED",
        "FULLY_AUTOMATED",
        name="hitlclassification",
    ).create(op.get_bind())

    # Create tables
    op.create_table(
        "afip_agents",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("role", sa.String(length=255), nullable=False),
        sa.Column(
            "capabilities", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "allowed_tools", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "allowed_sdks", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("memory_scope", sa.String(length=100), nullable=False),
        sa.Column(
            "risk_classification",
            postgresql.ENUM(
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL",
                name="riskclassification",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "execution_permissions",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("lifecycle_state", sa.String(length=50), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column(
            "dependencies", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("policies", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("owner", sa.String(length=255), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "afip_goals",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "goal_type",
            postgresql.ENUM(
                "EMERGENCY_FUND",
                "DEBT_REDUCTION",
                "INVESTMENT_GROWTH",
                "SAVINGS",
                "CASH_FLOW",
                "INSURANCE",
                "TAXES",
                "RETIREMENT",
                "TRAVEL",
                "EDUCATION",
                "CUSTOM",
                name="goaltype",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("target_amount", sa.Float(), nullable=True),
        sa.Column("current_amount", sa.Float(), nullable=True),
        sa.Column("target_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column(
            "parameters", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["afip_agents.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "afip_missions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("goal_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("plan", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "hitl_classification",
            postgresql.ENUM(
                "INFORM",
                "RECOMMEND",
                "REQUIRE_APPROVAL",
                "SEMI_AUTOMATED",
                "FULLY_AUTOMATED",
                name="hitlclassification",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["afip_agents.id"],
        ),
        sa.ForeignKeyConstraint(
            ["goal_id"],
            ["afip_goals.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "afip_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mission_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("horizon", sa.String(length=50), nullable=False),
        sa.Column("content", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("is_contingency", sa.Boolean(), nullable=False),
        sa.Column("is_alternative", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["afip_agents.id"],
        ),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["afip_missions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "afip_memories",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("memory_type", sa.String(length=50), nullable=False),
        sa.Column("reference_id", sa.String(length=255), nullable=True),
        sa.Column("content", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["afip_agents.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "afip_evaluations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mission_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("goal_completion_score", sa.Float(), nullable=False),
        sa.Column("financial_impact", sa.Float(), nullable=False),
        sa.Column("recommendation_acceptance_rate", sa.Float(), nullable=False),
        sa.Column("execution_success_rate", sa.Float(), nullable=False),
        sa.Column("ai_quality_score", sa.Float(), nullable=False),
        sa.Column("latency_ms", sa.Float(), nullable=False),
        sa.Column("cost_usd", sa.Float(), nullable=False),
        sa.Column("trust_score", sa.Float(), nullable=False),
        sa.Column("user_satisfaction_score", sa.Float(), nullable=False),
        sa.Column(
            "evaluation_period_start", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column("evaluation_period_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["afip_agents.id"],
        ),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["afip_missions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("afip_evaluations")
    op.drop_table("afip_memories")
    op.drop_table("afip_plans")
    op.drop_table("afip_missions")
    op.drop_table("afip_goals")
    op.drop_table("afip_agents")

    sa.Enum(
        "INFORM",
        "RECOMMEND",
        "REQUIRE_APPROVAL",
        "SEMI_AUTOMATED",
        "FULLY_AUTOMATED",
        name="hitlclassification",
    ).drop(op.get_bind())
    sa.Enum(
        "EMERGENCY_FUND",
        "DEBT_REDUCTION",
        "INVESTMENT_GROWTH",
        "SAVINGS",
        "CASH_FLOW",
        "INSURANCE",
        "TAXES",
        "RETIREMENT",
        "TRAVEL",
        "EDUCATION",
        "CUSTOM",
        name="goaltype",
    ).drop(op.get_bind())
    sa.Enum("LOW", "MEDIUM", "HIGH", "CRITICAL", name="riskclassification").drop(
        op.get_bind()
    )
