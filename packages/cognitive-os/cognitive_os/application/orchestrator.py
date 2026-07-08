from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio

from .agent_registry import AgentRegistryService
from ..domain.models import AgentRole
from ..infrastructure.ai_router import ModelRoutingClient
from ..infrastructure.redis_store import TransientStateStore
from ..infrastructure.telemetry import trace_ai_reasoning

class ReasoningTask(BaseModel):
    task_id: str
    description: str
    assigned_role: AgentRole
    context: Dict[str, Any]

class CognitiveOrchestrator:
    """
    Orchestrates the cognitive loop:
    Observe -> Understand -> Reason -> Plan -> Evaluate -> Approval -> Execute -> Reflect -> Learn
    """
    def __init__(self, registry: AgentRegistryService, router: ModelRoutingClient, transient_store: TransientStateStore):
        self.registry = registry
        self.router = router
        self.transient_store = transient_store

    @trace_ai_reasoning(agent_role="dynamic", model="routed")
    async def _execute_agent_reasoning(self, task: ReasoningTask) -> Dict[str, Any]:
        """
        Executes reasoning using the abstract Model Routing Platform.
        Maintains transient in-flight state in Redis.
        """
        agent_def = self.registry.get_agent(task.assigned_role)
        if not agent_def:
            raise ValueError(f"Unknown agent role: {task.assigned_role}")

        # Construct system prompt based on agent definition (Role, capabilities, policies)
        system_prompt = f"You are the {agent_def.role.value}. {agent_def.description}\n"
        
        # Save transient state (e.g., indicating agent has started reasoning)
        state_key = f"inflight:reasoning:{task.task_id}"
        self.transient_store.save_in_flight_state(state_key, {"status": "STARTED", "agent": agent_def.role.value})

        # Request capability from Model Routing Platform (Agnostic of underlying LLM)
        ai_response = await self.router.execute_cognitive_task(
            capabilities=agent_def.capabilities,
            policies=agent_def.policies,
            prompt=task.description,
            context=task.context
        )
        
        result = {
            "task_id": task.task_id,
            "agent": agent_def.role.value,
            "status": "COMPLETED",
            "reasoning": ai_response,
            "plan": [],
            "requires_approval": False
        }
        
        # Update transient state
        self.transient_store.save_in_flight_state(state_key, result)
        return result

    async def run_sequential(self, tasks: List[ReasoningTask]) -> List[Dict[str, Any]]:
        """Run tasks one after another, passing context."""
        results = []
        for task in tasks:
            result = await self._execute_agent_reasoning(task)
            results.append(result)
        return results

    async def run_parallel(self, tasks: List[ReasoningTask]) -> List[Dict[str, Any]]:
        """Run tasks concurrently for independent reasoning."""
        coroutines = [self._execute_agent_reasoning(task) for task in tasks]
        return await asyncio.gather(*coroutines)

    async def orchestrate_mission(self, mission_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        High-level entry point where the SUPERVISOR routes the mission.
        """
        supervisor_task = ReasoningTask(
            task_id=f"{mission_id}_supervision",
            description="Analyze context and delegate to appropriate sub-agents.",
            assigned_role=AgentRole.SUPERVISOR,
            context=context
        )
        
        supervision_result = await self._execute_agent_reasoning(supervisor_task)
        
        # Clear transient state for the supervisor task after routing
        self.transient_store.delete_state(f"inflight:reasoning:{supervisor_task.task_id}")
        
        return supervision_result
