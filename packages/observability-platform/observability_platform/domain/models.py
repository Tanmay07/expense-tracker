from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid

class TelemetryEvent(BaseModel):
    id: str = Field(default_factory=lambda: f"tel_{uuid.uuid4().hex}")
    category: str
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    source: str
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)

class TelemetryEventCreate(BaseModel):
    category: str
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    source: str
    payload: Dict[str, Any]

class MetricRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"met_{uuid.uuid4().hex}")
    metric_name: str
    metric_type: str
    value: float
    tags: Optional[Dict[str, str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)

class MetricRecordCreate(BaseModel):
    metric_name: str
    metric_type: str
    value: float
    tags: Optional[Dict[str, str]] = None

class Incident(BaseModel):
    id: str = Field(default_factory=lambda: f"inc_{uuid.uuid4().hex}")
    title: str
    description: Optional[str] = None
    severity: str
    status: str = "OPEN"
    affected_components: Optional[List[str]] = None
    root_cause: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class SLORecord(BaseModel):
    id: str = Field(default_factory=lambda: f"slo_{uuid.uuid4().hex}")
    service_name: str
    slo_name: str
    target_percentage: float
    current_percentage: float
    error_budget_remaining: float
    is_breached: bool = False
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)

class DashboardConfig(BaseModel):
    id: str = Field(default_factory=lambda: f"dash_{uuid.uuid4().hex}")
    name: str
    owner_id: str
    layout_json: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)
