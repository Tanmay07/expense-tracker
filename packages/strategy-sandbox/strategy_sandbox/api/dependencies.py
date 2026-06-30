from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from strategy_sandbox.infrastructure.database import SessionLocal
from strategy_sandbox.infrastructure.repositories import (
    SandboxRunRepository, ValidationProfileRepository, FitnessRepository,
    PromptValidationRepository, BenchmarkRepository, CertificationRepository
)
from strategy_sandbox.application.services import (
    StrategySandboxService, ValidationProfileService, FitnessScoringService,
    PromptValidationService, BenchmarkService, CertificationService
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_run_repo(db: Session = Depends(get_db)) -> SandboxRunRepository:
    return SandboxRunRepository(db)

def get_profile_repo(db: Session = Depends(get_db)) -> ValidationProfileRepository:
    return ValidationProfileRepository(db)

def get_fitness_repo(db: Session = Depends(get_db)) -> FitnessRepository:
    return FitnessRepository(db)

def get_prompt_repo(db: Session = Depends(get_db)) -> PromptValidationRepository:
    return PromptValidationRepository(db)

def get_benchmark_repo(db: Session = Depends(get_db)) -> BenchmarkRepository:
    return BenchmarkRepository(db)

def get_cert_repo(db: Session = Depends(get_db)) -> CertificationRepository:
    return CertificationRepository(db)


def get_sandbox_service(
    run_repo: SandboxRunRepository = Depends(get_run_repo),
    profile_repo: ValidationProfileRepository = Depends(get_profile_repo)
) -> StrategySandboxService:
    return StrategySandboxService(run_repo, profile_repo)

def get_profile_service(repo: ValidationProfileRepository = Depends(get_profile_repo)) -> ValidationProfileService:
    return ValidationProfileService(repo)

def get_fitness_service(repo: FitnessRepository = Depends(get_fitness_repo)) -> FitnessScoringService:
    return FitnessScoringService(repo)

def get_prompt_service(repo: PromptValidationRepository = Depends(get_prompt_repo)) -> PromptValidationService:
    return PromptValidationService(repo)

def get_benchmark_service(repo: BenchmarkRepository = Depends(get_benchmark_repo)) -> BenchmarkService:
    return BenchmarkService(repo)

def get_cert_service(
    cert_repo: CertificationRepository = Depends(get_cert_repo),
    run_repo: SandboxRunRepository = Depends(get_run_repo)
) -> CertificationService:
    return CertificationService(cert_repo, run_repo)
