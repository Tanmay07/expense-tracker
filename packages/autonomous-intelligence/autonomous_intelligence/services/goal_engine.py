import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from autonomous_intelligence.domain.models import Goal, GoalType

class GoalEngineService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_goal(
        self,
        agent_id: uuid.UUID,
        name: str,
        goal_type: GoalType,
        target_amount: Optional[float] = None,
        target_date: Optional[str] = None,
        parameters: dict = None
    ) -> Goal:
        goal = Goal(
            agent_id=agent_id,
            name=name,
            goal_type=goal_type,
            target_amount=target_amount,
            target_date=target_date,
            parameters=parameters or {}
        )
        self.session.add(goal)
        await self.session.flush()
        return goal

    async def get_goal(self, goal_id: uuid.UUID) -> Optional[Goal]:
        stmt = select(Goal).where(Goal.id == goal_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_agent_goals(self, agent_id: uuid.UUID) -> List[Goal]:
        stmt = select(Goal).where(Goal.agent_id == agent_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_goal_progress(self, goal_id: uuid.UUID, current_amount: float) -> Optional[Goal]:
        goal = await self.get_goal(goal_id)
        if goal:
            goal.current_amount = current_amount
            if goal.target_amount and current_amount >= goal.target_amount:
                goal.status = "COMPLETED"
            await self.session.flush()
        return goal
