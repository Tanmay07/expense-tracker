import uuid
import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from autonomous_intelligence.domain.models import Mission, HITLClassification

logger = logging.getLogger(__name__)


class MissionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_mission(
        self,
        agent_id: uuid.UUID,
        name: str,
        hitl_classification: HITLClassification,
        goal_id: Optional[uuid.UUID] = None,
        description: str = "",
        plan: dict = None,
    ) -> Mission:
        logger.info(f"Creating mission {name} for agent {agent_id}")
        mission = Mission(
            agent_id=agent_id,
            goal_id=goal_id,
            name=name,
            description=description,
            plan=plan or {},
            hitl_classification=hitl_classification,
        )
        self.session.add(mission)
        await self.session.flush()
        return mission

    async def get_mission(self, mission_id: uuid.UUID) -> Optional[Mission]:
        stmt = select(Mission).where(Mission.id == mission_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_agent_missions(self, agent_id: uuid.UUID) -> List[Mission]:
        stmt = select(Mission).where(Mission.agent_id == agent_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_mission_status(
        self, mission_id: uuid.UUID, status: str
    ) -> Optional[Mission]:
        mission = await self.get_mission(mission_id)
        if mission:
            mission.status = status
            await self.session.flush()
        return mission
