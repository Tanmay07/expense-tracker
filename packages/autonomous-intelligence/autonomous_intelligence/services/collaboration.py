import uuid
import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from autonomous_intelligence.services.agent_registry import AgentRegistryService

logger = logging.getLogger(__name__)

class CollaborationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.registry = AgentRegistryService(session)

    async def delegate_task(self, source_agent_id: uuid.UUID, target_agent_id: uuid.UUID, task_details: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Delegating task from {source_agent_id} to {target_agent_id}")
        source_agent = await self.registry.get_agent(source_agent_id)
        target_agent = await self.registry.get_agent(target_agent_id)
        
        if not source_agent or not target_agent:
            raise ValueError("Invalid agents specified for delegation")
            
        return {
            "status": "ACCEPTED",
            "message": f"Task delegated to {target_agent.name}",
            "delegation_id": str(uuid.uuid4())
        }

    async def negotiate(self, agent_id_1: uuid.UUID, agent_id_2: uuid.UUID, conflict_context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Negotiating between {agent_id_1} and {agent_id_2}")
        return {
            "status": "RESOLVED",
            "agreed_parameters": conflict_context.get("proposed_parameters", {})
        }
