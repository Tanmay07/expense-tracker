from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from .dependencies import get_copilot_service, get_action_plan_service, get_simulation_service
from ..application.services import CopilotService, ActionPlanService, SimulationRequestService
from ..domain.models import CopilotMode, ActionPlan, SimulationRequest

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    conversation_id: str
    content: str
    mode: CopilotMode = CopilotMode.DAILY_COACH

class ChatResponse(BaseModel):
    response: str
    mode: str

class PlanRequest(BaseModel):
    user_id: str
    conversation_id: str
    goal: str

class SimulationReq(BaseModel):
    user_id: str
    scenario: str
    assumptions: Dict[str, Any]

@router.post("/chat", response_model=ChatResponse)
def copilot_chat(
    request: ChatRequest,
    service: CopilotService = Depends(get_copilot_service)
):
    try:
        resp = service.handle_message(
            request.user_id, request.conversation_id, request.content, request.mode
        )
        return ChatResponse(response=resp, mode=request.mode.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/action-plans", response_model=ActionPlan)
def create_action_plan(
    request: PlanRequest,
    service: ActionPlanService = Depends(get_action_plan_service)
):
    return service.generate_plan(request.user_id, request.conversation_id, request.goal)

@router.post("/simulations", response_model=SimulationRequest)
def request_simulation(
    request: SimulationReq,
    service: SimulationRequestService = Depends(get_simulation_service)
):
    return service.request_simulation(request.user_id, request.scenario, request.assumptions)
