import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from autonomous_intelligence.domain.models import Agent

logger = logging.getLogger(__name__)

class GovernanceService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def evaluate_policy_compliance(self, agent: Agent, proposed_action: Dict[str, Any]) -> bool:
        """
        Integrates with Execution Policy Engine and Governance Platform.
        In this mock, we just check if the action's tool is in the agent's allowed tools.
        """
        logger.info(f"Evaluating policy compliance for agent {agent.id} against action {proposed_action}")
        tool_name = proposed_action.get("tool")
        if not tool_name:
            return False
            
        if tool_name not in agent.allowed_tools:
            logger.warning(f"Policy violation: Agent {agent.id} attempted to use forbidden tool {tool_name}")
            return False
            
        return True
