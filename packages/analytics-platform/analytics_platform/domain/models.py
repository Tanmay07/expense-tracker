from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid


class ExperimentRegistry(BaseModel):
    id: str = Field(default_factory=lambda: f"exp_reg_{uuid.uuid4().hex}")
    name: str
    description: Optional[str] = None
    owner_id: str
    business_objective: str
    hypothesis: str
    feature_id: Optional[str] = None
    status: str = "REGISTERED"
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)


class ExperimentRegistryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: str
    business_objective: str
    hypothesis: str
    feature_id: Optional[str] = None


class StatisticalGuardrail(BaseModel):
    id: str = Field(default_factory=lambda: f"grdl_{uuid.uuid4().hex}")
    experiment_id: str
    primary_metric: str
    guardrail_metrics: List[str]
    min_sample_size: int
    minimum_detectable_effect: float
    confidence_threshold: float = 0.95
    statistical_method: str = "FREQUENTIST"
    auto_stop_conditions: Optional[Dict[str, Any]] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)


class KPICatalog(BaseModel):
    id: str = Field(default_factory=lambda: f"kpi_{uuid.uuid4().hex}")
    kpi_name: str
    category: str
    formula: str
    refresh_policy: str = "DAILY"
    target_value: Optional[float] = None
    alert_threshold: Optional[float] = None
    owner_id: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)


class Insight(BaseModel):
    id: str = Field(default_factory=lambda: f"ins_{uuid.uuid4().hex}")
    insight_type: str
    severity: str = "INFO"
    title: str
    description: str
    metadata_json: Optional[Dict[str, Any]] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)


class ExecutiveReport(BaseModel):
    id: str = Field(default_factory=lambda: f"rep_{uuid.uuid4().hex}")
    report_type: str
    content_json: Dict[str, Any]
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)
