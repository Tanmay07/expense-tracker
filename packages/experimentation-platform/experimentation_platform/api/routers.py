from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from experimentation_platform.domain.models import Feature, FeatureCreate
from experimentation_platform.application.services import (
    FeatureRegistryService,
    FeatureFlagService,
    ExperimentService,
    RollbackService,
)
from experimentation_platform.api.dependencies import (
    get_feature_service,
    get_flag_service,
    get_experiment_service,
    get_rollback_service,
)

router = APIRouter()


@router.post("/features", response_model=Feature)
def register_feature(
    dto: FeatureCreate, svc: FeatureRegistryService = Depends(get_feature_service)
):
    return svc.register_feature(dto)


@router.get("/features/{name}", response_model=Feature)
def get_feature(name: str, svc: FeatureRegistryService = Depends(get_feature_service)):
    feat = svc.get_feature(name)
    if not feat:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feat


class EvaluateReq(BaseModel):
    feature_id: str
    context: Dict[str, Any]


@router.post("/feature-flags/evaluate", response_model=Dict[str, bool])
def evaluate_flag(
    req: EvaluateReq, svc: FeatureFlagService = Depends(get_flag_service)
):
    result = svc.evaluate(req.feature_id, req.context)
    return {"is_enabled": result}


class AssignReq(BaseModel):
    experiment_id: str
    context: Dict[str, Any]


@router.post("/experiments/assign", response_model=Dict[str, str])
def assign_experiment(
    req: AssignReq, svc: ExperimentService = Depends(get_experiment_service)
):
    variant = svc.assign_bucket(req.experiment_id, req.context)
    return {"variant": variant}


class RollbackReq(BaseModel):
    reason: str


@router.post("/rollback/{feature_id}")
def rollback_feature(
    feature_id: str,
    req: RollbackReq,
    svc: RollbackService = Depends(get_rollback_service),
):
    svc.trigger_rollback(feature_id, req.reason)
    return {"status": "rollback_triggered"}
