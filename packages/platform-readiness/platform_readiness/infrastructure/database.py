import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, Float, DateTime,
    ForeignKey, Boolean, Integer, JSON
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


class ArchitectureFitnessModel(Base):
    __tablename__ = "readiness_architecture_fitness"

    id = Column(String, primary_key=True)
    component_name = Column(String, nullable=False, index=True)
    compliance_score = Column(Float, nullable=False)
    violations = Column(JSONB, nullable=True) # e.g. ["cyclic_dependency", "layer_violation"]
    last_scanned_at = Column(DateTime, default=datetime.utcnow)


class SecurityCertificationModel(Base):
    __tablename__ = "readiness_security_certification"

    id = Column(String, primary_key=True)
    component_name = Column(String, nullable=False, index=True)
    security_score = Column(Float, nullable=False)
    vulnerabilities = Column(JSONB, nullable=True)
    is_certified = Column(Boolean, default=False)
    last_scanned_at = Column(DateTime, default=datetime.utcnow)


class PerformanceCertificationModel(Base):
    __tablename__ = "readiness_performance_certification"

    id = Column(String, primary_key=True)
    endpoint = Column(String, nullable=False, index=True)
    p99_latency_ms = Column(Float, nullable=False)
    requests_per_second = Column(Float, nullable=False)
    error_rate = Column(Float, nullable=False)
    is_certified = Column(Boolean, default=False)
    last_tested_at = Column(DateTime, default=datetime.utcnow)


class ChaosExperimentModel(Base):
    __tablename__ = "readiness_chaos_experiments"

    id = Column(String, primary_key=True)
    scenario_name = Column(String, nullable=False)
    target_component = Column(String, nullable=False)
    recovery_time_ms = Column(Float, nullable=True)
    success = Column(Boolean, default=False)
    executed_at = Column(DateTime, default=datetime.utcnow)


class CostModel(Base):
    __tablename__ = "readiness_cost_projections"

    id = Column(String, primary_key=True)
    component_name = Column(String, nullable=False)
    monthly_forecast_usd = Column(Float, nullable=False)
    optimization_recommendations = Column(JSONB, nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow)


class ProductionReadinessModel(Base):
    """
    The final Go/No-Go aggregated score.
    """
    __tablename__ = "readiness_production_score"

    id = Column(String, primary_key=True)
    version_tag = Column(String, nullable=False, unique=True, index=True)
    overall_score = Column(Float, nullable=False)
    is_go = Column(Boolean, default=False)
    risk_register = Column(JSONB, nullable=True)
    remediation_plan = Column(JSONB, nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow)
