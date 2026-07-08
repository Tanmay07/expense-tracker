import uuid
from fastapi import FastAPI, Depends, status
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from autonomous_intelligence.infrastructure.database import get_db_session
from autonomous_intelligence.domain.models import GoalType, HITLClassification
from autonomous_intelligence.services.agent_registry import AgentRegistryService
from autonomous_intelligence.services.orchestrator import AgentOrchestratorService
from autonomous_intelligence.services.goal_engine import GoalEngineService
from autonomous_intelligence.services.mission import MissionService

app = FastAPI(
    title="Autonomous Intelligence API",
    description="Enterprise Autonomous Financial Intelligence Platform",
    version="1.0.0"
)

# OpenTelemetry Instrumentation
FastAPIInstrumentor.instrument_app(app)

@app.post("/agents", status_code=status.HTTP_201_CREATED)
async def register_agent(
    payload: Dict[str, Any],
    session: AsyncSession = Depends(get_db_session)
):
    registry = AgentRegistryService(session)
    agent = await registry.register_agent(
        name=payload["name"],
        role=payload["role"],
        owner=payload["owner"],
        description=payload.get("description", ""),
        capabilities=payload.get("capabilities", {}),
        allowed_tools=payload.get("allowed_tools", []),
        policies=payload.get("policies", [])
    )
    return {"id": agent.id, "name": agent.name, "role": agent.role}

@app.get("/agents")
async def list_agents(
    session: AsyncSession = Depends(get_db_session)
):
    registry = AgentRegistryService(session)
    agents = await registry.list_agents()
    return [{"id": a.id, "name": a.name, "role": a.role} for a in agents]

@app.post("/orchestrator/execute")
async def execute_workflow(
    payload: Dict[str, Any],
    session: AsyncSession = Depends(get_db_session)
):
    orchestrator = AgentOrchestratorService(session)
    agent_id = uuid.UUID(payload["agent_id"])
    mission_id = uuid.UUID(payload["mission_id"])
    steps = payload.get("steps", [])
    
    result = await orchestrator.execute_sequential_workflow(agent_id, mission_id, steps)
    return result

@app.post("/goals")
async def create_goal(
    payload: Dict[str, Any],
    session: AsyncSession = Depends(get_db_session)
):
    engine = GoalEngineService(session)
    goal = await engine.create_goal(
        agent_id=uuid.UUID(payload["agent_id"]),
        name=payload["name"],
        goal_type=GoalType(payload["goal_type"]),
        target_amount=payload.get("target_amount")
    )
    return {"id": goal.id, "name": goal.name, "status": goal.status}

@app.post("/missions")
async def create_mission(
    payload: Dict[str, Any],
    session: AsyncSession = Depends(get_db_session)
):
    mission_svc = MissionService(session)
    mission = await mission_svc.create_mission(
        agent_id=uuid.UUID(payload["agent_id"]),
        name=payload["name"],
        hitl_classification=HITLClassification(payload.get("hitl_classification", "FULLY_AUTOMATED")),
        goal_id=uuid.UUID(payload["goal_id"]) if "goal_id" in payload else None
    )
    return {"id": mission.id, "name": mission.name, "status": mission.status}
