from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel

from .dependencies import get_capability_svc, get_routing_svc, get_approval_svc
from ..application.services import (
    ExecutionCapabilityService,
    RoutingService,
    ApprovalService,
)
from ..domain.models import ExecutionCapability, ExecutionRoute, ApprovalRequest

router = APIRouter()


@router.post("/capabilities", response_model=ExecutionCapability)
def register_capability(
    capability: ExecutionCapability,
    svc: ExecutionCapabilityService = Depends(get_capability_svc),
):
    return svc.register_capability(capability)


@router.get("/capabilities", response_model=List[ExecutionCapability])
def list_capabilities(svc: ExecutionCapabilityService = Depends(get_capability_svc)):
    return svc.list_capabilities()


class RouteRequest(BaseModel):
    step_id: str
    required_tags: List[str]


@router.post("/routing", response_model=ExecutionRoute)
def route_execution(req: RouteRequest, svc: RoutingService = Depends(get_routing_svc)):
    route = svc.determine_route(req.step_id, req.required_tags)
    if not route:
        raise HTTPException(status_code=404, detail="No matching capability found")
    return route


class ApprovalPayload(BaseModel):
    execution_step_id: str
    capability_id: str
    requested_by: str


@router.post("/approvals", response_model=ApprovalRequest)
def request_approval(
    req: ApprovalPayload, svc: ApprovalService = Depends(get_approval_svc)
):
    return svc.request_approval(
        req.execution_step_id, req.capability_id, req.requested_by
    )
