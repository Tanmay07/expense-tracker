from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"


class ExperimentRegistered(DomainEvent):
    experiment_id: str


class GuardrailsValidated(DomainEvent):
    experiment_id: str
    is_valid: bool


class KPICalculated(DomainEvent):
    kpi_id: str
    value: float


class InsightGenerated(DomainEvent):
    insight_id: str


class ExperimentCompleted(DomainEvent):
    experiment_id: str
    winner_variant: str


class ExperimentStopped(DomainEvent):
    experiment_id: str
    reason: str


class RegressionDetected(DomainEvent):
    metric: str
    severity: str


class OptimizationSuggested(DomainEvent):
    opportunity_id: str


class ExecutiveReportGenerated(DomainEvent):
    report_id: str
