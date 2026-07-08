from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from strategy_sandbox.infrastructure.database import (
    ValidationProfileModel,
    SandboxRunModel,
    BenchmarkRecordModel,
    FitnessScoreModel,
    PromptValidationModel,
    ReplaySnapshotModel,
    SandboxCertificationModel,
)
from strategy_sandbox.domain.models import (
    ValidationProfile,
    SandboxRun,
    BenchmarkRecord,
    FitnessScore,
    PromptValidation,
    ReplaySnapshot,
    SandboxCertification,
)


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session


class ValidationProfileRepository(BaseRepository):
    def get_by_id(self, profile_id: str) -> Optional[ValidationProfile]:
        result = self.session.execute(
            select(ValidationProfileModel).where(
                ValidationProfileModel.id == profile_id
            )
        ).scalar_one_or_none()
        return ValidationProfile.model_validate(result) if result else None

    def list_profiles(self, limit: int = 50) -> List[ValidationProfile]:
        results = (
            self.session.execute(select(ValidationProfileModel).limit(limit))
            .scalars()
            .all()
        )
        return [ValidationProfile.model_validate(r) for r in results]

    def save(self, domain: ValidationProfile) -> ValidationProfile:
        model = self.session.execute(
            select(ValidationProfileModel).where(ValidationProfileModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ValidationProfileModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ValidationProfile.model_validate(model)


class SandboxRunRepository(BaseRepository):
    def get_by_id(self, run_id: str) -> Optional[SandboxRun]:
        result = self.session.execute(
            select(SandboxRunModel).where(SandboxRunModel.id == run_id)
        ).scalar_one_or_none()
        return SandboxRun.model_validate(result) if result else None

    def list_runs(
        self, asset_id: Optional[str] = None, limit: int = 50
    ) -> List[SandboxRun]:
        query = select(SandboxRunModel)
        if asset_id:
            query = query.where(SandboxRunModel.asset_id == asset_id)
        results = self.session.execute(query.limit(limit)).scalars().all()
        return [SandboxRun.model_validate(r) for r in results]

    def save(self, domain: SandboxRun) -> SandboxRun:
        model = self.session.execute(
            select(SandboxRunModel).where(SandboxRunModel.id == domain.id)
        ).scalar_one_or_none()

        dump = domain.model_dump(
            exclude={
                "profile",
                "fitness_score",
                "prompt_validation",
                "benchmark",
                "replay_snapshot",
                "certification",
            }
        )

        if not model:
            model = SandboxRunModel(**dump)
            self.session.add(model)
        else:
            for key, value in dump.items():
                setattr(model, key, value)

        self.session.commit()
        self.session.refresh(model)
        return SandboxRun.model_validate(model)


class FitnessRepository(BaseRepository):
    def get_by_run_id(self, run_id: str) -> Optional[FitnessScore]:
        result = self.session.execute(
            select(FitnessScoreModel).where(FitnessScoreModel.run_id == run_id)
        ).scalar_one_or_none()
        return FitnessScore.model_validate(result) if result else None

    def save(self, domain: FitnessScore) -> FitnessScore:
        model = self.session.execute(
            select(FitnessScoreModel).where(FitnessScoreModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = FitnessScoreModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return FitnessScore.model_validate(model)


class BenchmarkRepository(BaseRepository):
    def save(self, domain: BenchmarkRecord) -> BenchmarkRecord:
        model = self.session.execute(
            select(BenchmarkRecordModel).where(BenchmarkRecordModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = BenchmarkRecordModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return BenchmarkRecord.model_validate(model)


class PromptValidationRepository(BaseRepository):
    def save(self, domain: PromptValidation) -> PromptValidation:
        model = self.session.execute(
            select(PromptValidationModel).where(PromptValidationModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = PromptValidationModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return PromptValidation.model_validate(model)


class ReplayRepository(BaseRepository):
    def save(self, domain: ReplaySnapshot) -> ReplaySnapshot:
        model = self.session.execute(
            select(ReplaySnapshotModel).where(ReplaySnapshotModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ReplaySnapshotModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ReplaySnapshot.model_validate(model)


class CertificationRepository(BaseRepository):
    def get_by_run_id(self, run_id: str) -> Optional[SandboxCertification]:
        result = self.session.execute(
            select(SandboxCertificationModel).where(
                SandboxCertificationModel.run_id == run_id
            )
        ).scalar_one_or_none()
        return SandboxCertification.model_validate(result) if result else None

    def save(self, domain: SandboxCertification) -> SandboxCertification:
        model = self.session.execute(
            select(SandboxCertificationModel).where(
                SandboxCertificationModel.id == domain.id
            )
        ).scalar_one_or_none()
        if not model:
            model = SandboxCertificationModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return SandboxCertification.model_validate(model)
