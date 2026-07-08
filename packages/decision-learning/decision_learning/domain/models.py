from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime


class DecisionMemoryBase(BaseModel):
    decision_id: str
    user_id: str
    action_type: str
    evidence_json: Dict[str, Any] = Field(default_factory=dict)
    context_snapshot_json: Dict[str, Any] = Field(default_factory=dict)
    policy_snapshot_json: Dict[str, Any] = Field(default_factory=dict)
    timeline_snapshot_version: Optional[int] = None
    knowledge_graph_snapshot_version: Optional[int] = None
    simulation_snapshot_id: Optional[str] = None
    financial_metrics_json: Dict[str, Any] = Field(default_factory=dict)
    prompt_version: Optional[str] = None
    model_version: Optional[str] = None
    execution_outcome: Optional[str] = None
    user_feedback_score: Optional[float] = None
    embedding: Optional[List[float]] = None


class DecisionMemoryCreate(DecisionMemoryBase):
    pass


class DecisionMemoryResponse(DecisionMemoryBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PatternBase(BaseModel):
    user_id: str
    pattern_type: str
    description: str
    confidence: float
    evidence_events: List[str] = Field(default_factory=list)
    metadata_json: Dict[str, Any] = Field(default_factory=dict)


class PatternCreate(PatternBase):
    pass


class PatternResponse(PatternBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PersonalizationBase(BaseModel):
    user_id: str
    preferred_strategies_json: Dict[str, Any] = Field(default_factory=dict)
    communication_style: Optional[str] = None
    risk_preference: Optional[str] = None
    recommendation_frequency: Optional[str] = None


class PersonalizationCreate(PersonalizationBase):
    pass


class PersonalizationResponse(PersonalizationBase):
    id: str
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)


class PolicyCacheBase(BaseModel):
    decision_id: str
    policy_version: int
    context_snapshot_id: str
    evaluation_result: str
    expires_at: Optional[datetime] = None
    is_valid: bool = True


class PolicyCacheCreate(PolicyCacheBase):
    pass


class PolicyCacheResponse(PolicyCacheBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PredictionBase(BaseModel):
    decision_id: str
    user_id: str
    acceptance_probability: float
    completion_probability: float
    expected_roi: float
    risk_reduction: float
    confidence_interval_json: Dict[str, Any] = Field(default_factory=dict)


class PredictionCreate(PredictionBase):
    pass


class PredictionResponse(PredictionBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class FinancialDNABase(BaseModel):
    user_id: str
    investor_type: Optional[str] = None
    saver_type: Optional[str] = None
    debt_discipline_score: float = 0.0
    risk_appetite_score: float = 0.0
    impulse_spending_index: float = 0.0
    goal_discipline_score: float = 0.0


class FinancialDNACreate(FinancialDNABase):
    pass


class FinancialDNAResponse(FinancialDNABase):
    id: str
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)


class BehaviorBase(BaseModel):
    user_id: str
    evolution_type: str
    previous_value: Optional[str] = None
    new_value: Optional[str] = None
    reasoning: Optional[str] = None


class BehaviorCreate(BehaviorBase):
    pass


class BehaviorResponse(BehaviorBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class LearningBase(BaseModel):
    learning_type: str
    target_id: str
    weight_adjustments_json: Dict[str, Any] = Field(default_factory=dict)


class LearningCreate(LearningBase):
    pass


class LearningResponse(LearningBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ReplayBase(BaseModel):
    session_id: str
    replay_data_json: Dict[str, Any] = Field(default_factory=dict)


class ReplayCreate(ReplayBase):
    pass


class ReplayResponse(ReplayBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
