"""initial platform release

Revision ID: 1a2b3c4d5e6f
Revises:
Create Date: 2026-06-30 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1a2b3c4d5e6f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "release_platform_baselines",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column("technical_metrics", sa.JSON(), nullable=True),
        sa.Column("business_metrics", sa.JSON(), nullable=True),
        sa.Column("ai_metrics", sa.JSON(), nullable=True),
        sa.Column("operational_metrics", sa.JSON(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_release_platform_baselines_id"),
        "release_platform_baselines",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_release_platform_baselines_version"),
        "release_platform_baselines",
        ["version"],
        unique=False,
    )

    op.create_table(
        "release_certification_reports",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column("architecture_certified", sa.Boolean(), nullable=True),
        sa.Column("performance_certified", sa.Boolean(), nullable=True),
        sa.Column("security_certified", sa.Boolean(), nullable=True),
        sa.Column("governance_certified", sa.Boolean(), nullable=True),
        sa.Column("operationally_ready", sa.Boolean(), nullable=True),
        sa.Column("ai_certified", sa.Boolean(), nullable=True),
        sa.Column("marketplace_certified", sa.Boolean(), nullable=True),
        sa.Column("validation_certified", sa.Boolean(), nullable=True),
        sa.Column("analytics_certified", sa.Boolean(), nullable=True),
        sa.Column("mission_control_ready", sa.Boolean(), nullable=True),
        sa.Column("overall_pass", sa.Boolean(), nullable=True),
        sa.Column("risk_register", sa.JSON(), nullable=True),
        sa.Column("technical_debt", sa.JSON(), nullable=True),
        sa.Column("recommendations", sa.JSON(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_release_certification_reports_id"),
        "release_certification_reports",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_release_certification_reports_version"),
        "release_certification_reports",
        ["version"],
        unique=False,
    )

    op.create_table(
        "release_contract_matrices",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column("rest_apis", sa.JSON(), nullable=True),
        sa.Column("sdk_apis", sa.JSON(), nullable=True),
        sa.Column("events", sa.JSON(), nullable=True),
        sa.Column("plugins", sa.JSON(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_release_contract_matrices_id"),
        "release_contract_matrices",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_release_contract_matrices_version"),
        "release_contract_matrices",
        ["version"],
        unique=False,
    )

    op.create_table(
        "release_documentation_indices",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column("documents", sa.JSON(), nullable=True),
        sa.Column("completeness_score", sa.Float(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_release_documentation_indices_id"),
        "release_documentation_indices",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_release_documentation_indices_version"),
        "release_documentation_indices",
        ["version"],
        unique=False,
    )

    op.create_table(
        "release_manifests",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("certification_id", sa.String(), nullable=True),
        sa.Column("baseline_id", sa.String(), nullable=True),
        sa.Column("contract_matrix_id", sa.String(), nullable=True),
        sa.Column("documentation_index_id", sa.String(), nullable=True),
        sa.Column("release_notes", sa.Text(), nullable=True),
        sa.Column("breaking_changes", sa.JSON(), nullable=True),
        sa.Column("known_limitations", sa.JSON(), nullable=True),
        sa.Column("sbom", sa.JSON(), nullable=True),
        sa.Column("architecture_hash", sa.String(), nullable=True),
        sa.Column("platform_fingerprint", sa.String(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_release_manifests_id"), "release_manifests", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_release_manifests_version"),
        "release_manifests",
        ["version"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_release_manifests_version"), table_name="release_manifests")
    op.drop_index(op.f("ix_release_manifests_id"), table_name="release_manifests")
    op.drop_table("release_manifests")
    op.drop_index(
        op.f("ix_release_documentation_indices_version"),
        table_name="release_documentation_indices",
    )
    op.drop_index(
        op.f("ix_release_documentation_indices_id"),
        table_name="release_documentation_indices",
    )
    op.drop_table("release_documentation_indices")
    op.drop_index(
        op.f("ix_release_contract_matrices_version"),
        table_name="release_contract_matrices",
    )
    op.drop_index(
        op.f("ix_release_contract_matrices_id"), table_name="release_contract_matrices"
    )
    op.drop_table("release_contract_matrices")
    op.drop_index(
        op.f("ix_release_certification_reports_version"),
        table_name="release_certification_reports",
    )
    op.drop_index(
        op.f("ix_release_certification_reports_id"),
        table_name="release_certification_reports",
    )
    op.drop_table("release_certification_reports")
    op.drop_index(
        op.f("ix_release_platform_baselines_version"),
        table_name="release_platform_baselines",
    )
    op.drop_index(
        op.f("ix_release_platform_baselines_id"),
        table_name="release_platform_baselines",
    )
    op.drop_table("release_platform_baselines")
