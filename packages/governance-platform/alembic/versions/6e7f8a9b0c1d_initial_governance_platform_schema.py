"""initial governance platform schema

Revision ID: 6e7f8a9b0c1d
Revises: 
Create Date: 2026-06-30 11:55:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '6e7f8a9b0c1d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('gov_policies',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('domain', sa.String(), nullable=False),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('policy_payload_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', 'version', name='uq_policy_version')
    )

    op.create_table('gov_trust_scores',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('asset_id', sa.String(), nullable=False),
        sa.Column('validation_score', sa.Float(), nullable=True),
        sa.Column('lineage_score', sa.Float(), nullable=True),
        sa.Column('ai_confidence_score', sa.Float(), nullable=True),
        sa.Column('policy_compliance_score', sa.Float(), nullable=True),
        sa.Column('marketplace_usage_score', sa.Float(), nullable=True),
        sa.Column('composite_trust_score', sa.Float(), nullable=False),
        sa.Column('is_trusted', sa.Boolean(), nullable=True),
        sa.Column('last_calculated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gov_trust_scores_asset_id'), 'gov_trust_scores', ['asset_id'], unique=False)

    op.create_table('gov_maturity_records',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('asset_id', sa.String(), nullable=False),
        sa.Column('current_level', sa.String(), nullable=False),
        sa.Column('promoted_at', sa.DateTime(), nullable=True),
        sa.Column('promoted_by', sa.String(), nullable=False),
        sa.Column('reason', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gov_maturity_records_asset_id'), 'gov_maturity_records', ['asset_id'], unique=False)

    op.create_table('gov_ai_metrics',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('asset_id', sa.String(), nullable=False),
        sa.Column('hallucination_rate', sa.Float(), nullable=True),
        sa.Column('bias_score', sa.Float(), nullable=True),
        sa.Column('fairness_score', sa.Float(), nullable=True),
        sa.Column('prompt_drift', sa.Float(), nullable=True),
        sa.Column('privacy_violation_count', sa.Float(), nullable=True),
        sa.Column('evaluated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gov_ai_metrics_asset_id'), 'gov_ai_metrics', ['asset_id'], unique=False)

    op.create_table('gov_evidence_ledger',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('asset_id', sa.String(), nullable=False),
        sa.Column('evidence_type', sa.String(), nullable=False),
        sa.Column('payload_hash', sa.String(), nullable=False),
        sa.Column('digital_signature', sa.String(), nullable=False),
        sa.Column('signer_id', sa.String(), nullable=False),
        sa.Column('previous_ledger_id', sa.String(), nullable=True),
        sa.Column('recorded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['previous_ledger_id'], ['gov_evidence_ledger.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gov_evidence_ledger_asset_id'), 'gov_evidence_ledger', ['asset_id'], unique=False)

    op.create_table('gov_workflows',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('asset_id', sa.String(), nullable=False),
        sa.Column('workflow_type', sa.String(), nullable=False),
        sa.Column('current_state', sa.String(), nullable=False),
        sa.Column('assigned_reviewer_id', sa.String(), nullable=True),
        sa.Column('comments', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gov_workflows_asset_id'), 'gov_workflows', ['asset_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_gov_workflows_asset_id'), table_name='gov_workflows')
    op.drop_table('gov_workflows')
    op.drop_index(op.f('ix_gov_evidence_ledger_asset_id'), table_name='gov_evidence_ledger')
    op.drop_table('gov_evidence_ledger')
    op.drop_index(op.f('ix_gov_ai_metrics_asset_id'), table_name='gov_ai_metrics')
    op.drop_table('gov_ai_metrics')
    op.drop_index(op.f('ix_gov_maturity_records_asset_id'), table_name='gov_maturity_records')
    op.drop_table('gov_maturity_records')
    op.drop_index(op.f('ix_gov_trust_scores_asset_id'), table_name='gov_trust_scores')
    op.drop_table('gov_trust_scores')
    op.drop_table('gov_policies')
