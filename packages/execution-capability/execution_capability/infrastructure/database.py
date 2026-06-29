from sqlalchemy import create_engine, Column, String, Boolean, JSON, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CapabilityModel(Base):
    __tablename__ = "execution_capabilities"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    automation_level = Column(String)
    risk_level = Column(String)
    supported_platforms_json = Column(JSON)
    prerequisites_json = Column(JSON)
    metadata_json = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ApprovalRequestModel(Base):
    __tablename__ = "execution_approvals"
    
    id = Column(String, primary_key=True, index=True)
    execution_step_id = Column(String, index=True)
    capability_id = Column(String)
    requested_by = Column(String)
    status = Column(String)
    approver_id = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
