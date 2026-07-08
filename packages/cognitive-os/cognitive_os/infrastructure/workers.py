import asyncio
from .celery_app import celery_app
from ..application.orchestrator import CognitiveOrchestrator
from ..application.agent_registry import AgentRegistryService
from ..application.reflection_engine import ReflectionEngine

# Instantiating services (in a real app, use proper dependency injection)
registry = AgentRegistryService()
orchestrator = CognitiveOrchestrator(registry)
reflection_engine = ReflectionEngine()

@celery_app.task(bind=True, max_retries=3)
def execute_mission(self, mission_id: str, context: dict):
    """
    Background worker that runs the Cognitive Orchestrator for a specific mission.
    """
    try:
        # Run the async orchestrator in a synchronous celery task wrapper
        result = asyncio.run(orchestrator.orchestrate_mission(mission_id, context))
        
        # Trigger reflection asynchronously after execution
        reflect_on_mission.delay(mission_id, result)
        
        return result
    except Exception as e:
        self.retry(exc=e, countdown=60) # Retry after 1 minute

@celery_app.task(bind=True)
def reflect_on_mission(self, mission_id: str, execution_data: dict):
    """
    Background worker that evaluates mission outcome.
    """
    reflection_result = reflection_engine.evaluate_mission_outcome(mission_id, execution_data)
    
    # Store reflection result in Learning Platform (stub)
    print(f"Mission {mission_id} completed with score: {reflection_result.success_score}")
    
    return reflection_result.model_dump()
