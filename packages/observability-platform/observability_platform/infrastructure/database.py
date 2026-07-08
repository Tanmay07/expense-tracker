import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TelemetryEventModel(Base):
    """
    Canonical store for cross-domain operational intelligence events.
    Utilizes JSONB for flexible payload indexing.
    """

    __tablename__ = "obs_telemetry_events"

    id = Column(String, primary_key=True)

    # E.g. BUSINESS, FINANCIAL, SYSTEM, AI, GOVERNANCE
    category = Column(String, nullable=False, index=True)

    # e.g., trace_id, span_id, correlation_id
    trace_id = Column(String, nullable=True, index=True)
    correlation_id = Column(String, nullable=True, index=True)

    # Emitting source (e.g., 'financial_core', 'decision_engine')
    source = Column(String, nullable=False)

    # The actual structured payload
    payload = Column(JSONB, nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class MetricRecordModel(Base):
    """
    Aggregated time-series KPI data.
    """

    __tablename__ = "obs_metric_records"

    id = Column(String, primary_key=True)
    metric_name = Column(String, nullable=False, index=True)

    # E.g. GAUGE, COUNTER, HISTOGRAM
    metric_type = Column(String, nullable=False)

    value = Column(Float, nullable=False)
    tags = Column(JSONB, nullable=True)  # E.g. {"tenant": "123", "region": "us-east"}

    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class IncidentModel(Base):
    """
    Operational incidents detected via anomalies or raised manually.
    """

    __tablename__ = "obs_incidents"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    severity = Column(String, nullable=False)  # SEV-1, SEV-2, SEV-3
    status = Column(
        String, nullable=False, default="OPEN"
    )  # OPEN, INVESTIGATING, RESOLVED

    affected_components = Column(JSONB, nullable=True)  # list of affected services
    root_cause = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)


class SLORecordModel(Base):
    """
    Service Level Objective tracking.
    """

    __tablename__ = "obs_slo_records"

    id = Column(String, primary_key=True)
    service_name = Column(String, nullable=False, index=True)
    slo_name = Column(String, nullable=False)

    target_percentage = Column(Float, nullable=False)
    current_percentage = Column(Float, nullable=False)

    error_budget_remaining = Column(Float, nullable=False)
    is_breached = Column(Boolean, default=False)

    evaluated_at = Column(DateTime, default=datetime.utcnow)


class DashboardConfigModel(Base):
    """
    Executive dashboard JSON layouts.
    """

    __tablename__ = "obs_dashboards"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)

    # JSON definition of layout and widgets
    layout_json = Column(JSONB, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
