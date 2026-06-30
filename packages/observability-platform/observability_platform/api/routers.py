from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from observability_platform.domain.models import (
    TelemetryEvent, TelemetryEventCreate, MetricRecord, MetricRecordCreate,
    Incident, SLORecord, DashboardConfig
)
from observability_platform.application.services import (
    TelemetryService, MetricsService, AIObservabilityService,
    FinancialObservabilityService, OperationalIntelligenceService,
    SLOService, DashboardService
)
from observability_platform.api.dependencies import (
    get_telemetry_service, get_metrics_service, get_ai_obs_service,
    get_fin_obs_service, get_intelligence_service, get_slo_service, get_dashboard_service
)

router = APIRouter()

@router.post("/telemetry", response_model=TelemetryEvent)
def ingest_telemetry(
    dto: TelemetryEventCreate,
    svc: TelemetryService = Depends(get_telemetry_service)
):
    return svc.ingest_event(dto)

@router.get("/telemetry/{category}", response_model=List[TelemetryEvent])
def query_telemetry(
    category: str,
    svc: TelemetryService = Depends(get_telemetry_service)
):
    return svc.query_events(category)

@router.post("/metrics", response_model=MetricRecord)
def record_metric(
    dto: MetricRecordCreate,
    svc: MetricsService = Depends(get_metrics_service)
):
    return svc.record_metric(dto)

class AITelemetryReq(BaseModel):
    source: str
    metrics: Dict[str, Any]

@router.post("/ai-observability", response_model=TelemetryEvent)
def track_ai_event(
    req: AITelemetryReq,
    svc: AIObservabilityService = Depends(get_ai_obs_service)
):
    return svc.track_ai_event(req.source, req.metrics)

class FinTelemetryReq(BaseModel):
    source: str
    event_data: Dict[str, Any]

@router.post("/financial-observability", response_model=TelemetryEvent)
def track_fin_event(
    req: FinTelemetryReq,
    svc: FinancialObservabilityService = Depends(get_fin_obs_service)
):
    return svc.track_financial_event(req.source, req.event_data)

class AnomalyReq(BaseModel):
    title: str
    severity: str
    details: Dict[str, Any]

@router.post("/incidents", response_model=Incident)
def report_incident(
    req: AnomalyReq,
    svc: OperationalIntelligenceService = Depends(get_intelligence_service)
):
    return svc.analyze_anomaly(req.title, req.severity, req.details)

class SLORegisterReq(BaseModel):
    service_name: str
    slo_name: str
    target_percentage: float

@router.post("/slo", response_model=SLORecord)
def register_slo(
    req: SLORegisterReq,
    svc: SLOService = Depends(get_slo_service)
):
    return svc.register_slo(req.service_name, req.slo_name, req.target_percentage)

class DashboardCreateReq(BaseModel):
    name: str
    owner_id: str
    layout: Dict[str, Any]

@router.post("/dashboards", response_model=DashboardConfig)
def create_dashboard(
    req: DashboardCreateReq,
    svc: DashboardService = Depends(get_dashboard_service)
):
    return svc.create_dashboard(req.name, req.owner_id, req.layout)
