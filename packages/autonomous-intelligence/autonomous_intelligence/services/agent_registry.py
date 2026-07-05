import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from autonomous_intelligence.domain.models import Agent, RiskClassification
from autonomous_intelligence.domain.events import AgentRegistered

class AgentRegistryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_agent(
        self,
        name: str,
        role: str,
        owner: str,
        description: str = "",
        capabilities: dict = None,
        allowed_tools: List[str] = None,
        risk_classification: RiskClassification = RiskClassification.MEDIUM,
        policies: List[str] = None
    ) -> Agent:
        agent = Agent(
            name=name,
            role=role,
            owner=owner,
            description=description,
            capabilities=capabilities or {},
            allowed_tools=allowed_tools or [],
            risk_classification=risk_classification,
            policies=policies or []
        )
        self.session.add(agent)
        await self.session.flush()
        
        # In a real event-driven system, we'd publish AgentRegistered to Redis/Kafka here
        
        return agent

    async def get_agent(self, agent_id: uuid.UUID) -> Optional[Agent]:
        stmt = select(Agent).where(Agent.id == agent_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_agents(self, skip: int = 0, limit: int = 100) -> List[Agent]:
        stmt = select(Agent).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
