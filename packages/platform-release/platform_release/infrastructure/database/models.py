from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class DBPlatformBaseline(Base):
    __tablename__ = "release_platform_baselines"
    id = Column(String, primary_key=True, index=True)
    version = Column(String, index=True)
    technical_metrics = Column(JSON)
    business_metrics = Column(JSON)
    ai_metrics = Column(JSON)
    operational_metrics = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DBCertificationReport(Base):
    __tablename__ = "release_certification_reports"
    id = Column(String, primary_key=True, index=True)
    version = Column(String, index=True)
    architecture_certified = Column(Boolean)
    performance_certified = Column(Boolean)
    security_certified = Column(Boolean)
    governance_certified = Column(Boolean)
    operationally_ready = Column(Boolean)
    ai_certified = Column(Boolean)
    marketplace_certified = Column(Boolean)
    validation_certified = Column(Boolean)
    analytics_certified = Column(Boolean)
    mission_control_ready = Column(Boolean)
    overall_pass = Column(Boolean)
    risk_register = Column(JSON)
    technical_debt = Column(JSON)
    recommendations = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DBContractVersionMatrix(Base):
    __tablename__ = "release_contract_matrices"
    id = Column(String, primary_key=True, index=True)
    version = Column(String, index=True)
    rest_apis = Column(JSON)
    sdk_apis = Column(JSON)
    events = Column(JSON)
    plugins = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DBDocumentationIndex(Base):
    __tablename__ = "release_documentation_indices"
    id = Column(String, primary_key=True, index=True)
    version = Column(String, index=True)
    documents = Column(JSON)
    completeness_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DBReleaseManifest(Base):
    __tablename__ = "release_manifests"
    id = Column(String, primary_key=True, index=True)
    version = Column(String, unique=True, index=True)
    name = Column(String)
    certification_id = Column(String)
    baseline_id = Column(String)
    contract_matrix_id = Column(String)
    documentation_index_id = Column(String)
    release_notes = Column(Text)
    breaking_changes = Column(JSON)
    known_limitations = Column(JSON)
    sbom = Column(JSON)
    architecture_hash = Column(String)
    platform_fingerprint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
