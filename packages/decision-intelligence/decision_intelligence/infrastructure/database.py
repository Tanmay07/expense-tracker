from sqlalchemy import create_engine, Column, String, Float, JSON, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DecisionCandidateModel(Base):
    __tablename__ = "intel_decision_candidates"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String)
    strategy = Column(String)
    
    overall_score = Column(Float)
    
    # Store complex nested data in JSON
    proposed_actions = Column(JSON)
    sub_scores = Column(JSON, nullable=True)
    opportunity_cost = Column(JSON, nullable=True)
    confidence = Column(JSON, nullable=True)
    evidence = Column(JSON, nullable=True)
    constraint_violations = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class DecisionBundleModel(Base):
    __tablename__ = "intel_decision_bundles"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    name = Column(String)
    combined_score = Column(Float)
    
    candidates_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
