from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from platform_readiness.api.dependencies import (
    get_db,
    get_architecture_fitness_service,
    get_security_certification_service,
    get_performance_certification_service,
    get_chaos_engineering_service,
    get_cost_engineering_service,
    get_production_readiness_service
)

router = APIRouter(prefix="/api/v1/readiness", tags=["Readiness"])

class ComponentRequest(BaseModel):
    component_name: str

class PerformanceRequest(BaseModel):
    endpoint: str

class ChaosRequest(BaseModel):
    scenario_name: str
    target_component: str

class ScoreRequest(BaseModel):
    version_tag: str

@router.get("/")
def check_service_health():
    return {"status": "ok", "service": "platform-readiness"}

@router.post("/architecture")
def run_architecture_audit(
    req: ComponentRequest,
    db: Session = Depends(get_db)
):
    svc = get_architecture_fitness_service(db)
    result = svc.run_architecture_audit(req.component_name)
    return result

@router.post("/security")
def run_security_assessment(
    req: ComponentRequest,
    db: Session = Depends(get_db)
):
    svc = get_security_certification_service(db)
    result = svc.run_security_assessment(req.component_name)
    return result

@router.post("/performance")
def run_performance_certification(
    req: PerformanceRequest,
    db: Session = Depends(get_db)
):
    svc = get_performance_certification_service(db)
    result = svc.run_performance_certification(req.endpoint)
    return result

@router.post("/chaos")
def run_chaos_experiment(
    req: ChaosRequest,
    db: Session = Depends(get_db)
):
    svc = get_chaos_engineering_service(db)
    result = svc.run_chaos_experiment(req.scenario_name, req.target_component)
    return result

@router.post("/cost")
def estimate_cost(
    req: ComponentRequest,
    db: Session = Depends(get_db)
):
    svc = get_cost_engineering_service(db)
    result = svc.estimate_cost(req.component_name)
    return result

@router.post("/score")
def calculate_readiness_score(
    req: ScoreRequest,
    db: Session = Depends(get_db)
):
    svc = get_production_readiness_service(db)
    result = svc.calculate_readiness(req.version_tag)
    return result

@router.get("/score/{version_tag}")
def get_certification(
    version_tag: str,
    db: Session = Depends(get_db)
):
    svc = get_production_readiness_service(db)
    result = svc.get_certification(version_tag)
    if not result:
        raise HTTPException(status_code=404, detail="Certification not found")
    return result
