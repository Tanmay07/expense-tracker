from typing import Dict, Any
from ..infrastructure.repositories import (
    DecisionMemoryRepository, PatternRepository, PersonalizationRepository,
    PolicyDecisionCacheRepository, PredictionRepository, FinancialDNARepository,
    BehaviorRepository, LearningRepository, ReplayRepository
)
from ..domain.models import (
    DecisionMemoryCreate, PatternCreate, PersonalizationCreate, PolicyCacheCreate,
    PredictionCreate, FinancialDNACreate, BehaviorCreate, LearningCreate, ReplayCreate
)
from .tasks import detect_patterns_task, generate_prediction_task, update_behavior_task, build_replay_task

class DecisionMemoryService:
    def __init__(self, repo: DecisionMemoryRepository):
        self.repo = repo

    def record_decision(self, data: DecisionMemoryCreate):
        # 1. Store in PostgreSQL
        record = self.repo.create(data.model_dump())
        
        # 2. Trigger asynchronous learning
        detect_patterns_task.delay(data.user_id)
        generate_prediction_task.delay(data.decision_id)
        
        return record

    def get_memory(self, decision_id: str):
        return self.repo.get_by_decision_id(decision_id)

    def list_user_memory(self, user_id: str):
        return self.repo.list_by_user(user_id)

class PatternMiningService:
    def __init__(self, repo: PatternRepository):
        self.repo = repo

    def create_pattern(self, data: PatternCreate):
        return self.repo.create(data.model_dump())

    def get_patterns(self, user_id: str):
        return self.repo.list_by_user(user_id)

class PersonalizationService:
    def __init__(self, repo: PersonalizationRepository):
        self.repo = repo

    def update_personalization(self, user_id: str, data: PersonalizationCreate):
        return self.repo.upsert(user_id, data.model_dump(exclude={"user_id"}))

    def get_personalization(self, user_id: str):
        return self.repo.get_by_user(user_id)

class PolicyDecisionCacheService:
    def __init__(self, repo: PolicyDecisionCacheRepository):
        self.repo = repo

    def cache_decision(self, data: PolicyCacheCreate):
        return self.repo.create(data.model_dump())

    def check_cache(self, decision_id: str, policy_version: int):
        return self.repo.get_valid_cache(decision_id, policy_version)

    def invalidate(self, decision_id: str):
        self.repo.invalidate(decision_id)

class SuccessPredictionService:
    def __init__(self, repo: PredictionRepository):
        self.repo = repo

    def store_prediction(self, data: PredictionCreate):
        return self.repo.create(data.model_dump())

    def get_prediction(self, decision_id: str):
        return self.repo.get_latest_by_decision(decision_id)

class FinancialDNAService:
    def __init__(self, repo: FinancialDNARepository):
        self.repo = repo

    def update_dna(self, user_id: str, data: FinancialDNACreate):
        # In a real app, this triggers an event for BehaviorEvolution
        record = self.repo.upsert(user_id, data.model_dump(exclude={"user_id"}))
        update_behavior_task.delay(user_id)
        return record

    def get_dna(self, user_id: str):
        return self.repo.get_by_user(user_id)

class BehaviorEvolutionService:
    def __init__(self, repo: BehaviorRepository):
        self.repo = repo

    def record_evolution(self, data: BehaviorCreate):
        return self.repo.create(data.model_dump())

    def get_behavior_history(self, user_id: str):
        return self.repo.list_by_user(user_id)

class ContinuousLearningService:
    def __init__(self, repo: LearningRepository):
        self.repo = repo

    def record_learning(self, data: LearningCreate):
        return self.repo.create(data.model_dump())

class LearningReplayService:
    def __init__(self, repo: ReplayRepository):
        self.repo = repo

    def trigger_replay(self, session_id: str, replay_data: Dict[str, Any]):
        # Schedule the replay generation
        build_replay_task.delay(session_id, replay_data)
        
    def store_replay(self, data: ReplayCreate):
        return self.repo.create(data.model_dump())

    def get_replay(self, session_id: str):
        return self.repo.get_by_session(session_id)
