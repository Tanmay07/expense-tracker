from fastapi import APIRouter, Depends
from typing import Dict, Any

from .dependencies import get_optimization_svc
from ..application.services import OptimizationService
from ..application.tasks import optimize_portfolio, calculate_opportunity_cost

router = APIRouter()

@router.post("/decision-optimization/trigger")
def trigger_optimization(
    user_id: str,
    profile_data: Dict[str, Any],
):
    """
    Triggers the multi-objective optimization worker asynchronously.
    """
    optimize_portfolio.delay(user_id, profile_data)
    return {"status": "accepted", "message": "Optimization started in background"}

@router.post("/decision-optimization/sync")
def sync_optimization(
    user_id: str,
    profile_data: Dict[str, Any],
    svc: OptimizationService = Depends(get_optimization_svc)
):
    """
    Synchronous fallback for generating candidates instantly.
    """
    candidates = svc.generate_candidates(user_id, profile_data)
    return candidates

@router.post("/opportunity-cost/{candidate_id}")
def calculate_cost_async(
    candidate_id: str
):
    calculate_opportunity_cost.delay(candidate_id)
    return {"status": "accepted"}
