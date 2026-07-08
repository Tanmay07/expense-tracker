from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ConsentProfile(BaseModel):
    id: str
    user_id: str
    allow_anonymous_aggregation: bool = True
    allow_household_sharing: bool = False
    data_residency_region: str = "US"
    opted_out_topics: List[str] = Field(default_factory=list)
    federated_learning_opt_in: bool = False
    differential_privacy_budget: float = 1.0
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)


class GlobalLearning(BaseModel):
    id: str
    topic: str
    aggregated_knowledge_json: Dict[str, Any]
    confidence_score: float
    sample_size: int
    last_updated: datetime
    version: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class RegionalLearning(BaseModel):
    id: str
    region_id: str
    topic: str
    regional_knowledge_json: Dict[str, Any]
    confidence_score: float
    sample_size: int
    last_updated: datetime
    version: int
    overrides_global: bool

    model_config = ConfigDict(from_attributes=True)


class HouseholdLearning(BaseModel):
    id: str
    household_id: str
    topic: str
    household_knowledge_json: Dict[str, Any]
    member_permissions_json: Dict[str, str]
    consensus_score: float
    last_updated: datetime
    version: int

    model_config = ConfigDict(from_attributes=True)


class HouseholdConsensus(BaseModel):
    id: str
    household_id: str
    conflict_topic: str
    competing_preferences_json: Dict[str, Any]
    resolved_consensus_json: Optional[Dict[str, Any]] = None
    explainability_text: Optional[str] = None
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PersonalLearning(BaseModel):
    id: str
    user_id: str
    topic: str
    personal_knowledge_json: Dict[str, Any]
    financial_dna_snapshot: Dict[str, Any]
    last_updated: datetime
    decay_rate: float
    version: int

    model_config = ConfigDict(from_attributes=True)


class KnowledgePromotion(BaseModel):
    id: str
    source_scope: str
    target_scope: str
    source_id: str
    topic: str
    proposed_knowledge_json: Dict[str, Any]
    promotion_status: str
    evidence_json: Dict[str, Any]
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Update / Create requests


class ConsentProfileUpdate(BaseModel):
    allow_anonymous_aggregation: Optional[bool] = None
    allow_household_sharing: Optional[bool] = None
    data_residency_region: Optional[str] = None
    opted_out_topics: Optional[List[str]] = None
    federated_learning_opt_in: Optional[bool] = None
    differential_privacy_budget: Optional[float] = None


class PersonalLearningCreate(BaseModel):
    user_id: str
    topic: str
    personal_knowledge_json: Dict[str, Any]
    financial_dna_snapshot: Dict[str, Any]
    semantic_embedding: Optional[List[float]] = None


class KnowledgePromotionCreate(BaseModel):
    source_scope: str
    target_scope: str
    source_id: str
    topic: str
    proposed_knowledge_json: Dict[str, Any]
    evidence_json: Dict[str, Any]


class HouseholdConsensusCreate(BaseModel):
    household_id: str
    conflict_topic: str
    competing_preferences_json: Dict[str, Any]
