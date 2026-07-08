import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from hierarchical_learning.domain.models import (
    PersonalLearning,
    KnowledgePromotion, HouseholdConsensus,
    KnowledgePromotionCreate, PersonalLearningCreate, HouseholdConsensusCreate
)
from hierarchical_learning.infrastructure.repositories import (
    GlobalLearningRepository, RegionalLearningRepository, HouseholdLearningRepository,
    PersonalLearningRepository, KnowledgePromotionRepository, ConsentRepository,
    HouseholdConsensusRepository
)

class PrivacyBoundaryService:
    def __init__(self, consent_repo: ConsentRepository):
        self.consent_repo = consent_repo
        
    def can_aggregate(self, user_id: str) -> bool:
        profile = self.consent_repo.get_profile(user_id)
        if profile and not profile.allow_anonymous_aggregation:
            return False
        return True

    def can_share_household(self, user_id: str) -> bool:
        profile = self.consent_repo.get_profile(user_id)
        return profile.allow_household_sharing if profile else False

class KnowledgePromotionService:
    def __init__(self, promotion_repo: KnowledgePromotionRepository):
        self.promotion_repo = promotion_repo
        
    def propose_promotion(self, dto: KnowledgePromotionCreate) -> KnowledgePromotion:
        promotion = KnowledgePromotion(
            id=f"kp_{uuid.uuid4().hex}",
            source_scope=dto.source_scope,
            target_scope=dto.target_scope,
            source_id=dto.source_id,
            topic=dto.topic,
            proposed_knowledge_json=dto.proposed_knowledge_json,
            promotion_status="OBSERVED",
            evidence_json=dto.evidence_json,
            created_at=datetime.utcnow()
        )
        return self.promotion_repo.save(promotion)

class ConfidenceService:
    def calculate_confidence(self, sample_size: int, evidence_quality: float, behavior_stability: float) -> float:
        # Simplistic confidence scoring based on sample size and stability
        base = min(sample_size / 1000.0, 0.7)
        return min(base + (evidence_quality * 0.2) + (behavior_stability * 0.1), 1.0)

class DecayService:
    def evaluate_decay(self, last_updated: datetime, base_decay_rate: float) -> float:
        # Calculate time-based decay
        days_since = (datetime.utcnow() - last_updated).days
        decay = days_since * base_decay_rate
        return min(decay, 1.0)

class ConsensusService:
    def __init__(self, consensus_repo: HouseholdConsensusRepository):
        self.consensus_repo = consensus_repo
        
    def build_consensus(self, dto: HouseholdConsensusCreate) -> HouseholdConsensus:
        # In a real system, this might use LiteLLM to analyze competing preferences.
        # For now, we stub the generation and save it as PENDING.
        consensus = HouseholdConsensus(
            id=f"hc_{uuid.uuid4().hex}",
            household_id=dto.household_id,
            conflict_topic=dto.conflict_topic,
            competing_preferences_json=dto.competing_preferences_json,
            status="PENDING",
            created_at=datetime.utcnow()
        )
        # Background task would pick this up, resolve it, and emit ConsensusReached
        return self.consensus_repo.save(consensus)

class PersonalLearningService:
    def __init__(self, repo: PersonalLearningRepository, privacy_svc: PrivacyBoundaryService):
        self.repo = repo
        self.privacy_svc = privacy_svc
        
    def update_learning(self, dto: PersonalLearningCreate) -> PersonalLearning:
        existing = self.repo.get_by_user_and_topic(dto.user_id, dto.topic)
        if existing:
            existing.personal_knowledge_json.update(dto.personal_knowledge_json)
            existing.financial_dna_snapshot = dto.financial_dna_snapshot
            existing.last_updated = datetime.utcnow()
            existing.version += 1
            return self.repo.save(existing)
            
        new_learning = PersonalLearning(
            id=f"pl_{uuid.uuid4().hex}",
            user_id=dto.user_id,
            topic=dto.topic,
            personal_knowledge_json=dto.personal_knowledge_json,
            financial_dna_snapshot=dto.financial_dna_snapshot,
            last_updated=datetime.utcnow(),
            decay_rate=0.01,
            version=1
        )
        return self.repo.save(new_learning)

class LearningHierarchyService:
    def __init__(
        self, 
        global_repo: GlobalLearningRepository,
        regional_repo: RegionalLearningRepository,
        household_repo: HouseholdLearningRepository,
        personal_repo: PersonalLearningRepository
    ):
        self.global_repo = global_repo
        self.regional_repo = regional_repo
        self.household_repo = household_repo
        self.personal_repo = personal_repo

    def get_full_knowledge_stack(self, user_id: str, household_id: Optional[str], region_id: Optional[str], topic: str) -> Dict[str, Any]:
        """
        Retrieves knowledge from all scopes, resolving conflicts hierarchically.
        Overrides: Personal > Household > Regional > Global
        """
        stack = {}
        
        # 1. Global
        gl = self.global_repo.get_by_topic(topic)
        if gl:
            stack["global"] = gl.aggregated_knowledge_json
            
        # 2. Regional
        if region_id:
            rl = self.regional_repo.get_by_region_and_topic(region_id, topic)
            if rl:
                stack["regional"] = rl.regional_knowledge_json
                
        # 3. Household
        if household_id:
            hl = self.household_repo.get_by_household_and_topic(household_id, topic)
            if hl:
                stack["household"] = hl.household_knowledge_json
                
        # 4. Personal
        pl = self.personal_repo.get_by_user_and_topic(user_id, topic)
        if pl:
            stack["personal"] = pl.personal_knowledge_json
            
        return stack
