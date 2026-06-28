from sqlalchemy import create_engine, Column, String, Float, Boolean, JSON, DateTime, Enum as SQLEnum
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os
import enum

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ledger_user:ledger_password@localhost:5432/finance_ledger")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CopilotModeEnum(enum.Enum):
    DAILY_COACH = "DAILY_COACH"
    BUDGET_COACH = "BUDGET_COACH"
    INVESTMENT_COACH = "INVESTMENT_COACH"
    DEBT_COACH = "DEBT_COACH"
    GOAL_COACH = "GOAL_COACH"

class GoalConversationModel(Base):
    __tablename__ = "copilot_goal_conversations"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    goal_type = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)
    active_mode = Column(SQLEnum(CopilotModeEnum))
    progress = Column(Float, default=0.0)
    action_history = Column(JSON) # List of strings

class BehavioralProfileModel(Base):
    __tablename__ = "copilot_behavioral_profiles"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    spending_behavior = Column(String)
    saving_habits = Column(String)
    investment_style = Column(String)
    risk_behavior = Column(String)
    financial_stress_indicators = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ActionPlanModel(Base):
    __tablename__ = "copilot_action_plans"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    conversation_id = Column(String, index=True)
    priority = Column(String)
    expected_impact = Column(String)
    steps = Column(JSON) # List of dicts representing ActionStep
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class SimulationRequestModel(Base):
    __tablename__ = "copilot_simulation_requests"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    scenario_type = Column(String)
    assumptions = Column(JSON)
    status = Column(String)

class ProactiveAlertModel(Base):
    __tablename__ = "copilot_proactive_alerts"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    alert_type = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
