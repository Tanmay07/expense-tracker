import uuid
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from autonomous_intelligence.domain.models import Plan

logger = logging.getLogger(__name__)

class PlanningService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def generate_plan(
        self,
        agent_id: uuid.UUID,
        mission_id: Optional[uuid.UUID],
        horizon: str,
        context: Dict[str, Any]
    ) -> Plan:
        logger.info(f"Generating {horizon} plan for agent {agent_id}")
        
        # In reality, this calls an LLM or Planning Engine logic
        content = {
            "steps": [
                {"action": "analyze_expenses", "timeframe": "day_1"},
                {"action": "propose_reallocation", "timeframe": "day_2"}
            ],
            "context_used": context
        }
        
        plan = Plan(
            agent_id=agent_id,
            mission_id=mission_id,
            horizon=horizon,
            content=content,
            is_contingency=context.get("is_contingency", False),
            is_alternative=context.get("is_alternative", False)
        )
        
        self.session.add(plan)
        await self.session.flush()
        return plan

    async def get_plan(self, plan_id: uuid.UUID) -> Optional[Plan]:
        stmt = select(Plan).where(Plan.id == plan_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_agent_plans(self, agent_id: uuid.UUID) -> List[Plan]:
        stmt = select(Plan).where(Plan.agent_id == agent_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
