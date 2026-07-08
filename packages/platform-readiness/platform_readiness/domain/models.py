from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid


class ArchitectureFitness(BaseModel):
    id: str = Field(default_factory=lambda: f"arch_{uuid.uuid4().hex}")
    component_name: str
    compliance_score: float
    violations: Optional[List[str]] = None
    last_scanned_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)


class SecurityCertification(BaseModel):
    id: str = Field(default_factory=lambda: f"sec_{uuid.uuid4().hex}")
    component_name: str
    security_score: float
    vulnerabilities: Optional[List[str]] = None
    is_certified: bool = False
    last_scanned_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)


class PerformanceCertification(BaseModel):
    id: str = Field(default_factory=lambda: f"perf_{uuid.uuid4().hex}")
    endpoint: str
    p99_latency_ms: float
    requests_per_second: float
    error_rate: float
    is_certified: bool = False
    last_tested_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)


class ChaosExperiment(BaseModel):
    id: str = Field(default_factory=lambda: f"chaos_{uuid.uuid4().hex}")
    scenario_name: str
    target_component: str
    recovery_time_ms: Optional[float] = None
    success: bool = False
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)


class CostProjection(BaseModel):
    id: str = Field(default_factory=lambda: f"cost_{uuid.uuid4().hex}")
    component_name: str
    monthly_forecast_usd: float
    optimization_recommendations: Optional[List[str]] = None
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)


class ProductionReadiness(BaseModel):
    id: str = Field(default_factory=lambda: f"pr_score_{uuid.uuid4().hex}")
    version_tag: str
    overall_score: float
    is_go: bool = False
    risk_register: Optional[Dict[str, Any]] = None
    remediation_plan: Optional[Dict[str, Any]] = None
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)
