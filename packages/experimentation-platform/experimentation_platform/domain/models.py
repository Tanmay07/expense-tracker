from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid

class Feature(BaseModel):
    id: str = Field(default_factory=lambda: f"feat_{uuid.uuid4().hex}")
    name: str
    version: str
    description: Optional[str] = None
    feature_type: str
    owner_id: str
    dependencies: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)

class FeatureCreate(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    feature_type: str
    owner_id: str
    dependencies: Optional[List[str]] = None

class FeatureFlag(BaseModel):
    id: str = Field(default_factory=lambda: f"flag_{uuid.uuid4().hex}")
    feature_id: str
    flag_type: str
    is_enabled: bool = False
    default_value: Optional[bool] = None
    rollout_percentage: Optional[float] = None
    targeting_rules_json: Optional[Dict[str, Any]] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)

class Rollout(BaseModel):
    id: str = Field(default_factory=lambda: f"roll_{uuid.uuid4().hex}")
    feature_id: str
    current_stage: str
    stage_metadata_json: Optional[Dict[str, Any]] = None
    is_paused: bool = False
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)

class Experiment(BaseModel):
    id: str = Field(default_factory=lambda: f"exp_{uuid.uuid4().hex}")
    name: str
    experiment_type: str
    variants_json: Dict[str, Any]
    weights_json: Dict[str, int]
    target_metrics: List[str]
    status: str = "DRAFT"
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class ExperimentCreate(BaseModel):
    name: str
    experiment_type: str
    variants_json: Dict[str, Any]
    weights_json: Dict[str, int]
    target_metrics: List[str]

class ExperimentResult(BaseModel):
    id: str = Field(default_factory=lambda: f"expr_{uuid.uuid4().hex}")
    experiment_id: str
    results_json: Dict[str, Any]
    winning_variant_id: Optional[str] = None
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)
