import uuid
import logging
from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from autonomous_intelligence.domain.models import Evaluation

logger = logging.getLogger(__name__)

class EvaluationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def record_evaluation(
        self,
        agent_id: uuid.UUID,
        mission_id: Optional[uuid.UUID],
        metrics: dict
    ) -> Evaluation:
        logger.info(f"Recording evaluation for agent {agent_id}")
        evaluation = Evaluation(
            agent_id=agent_id,
            mission_id=mission_id,
            goal_completion_score=metrics.get("goal_completion_score", 0.0),
            financial_impact=metrics.get("financial_impact", 0.0),
            recommendation_acceptance_rate=metrics.get("recommendation_acceptance_rate", 0.0),
            execution_success_rate=metrics.get("execution_success_rate", 0.0),
            ai_quality_score=metrics.get("ai_quality_score", 0.0),
            latency_ms=metrics.get("latency_ms", 0.0),
            cost_usd=metrics.get("cost_usd", 0.0),
            trust_score=metrics.get("trust_score", 0.0),
            user_satisfaction_score=metrics.get("user_satisfaction_score", 0.0),
            evaluation_period_start=metrics.get("period_start", datetime.now(timezone.utc)),
            evaluation_period_end=metrics.get("period_end", datetime.now(timezone.utc))
        )
        self.session.add(evaluation)
        await self.session.flush()
        return evaluation

    async def get_agent_scorecard(self, agent_id: uuid.UUID) -> dict:
        stmt = select(Evaluation).where(Evaluation.agent_id == agent_id)
        result = await self.session.execute(stmt)
        evaluations = list(result.scalars().all())
        
        if not evaluations:
            return {"agent_id": str(agent_id), "status": "NO_DATA"}
            
        avg_trust = sum(e.trust_score for e in evaluations) / len(evaluations)
        return {
            "agent_id": str(agent_id),
            "average_trust_score": avg_trust,
            "total_evaluations": len(evaluations)
        }
