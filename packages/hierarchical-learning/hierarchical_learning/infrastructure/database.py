import os
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, String, DateTime, Float, 
    Boolean, JSON, Integer, Text, ForeignKey, ARRAY
)
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from pgvector.sqlalchemy import Vector

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class GlobalLearningModel(Base):
    __tablename__ = "hlkep_global_learning"
    
    id = Column(String, primary_key=True, default=lambda: f"gl_{uuid.uuid4().hex}")
    topic = Column(String, index=True) # e.g. "budget_heuristics", "merchant_trends"
    aggregated_knowledge_json = Column(JSON)
    confidence_score = Column(Float, default=0.0)
    sample_size = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1)
    status = Column(String, default="VALIDATED") # CANDIDATE, VALIDATED, APPROVED, DEPRECATED

class RegionalLearningModel(Base):
    __tablename__ = "hlkep_regional_learning"
    
    id = Column(String, primary_key=True, default=lambda: f"rl_{uuid.uuid4().hex}")
    region_id = Column(String, index=True) # e.g. "US-CA", "EU", "LATAM"
    topic = Column(String, index=True)
    regional_knowledge_json = Column(JSON)
    confidence_score = Column(Float, default=0.0)
    sample_size = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1)
    overrides_global = Column(Boolean, default=False)

class HouseholdLearningModel(Base):
    __tablename__ = "hlkep_household_learning"
    
    id = Column(String, primary_key=True, default=lambda: f"hl_{uuid.uuid4().hex}")
    household_id = Column(String, index=True)
    topic = Column(String, index=True)
    household_knowledge_json = Column(JSON)
    member_permissions_json = Column(JSON) # e.g. {"user_1": "READ", "user_2": "READ_WRITE"}
    consensus_score = Column(Float, default=1.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1)

class HouseholdConsensusModel(Base):
    __tablename__ = "hlkep_household_consensus"
    
    id = Column(String, primary_key=True, default=lambda: f"hc_{uuid.uuid4().hex}")
    household_id = Column(String, index=True)
    conflict_topic = Column(String, index=True)
    competing_preferences_json = Column(JSON)
    resolved_consensus_json = Column(JSON)
    explainability_text = Column(Text)
    status = Column(String, default="PENDING") # PENDING, RESOLVED, MANUAL_REVIEW
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

class PersonalLearningModel(Base):
    __tablename__ = "hlkep_personal_learning"
    
    id = Column(String, primary_key=True, default=lambda: f"pl_{uuid.uuid4().hex}")
    user_id = Column(String, index=True)
    topic = Column(String, index=True)
    personal_knowledge_json = Column(JSON)
    financial_dna_snapshot = Column(JSON)
    semantic_embedding = Column(Vector(1536), nullable=True) # pgvector for behavior matching
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    decay_rate = Column(Float, default=0.01) # rate at which knowledge becomes stale
    version = Column(Integer, default=1)

class KnowledgePromotionModel(Base):
    __tablename__ = "hlkep_knowledge_promotion"
    
    id = Column(String, primary_key=True, default=lambda: f"kp_{uuid.uuid4().hex}")
    source_scope = Column(String) # PERSONAL, HOUSEHOLD, REGIONAL
    target_scope = Column(String) # HOUSEHOLD, REGIONAL, GLOBAL
    source_id = Column(String)
    topic = Column(String, index=True)
    proposed_knowledge_json = Column(JSON)
    promotion_status = Column(String, default="OBSERVED") # OBSERVED, CANDIDATE, APPROVED, PUBLISHED, REJECTED
    evidence_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

class ConsentProfileModel(Base):
    __tablename__ = "hlkep_consent_profiles"
    
    id = Column(String, primary_key=True, default=lambda: f"cp_{uuid.uuid4().hex}")
    user_id = Column(String, unique=True, index=True)
    allow_anonymous_aggregation = Column(Boolean, default=True)
    allow_household_sharing = Column(Boolean, default=False)
    data_residency_region = Column(String, default="US")
    opted_out_topics = Column(ARRAY(String), default=list)
    federated_learning_opt_in = Column(Boolean, default=False)
    differential_privacy_budget = Column(Float, default=1.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
