from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from validation_registry.infrastructure.database import (
    ArtifactRecordModel, ArtifactLineageModel, EvidencePackageModel, ReuseEvaluationModel
)
from validation_registry.domain.models import (
    ArtifactRecord, ArtifactLineage, EvidencePackage, ReuseEvaluation
)

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

class ArtifactRepository(BaseRepository):
    def get_by_id(self, artifact_id: str) -> Optional[ArtifactRecord]:
        result = self.session.execute(
            select(ArtifactRecordModel).where(ArtifactRecordModel.id == artifact_id)
        ).scalar_one_or_none()
        return ArtifactRecord.model_validate(result) if result else None

    def list_artifacts(self, category: Optional[str] = None, limit: int = 50) -> List[ArtifactRecord]:
        query = select(ArtifactRecordModel)
        if category:
            query = query.where(ArtifactRecordModel.category == category)
        results = self.session.execute(query.limit(limit)).scalars().all()
        return [ArtifactRecord.model_validate(r) for r in results]

    def save(self, domain: ArtifactRecord) -> ArtifactRecord:
        model = self.session.execute(
            select(ArtifactRecordModel).where(ArtifactRecordModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ArtifactRecordModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ArtifactRecord.model_validate(model)


class ArtifactLineageRepository(BaseRepository):
    def get_by_source_id(self, source_id: str) -> List[ArtifactLineage]:
        results = self.session.execute(
            select(ArtifactLineageModel).where(ArtifactLineageModel.source_id == source_id)
        ).scalars().all()
        return [ArtifactLineage.model_validate(r) for r in results]

    def save(self, domain: ArtifactLineage) -> ArtifactLineage:
        model = self.session.execute(
            select(ArtifactLineageModel).where(ArtifactLineageModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ArtifactLineageModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ArtifactLineage.model_validate(model)


class EvidenceRepository(BaseRepository):
    def get_by_id(self, package_id: str) -> Optional[EvidencePackage]:
        result = self.session.execute(
            select(EvidencePackageModel).where(EvidencePackageModel.id == package_id)
        ).scalar_one_or_none()
        return EvidencePackage.model_validate(result) if result else None

    def save(self, domain: EvidencePackage) -> EvidencePackage:
        model = self.session.execute(
            select(EvidencePackageModel).where(EvidencePackageModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = EvidencePackageModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return EvidencePackage.model_validate(model)


class ReuseRepository(BaseRepository):
    def get_by_input_hash(self, input_hash: str) -> Optional[ReuseEvaluation]:
        result = self.session.execute(
            select(ReuseEvaluationModel).where(ReuseEvaluationModel.input_hash == input_hash)
        ).scalar_one_or_none()
        return ReuseEvaluation.model_validate(result) if result else None

    def save(self, domain: ReuseEvaluation) -> ReuseEvaluation:
        model = self.session.execute(
            select(ReuseEvaluationModel).where(ReuseEvaluationModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ReuseEvaluationModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ReuseEvaluation.model_validate(model)
