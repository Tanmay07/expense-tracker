from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from experimentation_platform.infrastructure.database import SessionLocal
from experimentation_platform.infrastructure.repositories import (
    FeatureRepository,
    FeatureFlagRepository,
    RolloutRepository,
    ExperimentRepository,
    ExperimentAnalyticsRepository,
)
from experimentation_platform.application.services import (
    FeatureRegistryService,
    FeatureFlagService,
    TargetingService,
    ProgressiveDeliveryService,
    ExperimentService,
    AIExperimentService,
    RollbackService,
    ExperimentAnalyticsService,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_feature_repo(db: Session = Depends(get_db)) -> FeatureRepository:
    return FeatureRepository(db)


def get_flag_repo(db: Session = Depends(get_db)) -> FeatureFlagRepository:
    return FeatureFlagRepository(db)


def get_rollout_repo(db: Session = Depends(get_db)) -> RolloutRepository:
    return RolloutRepository(db)


def get_experiment_repo(db: Session = Depends(get_db)) -> ExperimentRepository:
    return ExperimentRepository(db)


def get_analytics_repo(db: Session = Depends(get_db)) -> ExperimentAnalyticsRepository:
    return ExperimentAnalyticsRepository(db)


def get_feature_service(
    repo: FeatureRepository = Depends(get_feature_repo),
) -> FeatureRegistryService:
    return FeatureRegistryService(repo)


def get_targeting_service() -> TargetingService:
    return TargetingService()


def get_flag_service(
    repo: FeatureFlagRepository = Depends(get_flag_repo),
    target_svc: TargetingService = Depends(get_targeting_service),
) -> FeatureFlagService:
    return FeatureFlagService(repo, target_svc)


def get_delivery_service(
    repo: RolloutRepository = Depends(get_rollout_repo),
) -> ProgressiveDeliveryService:
    return ProgressiveDeliveryService(repo)


def get_experiment_service(
    repo: ExperimentRepository = Depends(get_experiment_repo),
) -> ExperimentService:
    return ExperimentService(repo)


def get_ai_experiment_service(
    repo: ExperimentRepository = Depends(get_experiment_repo),
) -> AIExperimentService:
    return AIExperimentService(repo)


def get_rollback_service(
    flag_repo: FeatureFlagRepository = Depends(get_flag_repo),
) -> RollbackService:
    return RollbackService(flag_repo)


def get_analytics_service(
    repo: ExperimentAnalyticsRepository = Depends(get_analytics_repo),
) -> ExperimentAnalyticsService:
    return ExperimentAnalyticsService(repo)
