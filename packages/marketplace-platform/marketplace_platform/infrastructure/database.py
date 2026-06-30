import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, Float, Integer, Boolean, DateTime,
    ForeignKey, ARRAY, JSON, Text
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MarketplaceAssetModel(Base):
    """
    Unified table for Strategies, Templates, Strategy Packs, and other reusable assets.
    """
    __tablename__ = "marketplace_assets"

    id = Column(String, primary_key=True)
    asset_type = Column(String, nullable=False) # STRATEGY, TEMPLATE, STRATEGY_PACK
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    publisher_id = Column(String, nullable=False)
    version = Column(String, nullable=False, default="1.0.0")
    status = Column(String, nullable=False, default="DRAFT") # DRAFT, REVIEW, PUBLISHED, DEPRECATED, ARCHIVED
    
    categories = Column(ARRAY(String), default=list)
    tags = Column(ARRAY(String), default=list)
    localization = Column(ARRAY(String), default=list)
    
    content_json = Column(JSONB, nullable=False, default=dict)
    dependencies_json = Column(JSONB, nullable=False, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    capability_matrix = relationship("KnowledgeCapabilityMatrixModel", back_populates="asset", uselist=False, cascade="all, delete-orphan")
    certification = relationship("CertificationModel", back_populates="asset", uselist=False, cascade="all, delete-orphan")
    ranking = relationship("AssetRankingModel", back_populates="asset", uselist=False, cascade="all, delete-orphan")


class KnowledgeCapabilityMatrixModel(Base):
    """
    Metadata-driven Knowledge Capability Matrix enforcing governance for each artifact.
    """
    __tablename__ = "knowledge_capability_matrix"

    id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("marketplace_assets.id"), nullable=False, unique=True)
    
    scope = Column(String, nullable=False) # GLOBAL, REGIONAL, HOUSEHOLD, PERSONAL
    visibility = Column(String, nullable=False) # PRIVATE, HOUSEHOLD, ORGANIZATION, PUBLIC
    sensitivity = Column(String, nullable=False) # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    
    retention_days = Column(Integer, nullable=True)
    purge_rules_json = Column(JSONB, nullable=False, default=dict)
    
    promotion_eligible_scopes = Column(ARRAY(String), default=list)
    explainability_level = Column(String, nullable=False, default="STANDARD")
    
    ai_usability_json = Column(JSONB, nullable=False, default=dict) # e.g. {"ai_coach": true, "digital_twin": false}
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    asset = relationship("MarketplaceAssetModel", back_populates="capability_matrix")


class CertificationModel(Base):
    """
    Trust and certification records for an asset.
    """
    __tablename__ = "asset_certifications"

    id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("marketplace_assets.id"), nullable=False, unique=True)
    
    status = Column(String, nullable=False, default="PENDING") # PENDING, APPROVED, REJECTED, REVOKED
    certifier_id = Column(String, nullable=True)
    certification_tier = Column(String, nullable=True)
    
    compliance_metadata_json = Column(JSONB, nullable=False, default=dict)
    security_metadata_json = Column(JSONB, nullable=False, default=dict)
    
    granted_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    asset = relationship("MarketplaceAssetModel", back_populates="certification")


class AssetRankingModel(Base):
    """
    Real-time ranking metrics for marketplace discovery.
    """
    __tablename__ = "asset_rankings"

    id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("marketplace_assets.id"), nullable=False, unique=True)
    
    financial_impact_score = Column(Float, default=0.0)
    completion_rate = Column(Float, default=0.0)
    roi_score = Column(Float, default=0.0)
    user_satisfaction = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.0)
    
    ai_recommendation_frequency = Column(Integer, default=0)
    simulation_success_rate = Column(Float, default=0.0)
    decision_success_rate = Column(Float, default=0.0)
    
    overall_quality_score = Column(Float, default=0.0)
    
    last_calculated = Column(DateTime, default=datetime.utcnow)

    asset = relationship("MarketplaceAssetModel", back_populates="ranking")
