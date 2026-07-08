from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from analytics_platform.infrastructure.database import SessionLocal
from analytics_platform.infrastructure.repositories import (
    ExperimentRegistryRepository,
    StatisticalGuardrailRepository,
    KPICatalogRepository,
    InsightRepository,
    ExecutiveReportRepository,
)
from analytics_platform.application.services import (
    ExperimentRegistryService,
    StatisticalGuardrailService,
    KPICatalogService,
    ContinuousImprovementService,
    InsightEngineService,
    ExecutiveReportingService,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_experiment_repo(db: Session = Depends(get_db)) -> ExperimentRegistryRepository:
    return ExperimentRegistryRepository(db)


def get_guardrail_repo(db: Session = Depends(get_db)) -> StatisticalGuardrailRepository:
    return StatisticalGuardrailRepository(db)


def get_kpi_repo(db: Session = Depends(get_db)) -> KPICatalogRepository:
    return KPICatalogRepository(db)


def get_insight_repo(db: Session = Depends(get_db)) -> InsightRepository:
    return InsightRepository(db)


def get_report_repo(db: Session = Depends(get_db)) -> ExecutiveReportRepository:
    return ExecutiveReportRepository(db)


def get_guardrail_service(
    repo: StatisticalGuardrailRepository = Depends(get_guardrail_repo),
) -> StatisticalGuardrailService:
    return StatisticalGuardrailService(repo)


def get_experiment_service(
    repo: ExperimentRegistryRepository = Depends(get_experiment_repo),
    guardrail_svc: StatisticalGuardrailService = Depends(get_guardrail_service),
) -> ExperimentRegistryService:
    return ExperimentRegistryService(repo, guardrail_svc)


def get_kpi_service(
    repo: KPICatalogRepository = Depends(get_kpi_repo),
) -> KPICatalogService:
    return KPICatalogService(repo)


def get_improvement_service() -> ContinuousImprovementService:
    return ContinuousImprovementService()


def get_insight_service(
    repo: InsightRepository = Depends(get_insight_repo),
) -> InsightEngineService:
    return InsightEngineService(repo)


def get_reporting_service(
    repo: ExecutiveReportRepository = Depends(get_report_repo),
) -> ExecutiveReportingService:
    return ExecutiveReportingService(repo)
