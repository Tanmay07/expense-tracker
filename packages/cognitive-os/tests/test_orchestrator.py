import pytest
import asyncio
from cognitive_os.application.orchestrator import CognitiveOrchestrator, ReasoningTask
from cognitive_os.application.agent_registry import AgentRegistryService
from cognitive_os.domain.models import AgentRole

@pytest.fixture
def orchestrator():
    registry = AgentRegistryService()
    return CognitiveOrchestrator(registry)

@pytest.mark.asyncio
async def test_orchestrator_parallel_execution(orchestrator):
    tasks = [
        ReasoningTask(task_id="t1", description="Analyze budget", assigned_role=AgentRole.BUDGET, context={}),
        ReasoningTask(task_id="t2", description="Analyze risk", assigned_role=AgentRole.RISK, context={})
    ]
    
    results = await orchestrator.run_parallel(tasks)
    
    assert len(results) == 2
    assert any(r["agent"] == "BUDGET" for r in results)
    assert any(r["agent"] == "RISK" for r in results)
