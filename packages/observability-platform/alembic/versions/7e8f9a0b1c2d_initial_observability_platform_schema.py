"""initial observability platform schema

Revision ID: 7e8f9a0b1c2d
Revises: 
Create Date: 2026-06-30 12:05:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '7e8f9a0b1c2d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('obs_telemetry_events',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('trace_id', sa.String(), nullable=True),
        sa.Column('correlation_id', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_obs_telemetry_events_category'), 'obs_telemetry_events', ['category'], unique=False)
    op.create_index(op.f('ix_obs_telemetry_events_trace_id'), 'obs_telemetry_events', ['trace_id'], unique=False)
    op.create_index(op.f('ix_obs_telemetry_events_correlation_id'), 'obs_telemetry_events', ['correlation_id'], unique=False)
    op.create_index(op.f('ix_obs_telemetry_events_timestamp'), 'obs_telemetry_events', ['timestamp'], unique=False)

    op.create_table('obs_metric_records',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('metric_name', sa.String(), nullable=False),
        sa.Column('metric_type', sa.String(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_obs_metric_records_metric_name'), 'obs_metric_records', ['metric_name'], unique=False)
    op.create_index(op.f('ix_obs_metric_records_timestamp'), 'obs_metric_records', ['timestamp'], unique=False)

    op.create_table('obs_incidents',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('affected_components', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('root_cause', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('obs_slo_records',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('service_name', sa.String(), nullable=False),
        sa.Column('slo_name', sa.String(), nullable=False),
        sa.Column('target_percentage', sa.Float(), nullable=False),
        sa.Column('current_percentage', sa.Float(), nullable=False),
        sa.Column('error_budget_remaining', sa.Float(), nullable=False),
        sa.Column('is_breached', sa.Boolean(), nullable=True),
        sa.Column('evaluated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_obs_slo_records_service_name'), 'obs_slo_records', ['service_name'], unique=False)

    op.create_table('obs_dashboards',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('owner_id', sa.String(), nullable=False),
        sa.Column('layout_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('obs_dashboards')
    op.drop_index(op.f('ix_obs_slo_records_service_name'), table_name='obs_slo_records')
    op.drop_table('obs_slo_records')
    op.drop_table('obs_incidents')
    op.drop_index(op.f('ix_obs_metric_records_timestamp'), table_name='obs_metric_records')
    op.drop_index(op.f('ix_obs_metric_records_metric_name'), table_name='obs_metric_records')
    op.drop_table('obs_metric_records')
    op.drop_index(op.f('ix_obs_telemetry_events_timestamp'), table_name='obs_telemetry_events')
    op.drop_index(op.f('ix_obs_telemetry_events_correlation_id'), table_name='obs_telemetry_events')
    op.drop_index(op.f('ix_obs_telemetry_events_trace_id'), table_name='obs_telemetry_events')
    op.drop_index(op.f('ix_obs_telemetry_events_category'), table_name='obs_telemetry_events')
    op.drop_table('obs_telemetry_events')
