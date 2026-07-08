from typing import Generator
from sqlalchemy.orm import Session
from platform_readiness.infrastructure.database import SessionLocal
from platform_readiness.infrastructure.repositories import (
    ArchitectureFitnessRepository,
    SecurityCertificationRepository,
    PerformanceCertificationRepository,
    ChaosExperimentRepository,
    CostRepository,
    ProductionReadinessRepository,
)
from platform_readiness.application.services import (
    ArchitectureFitnessService,
    SecurityCertificationService,
    PerformanceCertificationService,
    ChaosEngineeringService,
    CostEngineeringService,
    ProductionReadinessService,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_architecture_fitness_service(db: Session) -> ArchitectureFitnessService:
    repo = ArchitectureFitnessRepository(db)
    return ArchitectureFitnessService(repo)


def get_security_certification_service(db: Session) -> SecurityCertificationService:
    repo = SecurityCertificationRepository(db)
    return SecurityCertificationService(repo)


def get_performance_certification_service(
    db: Session,
) -> PerformanceCertificationService:
    repo = PerformanceCertificationRepository(db)
    return PerformanceCertificationService(repo)


def get_chaos_engineering_service(db: Session) -> ChaosEngineeringService:
    repo = ChaosExperimentRepository(db)
    return ChaosEngineeringService(repo)


def get_cost_engineering_service(db: Session) -> CostEngineeringService:
    repo = CostRepository(db)
    return CostEngineeringService(repo)


def get_production_readiness_service(db: Session) -> ProductionReadinessService:
    repo = ProductionReadinessRepository(db)
    return ProductionReadinessService(repo)
