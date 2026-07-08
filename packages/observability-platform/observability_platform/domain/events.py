from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

class TelemetryReceived(DomainEvent):
    event_category: str
    source: str

class IncidentDetected(DomainEvent):
    incident_id: str
    severity: str

class SLOViolated(DomainEvent):
    slo_id: str
    service_name: str

class MetricCalculated(DomainEvent):
    metric_name: str
    value: float

class ForecastGenerated(DomainEvent):
    target_metric: str
    forecast_value: float

class DashboardUpdated(DomainEvent):
    dashboard_id: str

class RootCauseCompleted(DomainEvent):
    incident_id: str
    root_cause: str

class GovernanceAlertRaised(DomainEvent):
    asset_id: str
    reason: str

class AIAnomalyDetected(DomainEvent):
    model_id: str
    anomaly_type: str

class FinancialAnomalyDetected(DomainEvent):
    account_id: str
    variance_amount: float
