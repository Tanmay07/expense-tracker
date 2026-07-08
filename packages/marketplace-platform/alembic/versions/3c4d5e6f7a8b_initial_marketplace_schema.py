"""initial marketplace schema

Revision ID: 3c4d5e6f7a8b
Revises:
Create Date: 2026-06-30 11:30:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "3c4d5e6f7a8b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "marketplace_assets",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("asset_type", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("publisher_id", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("categories", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("tags", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("localization", sa.ARRAY(sa.String()), nullable=True),
        sa.Column(
            "content_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "dependencies_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "knowledge_capability_matrix",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("asset_id", sa.String(), nullable=False),
        sa.Column("scope", sa.String(), nullable=False),
        sa.Column("visibility", sa.String(), nullable=False),
        sa.Column("sensitivity", sa.String(), nullable=False),
        sa.Column("retention_days", sa.Integer(), nullable=True),
        sa.Column(
            "purge_rules_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("promotion_eligible_scopes", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("explainability_level", sa.String(), nullable=False),
        sa.Column(
            "ai_usability_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["marketplace_assets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("asset_id"),
    )

    op.create_table(
        "asset_certifications",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("asset_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("certifier_id", sa.String(), nullable=True),
        sa.Column("certification_tier", sa.String(), nullable=True),
        sa.Column(
            "compliance_metadata_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "security_metadata_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("granted_at", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["marketplace_assets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("asset_id"),
    )

    op.create_table(
        "asset_rankings",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("asset_id", sa.String(), nullable=False),
        sa.Column("financial_impact_score", sa.Float(), nullable=True),
        sa.Column("completion_rate", sa.Float(), nullable=True),
        sa.Column("roi_score", sa.Float(), nullable=True),
        sa.Column("user_satisfaction", sa.Float(), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("risk_score", sa.Float(), nullable=True),
        sa.Column("ai_recommendation_frequency", sa.Integer(), nullable=True),
        sa.Column("simulation_success_rate", sa.Float(), nullable=True),
        sa.Column("decision_success_rate", sa.Float(), nullable=True),
        sa.Column("overall_quality_score", sa.Float(), nullable=True),
        sa.Column("last_calculated", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["marketplace_assets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("asset_id"),
    )


def downgrade() -> None:
    op.drop_table("asset_rankings")
    op.drop_table("asset_certifications")
    op.drop_table("knowledge_capability_matrix")
    op.drop_table("marketplace_assets")
