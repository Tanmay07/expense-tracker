import uuid
from datetime import datetime
from typing import List, Dict, Any

from observability_platform.domain.models import (
    TelemetryEvent,
    TelemetryEventCreate,
    MetricRecord,
    MetricRecordCreate,
    Incident,
    SLORecord,
    DashboardConfig,
)
from observability_platform.infrastructure.repositories import (
    TelemetryRepository,
    MetricRepository,
    IncidentRepository,
    SLORepository,
    DashboardRepository,
)


class TelemetryService:
    def __init__(self, repo: TelemetryRepository):
        self.repo = repo

    def ingest_event(self, dto: TelemetryEventCreate) -> TelemetryEvent:
        event = TelemetryEvent(
            id=f"tel_{uuid.uuid4().hex}",
            category=dto.category,
            trace_id=dto.trace_id,
            correlation_id=dto.correlation_id,
            source=dto.source,
            payload=dto.payload,
            timestamp=datetime.utcnow(),
        )
        return self.repo.save(event)

    def query_events(self, category: str) -> List[TelemetryEvent]:
        return self.repo.get_by_category(category)


class MetricsService:
    def __init__(self, repo: MetricRepository):
        self.repo = repo

    def record_metric(self, dto: MetricRecordCreate) -> MetricRecord:
        record = MetricRecord(
            id=f"met_{uuid.uuid4().hex}",
            metric_name=dto.metric_name,
            metric_type=dto.metric_type,
            value=dto.value,
            tags=dto.tags,
            timestamp=datetime.utcnow(),
        )
        return self.repo.save(record)


class AIObservabilityService:
    def __init__(self, tel_svc: TelemetryService):
        self.tel_svc = tel_svc

    def track_ai_event(self, source: str, metrics: Dict[str, Any]) -> TelemetryEvent:
        dto = TelemetryEventCreate(category="AI", source=source, payload=metrics)
        return self.tel_svc.ingest_event(dto)


class FinancialObservabilityService:
    def __init__(self, tel_svc: TelemetryService):
        self.tel_svc = tel_svc

    def track_financial_event(
        self, source: str, event_data: Dict[str, Any]
    ) -> TelemetryEvent:
        dto = TelemetryEventCreate(
            category="FINANCIAL", source=source, payload=event_data
        )
        return self.tel_svc.ingest_event(dto)


class OperationalIntelligenceService:
    def __init__(self, incident_repo: IncidentRepository):
        self.incident_repo = incident_repo

    def analyze_anomaly(
        self, title: str, severity: str, details: Dict[str, Any]
    ) -> Incident:
        """
        Simplified logic: if an anomaly is detected via Celery workers, it opens an incident.
        """
        incident = Incident(
            id=f"inc_{uuid.uuid4().hex}",
            title=title,
            description=str(details),
            severity=severity,
            status="OPEN",
            created_at=datetime.utcnow(),
        )
        return self.incident_repo.save(incident)


class SLOService:
    def __init__(self, repo: SLORepository):
        self.repo = repo

    def register_slo(
        self, service_name: str, slo_name: str, target: float
    ) -> SLORecord:
        slo = SLORecord(
            id=f"slo_{uuid.uuid4().hex}",
            service_name=service_name,
            slo_name=slo_name,
            target_percentage=target,
            current_percentage=100.0,
            error_budget_remaining=100.0 - target,
            evaluated_at=datetime.utcnow(),
        )
        return self.repo.save(slo)


class DashboardService:
    def __init__(self, repo: DashboardRepository):
        self.repo = repo

    def create_dashboard(
        self, name: str, owner_id: str, layout: Dict[str, Any]
    ) -> DashboardConfig:
        dash = DashboardConfig(
            id=f"dash_{uuid.uuid4().hex}",
            name=name,
            owner_id=owner_id,
            layout_json=layout,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return self.repo.save(dash)
