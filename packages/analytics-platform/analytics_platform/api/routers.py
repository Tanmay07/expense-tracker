from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from analytics_platform.domain.models import (
    ExperimentRegistry,
    ExperimentRegistryCreate,
    KPICatalog,
    Insight,
    ExecutiveReport,
)
from analytics_platform.application.services import (
    ExperimentRegistryService,
    StatisticalGuardrailService,
    KPICatalogService,
    InsightEngineService,
    ExecutiveReportingService,
)
from analytics_platform.api.dependencies import (
    get_experiment_service,
    get_guardrail_service,
    get_kpi_service,
    get_insight_service,
    get_reporting_service,
)

router = APIRouter()


@router.post("/experiments/registry", response_model=ExperimentRegistry)
def register_experiment(
    dto: ExperimentRegistryCreate,
    svc: ExperimentRegistryService = Depends(get_experiment_service),
):
    return svc.register_experiment(dto)


@router.get("/experiments/registry/{name}", response_model=ExperimentRegistry)
def get_experiment(
    name: str, svc: ExperimentRegistryService = Depends(get_experiment_service)
):
    exp = svc.get_experiment(name)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp


@router.post("/kpis", response_model=KPICatalog)
def create_kpi(dto: KPICatalog, svc: KPICatalogService = Depends(get_kpi_service)):
    return svc.register_kpi(dto)


@router.get("/kpis/{name}", response_model=KPICatalog)
def get_kpi(name: str, svc: KPICatalogService = Depends(get_kpi_service)):
    kpi = svc.get_kpi(name)
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    return kpi


class GuardrailCalcReq(BaseModel):
    baseline_conversion: float
    sample_size: int
    alpha: float = 0.05
    power: float = 0.8


@router.post("/experiments/guardrails/mde")
def calculate_mde(
    req: GuardrailCalcReq,
    svc: StatisticalGuardrailService = Depends(get_guardrail_service),
):
    mde = svc.calculate_mde(
        req.baseline_conversion, req.sample_size, req.alpha, req.power
    )
    return {"minimum_detectable_effect": mde}


class InsightReq(BaseModel):
    title: str
    description: str
    severity: str = "INFO"


@router.post("/insights", response_model=Insight)
def generate_insight(
    req: InsightReq, svc: InsightEngineService = Depends(get_insight_service)
):
    return svc.generate_insight(req.title, req.description, req.severity)


@router.post("/reports/weekly", response_model=ExecutiveReport)
def generate_weekly_report(
    svc: ExecutiveReportingService = Depends(get_reporting_service),
):
    return svc.generate_weekly_report()
