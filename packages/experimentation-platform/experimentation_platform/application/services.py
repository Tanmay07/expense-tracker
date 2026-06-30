import uuid
import mmh3
from datetime import datetime
from typing import Optional, List, Dict, Any

from experimentation_platform.domain.models import (
    Feature, FeatureCreate, FeatureFlag, Rollout,
    Experiment, ExperimentCreate, ExperimentResult
)
from experimentation_platform.infrastructure.repositories import (
    FeatureRepository, FeatureFlagRepository, RolloutRepository,
    ExperimentRepository, ExperimentAnalyticsRepository
)

class FeatureRegistryService:
    def __init__(self, repo: FeatureRepository):
        self.repo = repo
        
    def register_feature(self, dto: FeatureCreate) -> Feature:
        feat = Feature(
            id=f"feat_{uuid.uuid4().hex}",
            name=dto.name,
            version=dto.version,
            description=dto.description,
            feature_type=dto.feature_type,
            owner_id=dto.owner_id,
            dependencies=dto.dependencies,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return self.repo.save(feat)
        
    def get_feature(self, name: str) -> Optional[Feature]:
        return self.repo.get_by_name(name)

class TargetingService:
    def evaluate_rules(self, rules: Dict[str, Any], context: Dict[str, Any]) -> bool:
        # Minimal Mock JSONLogic evaluator
        # Assumes rules like {"attribute": "country", "operator": "eq", "value": "US"}
        if not rules:
            return True
            
        attr = rules.get("attribute")
        val = rules.get("value")
        if attr and attr in context:
            return context[attr] == val
        return False

class FeatureFlagService:
    def __init__(self, repo: FeatureFlagRepository, target_svc: TargetingService):
        self.repo = repo
        self.target_svc = target_svc
        
    def evaluate(self, feature_id: str, context: Dict[str, Any]) -> bool:
        flag = self.repo.get_by_feature_id(feature_id)
        if not flag or not flag.is_enabled:
            return False
            
        if flag.flag_type == "BOOLEAN":
            return flag.default_value or False
            
        elif flag.flag_type == "PERCENTAGE" and flag.rollout_percentage is not None:
            # Deterministic hash based on entity_id (user/household)
            entity_id = context.get("user_id", context.get("session_id", "unknown"))
            # 0 to 99
            bucket = mmh3.hash(f"{feature_id}_{entity_id}") % 100
            return bucket < flag.rollout_percentage
            
        elif flag.flag_type == "TARGETING" and flag.targeting_rules_json:
            return self.target_svc.evaluate_rules(flag.targeting_rules_json, context)
            
        return False

class ProgressiveDeliveryService:
    def __init__(self, repo: RolloutRepository):
        self.repo = repo
        
    def promote_rollout(self, rollout_id: str, next_stage: str) -> Rollout:
        # Mock logic
        rollout = Rollout(
            id=rollout_id,
            feature_id="mock_feat",
            current_stage=next_stage,
            updated_at=datetime.utcnow()
        )
        return self.repo.save(rollout)

class ExperimentService:
    def __init__(self, repo: ExperimentRepository):
        self.repo = repo
        
    def create_experiment(self, dto: ExperimentCreate) -> Experiment:
        exp = Experiment(
            id=f"exp_{uuid.uuid4().hex}",
            name=dto.name,
            experiment_type=dto.experiment_type,
            variants_json=dto.variants_json,
            weights_json=dto.weights_json,
            target_metrics=dto.target_metrics,
            status="DRAFT"
        )
        return self.repo.save(exp)
        
    def assign_bucket(self, experiment_id: str, context: Dict[str, Any]) -> str:
        # Fetch weights, default to 50/50 for MVP
        entity_id = context.get("user_id", context.get("session_id", "unknown"))
        bucket_hash = mmh3.hash(f"{experiment_id}_{entity_id}") % 100
        
        # Simple hardcoded routing for MVP: 50% variant_a, 50% variant_b
        if bucket_hash < 50:
            return "variant_a"
        return "variant_b"

class AIExperimentService(ExperimentService):
    """
    Extends base experimentation for AI specific prompt comparisons.
    """
    pass

class RollbackService:
    def __init__(self, flag_repo: FeatureFlagRepository):
        self.flag_repo = flag_repo
        
    def trigger_rollback(self, feature_id: str, reason: str):
        flag = self.flag_repo.get_by_feature_id(feature_id)
        if flag:
            flag.is_enabled = False
            self.flag_repo.save(flag)

class ExperimentAnalyticsService:
    def __init__(self, repo: ExperimentAnalyticsRepository):
        self.repo = repo
        
    def calculate_results(self, experiment_id: str) -> ExperimentResult:
        res = ExperimentResult(
            id=f"expr_{uuid.uuid4().hex}",
            experiment_id=experiment_id,
            results_json={"variant_a_success": 45, "variant_b_success": 55},
            winning_variant_id="variant_b",
            calculated_at=datetime.utcnow()
        )
        return self.repo.save(res)
