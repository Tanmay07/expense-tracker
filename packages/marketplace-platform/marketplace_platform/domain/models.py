from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class KnowledgeCapabilityMatrix(BaseModel):
    id: str
    asset_id: str
    scope: str
    visibility: str
    sensitivity: str
    retention_days: Optional[int] = None
    purge_rules_json: Dict[str, Any]
    promotion_eligible_scopes: List[str]
    explainability_level: str
    ai_usability_json: Dict[str, Any]
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class KnowledgeCapabilityMatrixCreate(BaseModel):
    scope: str
    visibility: str
    sensitivity: str
    retention_days: Optional[int] = None
    purge_rules_json: Dict[str, Any] = Field(default_factory=dict)
    promotion_eligible_scopes: List[str] = Field(default_factory=list)
    explainability_level: str = "STANDARD"
    ai_usability_json: Dict[str, Any] = Field(default_factory=dict)

class AssetRanking(BaseModel):
    id: str
    asset_id: str
    financial_impact_score: float
    completion_rate: float
    roi_score: float
    user_satisfaction: float
    confidence_score: float
    risk_score: float
    ai_recommendation_frequency: int
    simulation_success_rate: float
    decision_success_rate: float
    overall_quality_score: float
    last_calculated: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Certification(BaseModel):
    id: str
    asset_id: str
    status: str
    certifier_id: Optional[str] = None
    certification_tier: Optional[str] = None
    compliance_metadata_json: Dict[str, Any]
    security_metadata_json: Dict[str, Any]
    granted_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class MarketplaceAsset(BaseModel):
    id: str
    asset_type: str
    title: str
    description: Optional[str] = None
    publisher_id: str
    version: str
    status: str
    categories: List[str]
    tags: List[str]
    localization: List[str]
    content_json: Dict[str, Any]
    dependencies_json: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    capability_matrix: Optional[KnowledgeCapabilityMatrix] = None
    certification: Optional[Certification] = None
    ranking: Optional[AssetRanking] = None
    
    model_config = ConfigDict(from_attributes=True)

class MarketplaceAssetCreate(BaseModel):
    asset_type: str
    title: str
    description: Optional[str] = None
    publisher_id: str
    version: str = "1.0.0"
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    localization: List[str] = Field(default_factory=list)
    content_json: Dict[str, Any]
    dependencies_json: Dict[str, Any] = Field(default_factory=dict)
    capability_matrix: KnowledgeCapabilityMatrixCreate
