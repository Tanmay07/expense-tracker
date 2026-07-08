import uuid
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from autonomous_intelligence.domain.models import Memory

logger = logging.getLogger(__name__)


class MemoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def store_memory(
        self,
        agent_id: uuid.UUID,
        memory_type: str,
        content: Dict[str, Any],
        reference_id: Optional[str] = None,
    ) -> Memory:
        logger.info(f"Storing {memory_type} memory for agent {agent_id}")
        memory = Memory(
            agent_id=agent_id,
            memory_type=memory_type,
            content=content,
            reference_id=reference_id,
        )
        self.session.add(memory)
        await self.session.flush()
        return memory

    async def retrieve_memories(
        self, agent_id: uuid.UUID, memory_type: Optional[str] = None, limit: int = 50
    ) -> List[Memory]:
        stmt = select(Memory).where(Memory.agent_id == agent_id)
        if memory_type:
            stmt = stmt.where(Memory.memory_type == memory_type)
        stmt = stmt.order_by(Memory.created_at.desc()).limit(limit)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
