"""initial validation registry schema

Revision ID: 5e6f7a8b9c0d
Revises: 
Create Date: 2026-06-30 11:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '5e6f7a8b9c0d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('var_artifact_records',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('canonical_name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('producer', sa.String(), nullable=False),
        sa.Column('pipeline_id', sa.String(), nullable=True),
        sa.Column('sandbox_run_id', sa.String(), nullable=True),
        sa.Column('strategy_id', sa.String(), nullable=True),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('owner_id', sa.String(), nullable=False),
        sa.Column('tags', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('metadata_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('storage_location', sa.String(), nullable=False),
        sa.Column('checksum_sha256', sa.String(), nullable=False),
        sa.Column('digital_signature', sa.String(), nullable=True),
        sa.Column('is_encrypted', sa.Boolean(), nullable=True),
        sa.Column('is_compressed', sa.Boolean(), nullable=True),
        sa.Column('integrity_status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('retention_policy', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('canonical_name', 'version', name='uq_artifact_version')
    )

    op.create_table('var_artifact_lineage',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('source_id', sa.String(), nullable=False),
        sa.Column('target_id', sa.String(), nullable=False),
        sa.Column('relationship_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['source_id'], ['var_artifact_records.id'], ),
        sa.ForeignKeyConstraint(['target_id'], ['var_artifact_records.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('source_id', 'target_id', 'relationship_type', name='uq_lineage_edge')
    )

    op.create_table('var_evidence_packages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('package_name', sa.String(), nullable=False),
        sa.Column('artifact_ids', sa.ARRAY(sa.String()), nullable=False),
        sa.Column('certification_id', sa.String(), nullable=True),
        sa.Column('compliance_framework', sa.String(), nullable=True),
        sa.Column('digital_signature', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('package_name')
    )

    op.create_table('var_reuse_evaluations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('target_artifact_id', sa.String(), nullable=False),
        sa.Column('input_hash', sa.String(), nullable=False),
        sa.Column('policy_version', sa.String(), nullable=True),
        sa.Column('model_version', sa.String(), nullable=True),
        sa.Column('is_reusable', sa.Boolean(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('evaluated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['target_artifact_id'], ['var_artifact_records.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('var_reuse_evaluations')
    op.drop_table('var_evidence_packages')
    op.drop_table('var_artifact_lineage')
    op.drop_table('var_artifact_records')
