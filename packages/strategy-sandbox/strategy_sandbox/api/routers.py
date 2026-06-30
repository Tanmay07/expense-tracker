from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from strategy_sandbox.domain.models import (
    SandboxRun, SandboxRunCreate, ValidationProfile, ValidationProfileCreate,
    FitnessScore, PromptValidation, BenchmarkRecord, SandboxCertification
)
from strategy_sandbox.application.services import (
    StrategySandboxService, ValidationProfileService, FitnessScoringService,
    PromptValidationService, BenchmarkService, CertificationService
)
from strategy_sandbox.api.dependencies import (
    get_sandbox_service, get_profile_service, get_fitness_service,
    get_prompt_service, get_benchmark_service, get_cert_service,
    get_run_repo, get_profile_repo
)
from strategy_sandbox.infrastructure.repositories import (
    SandboxRunRepository, ValidationProfileRepository
)

router = APIRouter()

@router.post("/validation-profiles")
def create_profile(
    dto: ValidationProfileCreate,
    svc: ValidationProfileService = Depends(get_profile_service)
) -> ValidationProfile:
    return svc.create_profile(dto)

@router.get("/validation-profiles", response_model=List[ValidationProfile])
def list_profiles(
    repo: ValidationProfileRepository = Depends(get_profile_repo)
) -> List[ValidationProfile]:
    return repo.list_profiles()

@router.post("/sandbox/runs")
def initiate_run(
    dto: SandboxRunCreate,
    svc: StrategySandboxService = Depends(get_sandbox_service)
) -> SandboxRun:
    try:
        return svc.initiate_run(dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/sandbox/runs", response_model=List[SandboxRun])
def list_runs(
    asset_id: Optional[str] = None,
    repo: SandboxRunRepository = Depends(get_run_repo)
) -> List[SandboxRun]:
    return repo.list_runs(asset_id=asset_id)

@router.get("/sandbox/runs/{run_id}")
def get_run(
    run_id: str,
    repo: SandboxRunRepository = Depends(get_run_repo)
) -> SandboxRun:
    run = repo.get_by_id(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@router.post("/fitness/{run_id}")
def calculate_fitness(
    run_id: str,
    svc: FitnessScoringService = Depends(get_fitness_service)
) -> FitnessScore:
    return svc.calculate_fitness(run_id)

@router.post("/prompt-validation/{run_id}")
def validate_prompt(
    run_id: str,
    prompt_text: str,
    svc: PromptValidationService = Depends(get_prompt_service)
) -> PromptValidation:
    return svc.validate_prompt(run_id, prompt_text)

@router.post("/benchmarks/{run_id}")
def execute_benchmark(
    run_id: str,
    svc: BenchmarkService = Depends(get_benchmark_service)
) -> BenchmarkRecord:
    return svc.execute_benchmark(run_id)

@router.post("/certifications/{run_id}")
def grant_certification(
    run_id: str,
    level: str,
    svc: CertificationService = Depends(get_cert_service)
) -> SandboxCertification:
    try:
        return svc.grant_certification(run_id, level)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
