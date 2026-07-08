from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from platform_readiness.infrastructure.database import (
    ArchitectureFitnessModel, SecurityCertificationModel,
    PerformanceCertificationModel, ChaosExperimentModel,
    CostModel, ProductionReadinessModel
)
from platform_readiness.domain.models import (
    ArchitectureFitness, SecurityCertification,
    PerformanceCertification, ChaosExperiment,
    CostProjection, ProductionReadiness
)

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

class ArchitectureFitnessRepository(BaseRepository):
    def save(self, domain: ArchitectureFitness) -> ArchitectureFitness:
        model = self.session.execute(
            select(ArchitectureFitnessModel).where(ArchitectureFitnessModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ArchitectureFitnessModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ArchitectureFitness.model_validate(model)

class SecurityCertificationRepository(BaseRepository):
    def save(self, domain: SecurityCertification) -> SecurityCertification:
        model = self.session.execute(
            select(SecurityCertificationModel).where(SecurityCertificationModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = SecurityCertificationModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return SecurityCertification.model_validate(model)

class PerformanceCertificationRepository(BaseRepository):
    def save(self, domain: PerformanceCertification) -> PerformanceCertification:
        model = self.session.execute(
            select(PerformanceCertificationModel).where(PerformanceCertificationModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = PerformanceCertificationModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return PerformanceCertification.model_validate(model)

class ChaosExperimentRepository(BaseRepository):
    def save(self, domain: ChaosExperiment) -> ChaosExperiment:
        model = self.session.execute(
            select(ChaosExperimentModel).where(ChaosExperimentModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ChaosExperimentModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ChaosExperiment.model_validate(model)

class CostRepository(BaseRepository):
    def save(self, domain: CostProjection) -> CostProjection:
        model = self.session.execute(
            select(CostModel).where(CostModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = CostModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return CostProjection.model_validate(model)

class ProductionReadinessRepository(BaseRepository):
    def save(self, domain: ProductionReadiness) -> ProductionReadiness:
        model = self.session.execute(
            select(ProductionReadinessModel).where(ProductionReadinessModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ProductionReadinessModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ProductionReadiness.model_validate(model)

    def get_by_version(self, version_tag: str) -> Optional[ProductionReadiness]:
        model = self.session.execute(
            select(ProductionReadinessModel).where(ProductionReadinessModel.version_tag == version_tag)
        ).scalar_one_or_none()
        return ProductionReadiness.model_validate(model) if model else None
