from fastapi import APIRouter, Depends
from typing import List

from .dependencies import get_registry_svc, get_eval_svc
from ..application.services import PolicyRegistryService, PolicyEvaluationService
from ..domain.models import ExecutionPolicy, PolicyContext, EvaluationResult

router = APIRouter()


@router.post("/policies", response_model=ExecutionPolicy)
def register_policy(
    policy: ExecutionPolicy, svc: PolicyRegistryService = Depends(get_registry_svc)
):
    return svc.register_policy(policy)


@router.get("/policies", response_model=List[ExecutionPolicy])
def list_policies(svc: PolicyRegistryService = Depends(get_registry_svc)):
    return svc.list_active_policies()


@router.post("/evaluate", response_model=EvaluationResult)
def evaluate_context(
    context: PolicyContext, svc: PolicyEvaluationService = Depends(get_eval_svc)
):
    return svc.evaluate(context)
