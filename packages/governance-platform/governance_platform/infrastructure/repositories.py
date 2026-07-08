from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from governance_platform.infrastructure.database import (
    GovernancePolicyModel,
    TrustScoreModel,
    MaturityRecordModel,
    AIGovernanceModel,
    EvidenceLedgerModel,
    WorkflowStateModel,
)
from governance_platform.domain.models import (
    GovernancePolicy,
    TrustScore,
    MaturityRecord,
    AIGovernanceRecord,
    EvidenceLedgerEntry,
    WorkflowState,
)


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session


class PolicyRepository(BaseRepository):
    def get_by_id(self, policy_id: str) -> Optional[GovernancePolicy]:
        result = self.session.execute(
            select(GovernancePolicyModel).where(GovernancePolicyModel.id == policy_id)
        ).scalar_one_or_none()
        return GovernancePolicy.model_validate(result) if result else None

    def save(self, domain: GovernancePolicy) -> GovernancePolicy:
        model = self.session.execute(
            select(GovernancePolicyModel).where(GovernancePolicyModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = GovernancePolicyModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return GovernancePolicy.model_validate(model)


class TrustRepository(BaseRepository):
    def get_by_asset(self, asset_id: str) -> Optional[TrustScore]:
        result = self.session.execute(
            select(TrustScoreModel).where(TrustScoreModel.asset_id == asset_id)
        ).scalar_one_or_none()
        return TrustScore.model_validate(result) if result else None

    def save(self, domain: TrustScore) -> TrustScore:
        model = self.session.execute(
            select(TrustScoreModel).where(TrustScoreModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = TrustScoreModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return TrustScore.model_validate(model)


class MaturityRepository(BaseRepository):
    def get_by_asset(self, asset_id: str) -> Optional[MaturityRecord]:
        result = self.session.execute(
            select(MaturityRecordModel).where(MaturityRecordModel.asset_id == asset_id)
        ).scalar_one_or_none()
        return MaturityRecord.model_validate(result) if result else None

    def save(self, domain: MaturityRecord) -> MaturityRecord:
        model = self.session.execute(
            select(MaturityRecordModel).where(MaturityRecordModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = MaturityRecordModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return MaturityRecord.model_validate(model)


class AIGovernanceRepository(BaseRepository):
    def save(self, domain: AIGovernanceRecord) -> AIGovernanceRecord:
        model = self.session.execute(
            select(AIGovernanceModel).where(AIGovernanceModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = AIGovernanceModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return AIGovernanceRecord.model_validate(model)


class EvidenceRepository(BaseRepository):
    def get_latest_by_asset(self, asset_id: str) -> Optional[EvidenceLedgerEntry]:
        result = self.session.execute(
            select(EvidenceLedgerModel)
            .where(EvidenceLedgerModel.asset_id == asset_id)
            .order_by(EvidenceLedgerModel.recorded_at.desc())
            .limit(1)
        ).scalar_one_or_none()
        return EvidenceLedgerEntry.model_validate(result) if result else None

    def save(self, domain: EvidenceLedgerEntry) -> EvidenceLedgerEntry:
        model = self.session.execute(
            select(EvidenceLedgerModel).where(EvidenceLedgerModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = EvidenceLedgerModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return EvidenceLedgerEntry.model_validate(model)


class WorkflowRepository(BaseRepository):
    def save(self, domain: WorkflowState) -> WorkflowState:
        model = self.session.execute(
            select(WorkflowStateModel).where(WorkflowStateModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = WorkflowStateModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return WorkflowState.model_validate(model)
