import uuid
import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from autonomous_intelligence.domain.models import Agent, HITLClassification

logger = logging.getLogger(__name__)


class HITLService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def determine_classification(
        self, agent: Agent, proposed_action: Dict[str, Any]
    ) -> HITLClassification:
        logger.info(
            f"Determining HITL classification for agent {agent.id} action {proposed_action}"
        )
        tool_name = proposed_action.get("tool")

        # High-risk operations require approval
        if tool_name in ["execute_trade", "wire_transfer"]:
            return HITLClassification.REQUIRE_APPROVAL

        # Medium-risk operations recommend to user
        if tool_name in ["update_budget", "rebalance_portfolio"]:
            return HITLClassification.RECOMMEND

        return HITLClassification.FULLY_AUTOMATED

    async def request_human_approval(
        self, agent_id: uuid.UUID, action_details: Dict[str, Any]
    ) -> str:
        logger.info(f"Requesting human approval for agent {agent_id}")
        approval_id = str(uuid.uuid4())
        # In reality, this would emit an ApprovalRequested event to be picked up by the UI
        return approval_id
