from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from ..application.agent_registry import AgentRegistryService
from ..application.mission_planning import MissionPlanningService
from ..domain.models import AgentDefinition, AgentRole
from ..domain.planning_models import MissionDefinition, GoalDefinition, TimeHorizon

router = APIRouter(prefix="/cognition", tags=["Cognitive OS"])

# Dependency Injection placeholders
def get_registry() -> AgentRegistryService:
    return AgentRegistryService()

def get_mission_planner() -> MissionPlanningService:
    return MissionPlanningService()

@router.get("/agents", response_model=List[AgentDefinition])
async def list_agents(registry: AgentRegistryService = Depends(get_registry)):
    return registry.get_all_agents()

@router.get("/agents/{role}", response_model=AgentDefinition)
async def get_agent(role: AgentRole, registry: AgentRegistryService = Depends(get_registry)):
    agent = registry.get_agent(role)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.post("/missions", response_model=MissionDefinition)
async def create_mission(goal: GoalDefinition, context: Dict[str, Any] = {}, planner: MissionPlanningService = Depends(get_mission_planner)):
    # Trigger mission generation based on goal
    return planner.generate_mission_for_goal(goal, context)

@router.get("/missions/pending", response_model=List[MissionDefinition])
async def list_pending_missions(planner: MissionPlanningService = Depends(get_mission_planner)):
    return planner.get_pending_missions()
