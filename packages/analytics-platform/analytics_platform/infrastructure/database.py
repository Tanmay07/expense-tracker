import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, Float, DateTime,
    ForeignKey, Integer
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ExperimentRegistryModel(Base):
    """
    Canonical Registry for experiments.
    """
    __tablename__ = "analytics_experiments"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    
    owner_id = Column(String, nullable=False)
    business_objective = Column(String, nullable=False)
    hypothesis = Column(String, nullable=False)
    
    feature_id = Column(String, nullable=True) # Linked to Experimentation Platform
    status = Column(String, default="REGISTERED") # REGISTERED, APPROVED, RUNNING, STOPPED, COMPLETED
    
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StatisticalGuardrailModel(Base):
    """
    Statistical constraints protecting an experiment.
    """
    __tablename__ = "analytics_guardrails"

    id = Column(String, primary_key=True)
    experiment_id = Column(String, ForeignKey("analytics_experiments.id"), nullable=False, index=True)
    
    primary_metric = Column(String, nullable=False)
    guardrail_metrics = Column(JSONB, nullable=False) # e.g. ["latency", "error_rate"]
    
    min_sample_size = Column(Integer, nullable=False)
    minimum_detectable_effect = Column(Float, nullable=False)
    confidence_threshold = Column(Float, default=0.95)
    
    statistical_method = Column(String, default="FREQUENTIST")
    
    # E.g. {"latency": {"operator": "gt", "threshold": 500}}
    auto_stop_conditions = Column(JSONB, nullable=True)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class KPICatalogModel(Base):
    """
    Metadata registry for all enterprise KPIs.
    """
    __tablename__ = "analytics_kpi_catalog"

    id = Column(String, primary_key=True)
    kpi_name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False) # BUSINESS, FINANCIAL, AI, OPERATIONAL
    
    formula = Column(String, nullable=False)
    refresh_policy = Column(String, default="DAILY")
    
    target_value = Column(Float, nullable=True)
    alert_threshold = Column(Float, nullable=True)
    
    owner_id = Column(String, nullable=False)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class InsightModel(Base):
    """
    Generated anomalies, regressions, and optimizations.
    """
    __tablename__ = "analytics_insights"

    id = Column(String, primary_key=True)
    insight_type = Column(String, nullable=False) # ANOMALY, TREND, FORECAST, OPTIMIZATION
    severity = Column(String, default="INFO")
    
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    metadata_json = Column(JSONB, nullable=True)
    
    generated_at = Column(DateTime, default=datetime.utcnow)


class ExecutiveReportModel(Base):
    """
    Generated scorecards and summaries.
    """
    __tablename__ = "analytics_reports"

    id = Column(String, primary_key=True)
    report_type = Column(String, nullable=False) # WEEKLY, MONTHLY, AI_SCORECARD
    
    content_json = Column(JSONB, nullable=False) # The actual metrics and insights
    
    generated_at = Column(DateTime, default=datetime.utcnow)
