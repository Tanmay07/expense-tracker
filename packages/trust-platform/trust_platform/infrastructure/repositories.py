from typing import List, Optional, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import (
    Base,
    ConsentRecordModel,
    AITrustRecordModel,
    RiskScoreModel,
    AuditLogModel,
    TrustScoreModel,
)

T = TypeVar("T", bound=Base)


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _add_and_commit(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance


class ConsentRepository(BaseRepository):
    async def record_consent(self, consent: ConsentRecordModel) -> ConsentRecordModel:
        return await self._add_and_commit(consent)

    async def get_active_consent(
        self, user_id: str, purpose: str
    ) -> Optional[ConsentRecordModel]:
        stmt = select(ConsentRecordModel).where(
            ConsentRecordModel.user_id == user_id,
            ConsentRecordModel.purpose == purpose,
            ConsentRecordModel.status == "GRANTED",
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class AITrustRepository(BaseRepository):
    async def log_ai_execution(self, record: AITrustRecordModel) -> AITrustRecordModel:
        return await self._add_and_commit(record)

    async def get_ai_record(self, record_id: str) -> Optional[AITrustRecordModel]:
        stmt = select(AITrustRecordModel).where(AITrustRecordModel.id == record_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class RiskRepository(BaseRepository):
    async def save_risk_score(self, risk: RiskScoreModel) -> RiskScoreModel:
        return await self._add_and_commit(risk)

    async def get_latest_risk_score(
        self, target_id: str, category: str
    ) -> Optional[RiskScoreModel]:
        stmt = (
            select(RiskScoreModel)
            .where(
                RiskScoreModel.target_id == target_id,
                RiskScoreModel.category == category,
            )
            .order_by(RiskScoreModel.evaluated_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class AuditRepository(BaseRepository):
    async def append_audit_log(self, log: AuditLogModel) -> AuditLogModel:
        # Audit logs are strictly append-only
        return await self._add_and_commit(log)

    async def search_audit_logs(self, target_id: str) -> List[AuditLogModel]:
        stmt = select(AuditLogModel).where(AuditLogModel.target_id == target_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class TrustRepository(BaseRepository):
    async def save_trust_score(self, score: TrustScoreModel) -> TrustScoreModel:
        return await self._add_and_commit(score)
