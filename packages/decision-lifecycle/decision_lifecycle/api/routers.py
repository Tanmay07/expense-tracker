from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List

from .dependencies import get_lifecycle_svc, get_planner_svc
from ..application.services import DecisionLifecycleService, ExecutionPlannerService
from ..domain.models import DecisionLifecycle, ExecutionPlan, LifecycleState

router = APIRouter()

@router.post("/decision-lifecycle/{decision_id}", response_model=DecisionLifecycle)
def initialize_lifecycle(
    decision_id: str,
    svc: DecisionLifecycleService = Depends(get_lifecycle_svc)
):
    return svc.initialize_lifecycle(decision_id)

@router.put("/decision-lifecycle/{decision_id}/state", response_model=DecisionLifecycle)
def transition_state(
    decision_id: str,
    new_state: LifecycleState,
    svc: DecisionLifecycleService = Depends(get_lifecycle_svc)
):
    try:
        lifecycle = svc.transition_state(decision_id, new_state)
        if not lifecycle:
            raise HTTPException(status_code=404, detail="Lifecycle not found")
        return lifecycle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/execution-plans/{decision_id}", response_model=ExecutionPlan)
def generate_plan(
    decision_id: str,
    proposed_actions: List[Dict[str, Any]],
    svc: ExecutionPlannerService = Depends(get_planner_svc)
):
    return svc.generate_plan(decision_id, proposed_actions)
