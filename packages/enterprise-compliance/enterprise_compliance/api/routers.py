from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any

from .dependencies import (
    get_suitability_service, get_compliance_service, 
    get_policy_service, get_explainability_service
)
from ..application.services import (
    SuitabilityService, ComplianceService, PolicyService, ExplainabilityService, EvaluationResult
)
from ..domain.models import CompliancePolicy, SuitabilityProfile

router = APIRouter()

@router.post("/suitability/evaluate", response_model=SuitabilityProfile)
def evaluate_suitability(
    user_id: str,
    investment_params: Dict[str, Any],
    service: SuitabilityService = Depends(get_suitability_service)
):
    try:
        return service.evaluate_suitability(user_id, investment_params)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/compliance/evaluate", response_model=EvaluationResult)
def evaluate_compliance(
    user_id: str,
    context_id: str,
    transaction_data: Dict[str, Any],
    service: ComplianceService = Depends(get_compliance_service)
):
    return service.evaluate_transaction(user_id, context_id, transaction_data)

@router.get("/policies", response_model=List[CompliancePolicy])
def get_policies(service: PolicyService = Depends(get_policy_service)):
    return service.get_active_policies()

@router.post("/policies", response_model=CompliancePolicy)
def create_policy(
    policy_data: Dict[str, Any],
    service: PolicyService = Depends(get_policy_service)
):
    return service.create_policy(policy_data)

@router.get("/decision-governance/{context_id}/explain")
def explain_decision(
    context_id: str,
    service: ExplainabilityService = Depends(get_explainability_service)
):
    explanation = service.explain_decision(context_id)
    if "error" in explanation:
        raise HTTPException(status_code=404, detail=explanation["error"])
    return explanation
