from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from experimentation_platform.infrastructure.database import (
    FeatureModel,
    FeatureFlagModel,
    RolloutModel,
    ExperimentModel,
    ExperimentResultModel,
)
from experimentation_platform.domain.models import (
    Feature,
    FeatureFlag,
    Rollout,
    Experiment,
    ExperimentResult,
)


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session


class FeatureRepository(BaseRepository):
    def save(self, domain: Feature) -> Feature:
        model = self.session.execute(
            select(FeatureModel).where(FeatureModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = FeatureModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return Feature.model_validate(model)

    def get_by_name(self, name: str) -> Optional[Feature]:
        model = self.session.execute(
            select(FeatureModel).where(FeatureModel.name == name)
        ).scalar_one_or_none()
        return Feature.model_validate(model) if model else None


class FeatureFlagRepository(BaseRepository):
    def save(self, domain: FeatureFlag) -> FeatureFlag:
        model = self.session.execute(
            select(FeatureFlagModel).where(FeatureFlagModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = FeatureFlagModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return FeatureFlag.model_validate(model)

    def get_by_feature_id(self, feature_id: str) -> Optional[FeatureFlag]:
        model = self.session.execute(
            select(FeatureFlagModel).where(FeatureFlagModel.feature_id == feature_id)
        ).scalar_one_or_none()
        return FeatureFlag.model_validate(model) if model else None


class RolloutRepository(BaseRepository):
    def save(self, domain: Rollout) -> Rollout:
        model = self.session.execute(
            select(RolloutModel).where(RolloutModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = RolloutModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return Rollout.model_validate(model)


class ExperimentRepository(BaseRepository):
    def save(self, domain: Experiment) -> Experiment:
        model = self.session.execute(
            select(ExperimentModel).where(ExperimentModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ExperimentModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return Experiment.model_validate(model)


class ExperimentAnalyticsRepository(BaseRepository):
    def save(self, domain: ExperimentResult) -> ExperimentResult:
        model = self.session.execute(
            select(ExperimentResultModel).where(ExperimentResultModel.id == domain.id)
        ).scalar_one_or_none()
        if not model:
            model = ExperimentResultModel(**domain.model_dump())
            self.session.add(model)
        else:
            for key, value in domain.model_dump().items():
                setattr(model, key, value)
        self.session.commit()
        self.session.refresh(model)
        return ExperimentResult.model_validate(model)
