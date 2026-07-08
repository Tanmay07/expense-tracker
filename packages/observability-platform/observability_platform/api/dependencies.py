from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from observability_platform.infrastructure.database import SessionLocal
from observability_platform.infrastructure.repositories import (
    TelemetryRepository,
    MetricRepository,
    IncidentRepository,
    SLORepository,
    DashboardRepository,
)
from observability_platform.application.services import (
    TelemetryService,
    MetricsService,
    AIObservabilityService,
    FinancialObservabilityService,
    OperationalIntelligenceService,
    SLOService,
    DashboardService,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_telemetry_repo(db: Session = Depends(get_db)) -> TelemetryRepository:
    return TelemetryRepository(db)


def get_metric_repo(db: Session = Depends(get_db)) -> MetricRepository:
    return MetricRepository(db)


def get_incident_repo(db: Session = Depends(get_db)) -> IncidentRepository:
    return IncidentRepository(db)


def get_slo_repo(db: Session = Depends(get_db)) -> SLORepository:
    return SLORepository(db)


def get_dashboard_repo(db: Session = Depends(get_db)) -> DashboardRepository:
    return DashboardRepository(db)


def get_telemetry_service(
    repo: TelemetryRepository = Depends(get_telemetry_repo),
) -> TelemetryService:
    return TelemetryService(repo)


def get_metrics_service(
    repo: MetricRepository = Depends(get_metric_repo),
) -> MetricsService:
    return MetricsService(repo)


def get_ai_obs_service(
    tel_svc: TelemetryService = Depends(get_telemetry_service),
) -> AIObservabilityService:
    return AIObservabilityService(tel_svc)


def get_fin_obs_service(
    tel_svc: TelemetryService = Depends(get_telemetry_service),
) -> FinancialObservabilityService:
    return FinancialObservabilityService(tel_svc)


def get_intelligence_service(
    repo: IncidentRepository = Depends(get_incident_repo),
) -> OperationalIntelligenceService:
    return OperationalIntelligenceService(repo)


def get_slo_service(repo: SLORepository = Depends(get_slo_repo)) -> SLOService:
    return SLOService(repo)


def get_dashboard_service(
    repo: DashboardRepository = Depends(get_dashboard_repo),
) -> DashboardService:
    return DashboardService(repo)
