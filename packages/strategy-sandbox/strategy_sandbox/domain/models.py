from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid

class ValidationProfile(BaseModel):
    id: str
    name: str
    profile_type: str
    required_stages: List[str]
    pass_criteria_json: Dict[str, Any]
    failure_thresholds_json: Dict[str, Any]
    scoring_weights_json: Dict[str, Any]
    timeout_seconds: int = 3600
    approval_requirements: List[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ValidationProfileCreate(BaseModel):
    name: str
    profile_type: str
    required_stages: List[str]
    pass_criteria_json: Dict[str, Any] = Field(default_factory=dict)
    failure_thresholds_json: Dict[str, Any] = Field(default_factory=dict)
    scoring_weights_json: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = 3600
    approval_requirements: List[str] = Field(default_factory=list)

class FitnessScore(BaseModel):
    id: str
    run_id: str
    financial_impact: float = 0.0
    risk_adjusted_return: float = 0.0
    goal_completion_probability: float = 0.0
    policy_compliance: float = 0.0
    downside_risk: float = 0.0
    simulation_stability: float = 0.0
    historical_consistency: float = 0.0
    explainability_quality: float = 0.0
    ai_confidence: float = 0.0
    execution_complexity: float = 0.0
    composite_score: float
    model_config = ConfigDict(from_attributes=True)

class BenchmarkRecord(BaseModel):
    id: str
    run_id: str
    benchmark_type: str
    reference_id: Optional[str] = None
    regression_report_json: Dict[str, Any] = Field(default_factory=dict)
    improvement_analysis_json: Dict[str, Any] = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

class PromptValidation(BaseModel):
    id: str
    run_id: str
    hallucination_resistance: float = 0.0
    policy_compliance: float = 0.0
    tool_selection_accuracy: float = 0.0
    output_consistency: float = 0.0
    explainability: float = 0.0
    latency_ms: int = 0
    token_usage: int = 0
    model_compatibility: List[str] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

class ReplaySnapshot(BaseModel):
    id: str
    run_id: str
    input_snapshot_json: Dict[str, Any] = Field(default_factory=dict)
    timeline_snapshot_json: Dict[str, Any] = Field(default_factory=dict)
    knowledge_graph_snapshot_json: Dict[str, Any] = Field(default_factory=dict)
    digital_twin_version: Optional[str] = None
    prompt_version: Optional[str] = None
    model_version: Optional[str] = None
    policy_version: Optional[str] = None
    simulation_seed: str
    validation_configuration_json: Dict[str, Any] = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

class SandboxCertification(BaseModel):
    id: str
    run_id: str
    asset_id: str
    certification_level: str
    granted_at: datetime
    expires_at: Optional[datetime] = None
    review_schedule_json: Dict[str, Any] = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

class SandboxRun(BaseModel):
    id: str
    asset_id: str
    profile_id: str
    status: str = "PENDING"
    current_stage: Optional[str] = None
    stage_results_json: Dict[str, Any] = Field(default_factory=dict)
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    profile: Optional[ValidationProfile] = None
    fitness_score: Optional[FitnessScore] = None
    prompt_validation: Optional[PromptValidation] = None
    benchmark: Optional[BenchmarkRecord] = None
    replay_snapshot: Optional[ReplaySnapshot] = None
    certification: Optional[SandboxCertification] = None
    
    model_config = ConfigDict(from_attributes=True)

class SandboxRunCreate(BaseModel):
    asset_id: str
    profile_id: str
