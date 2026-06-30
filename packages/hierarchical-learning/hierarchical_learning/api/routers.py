from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException

from hierarchical_learning.domain.models import (
    GlobalLearning, RegionalLearning, HouseholdLearning, PersonalLearning,
    KnowledgePromotion, ConsentProfile, HouseholdConsensus,
    KnowledgePromotionCreate, PersonalLearningCreate, HouseholdConsensusCreate,
    ConsentProfileUpdate
)
from hierarchical_learning.application.services import (
    LearningHierarchyService, PersonalLearningService, KnowledgePromotionService,
    PrivacyBoundaryService, ConsensusService
)
from hierarchical_learning.api.dependencies import (
    get_hierarchy_service, get_personal_service, get_promotion_service,
    get_privacy_service, get_consensus_service, get_consent_repo, get_global_repo
)
from hierarchical_learning.infrastructure.repositories import ConsentRepository, GlobalLearningRepository

router = APIRouter()

@router.get("/hierarchy/stack")
def get_full_knowledge_stack(
    user_id: str,
    topic: str,
    household_id: Optional[str] = None,
    region_id: Optional[str] = None,
    hierarchy_svc: LearningHierarchyService = Depends(get_hierarchy_service)
) -> Dict[str, Any]:
    return hierarchy_svc.get_full_knowledge_stack(user_id, household_id, region_id, topic)

@router.post("/personal")
def update_personal_learning(
    dto: PersonalLearningCreate,
    svc: PersonalLearningService = Depends(get_personal_service)
) -> PersonalLearning:
    return svc.update_learning(dto)

@router.get("/global/{topic}")
def get_global_learning(
    topic: str,
    repo: GlobalLearningRepository = Depends(get_global_repo)
) -> GlobalLearning:
    result = repo.get_by_topic(topic)
    if not result:
        raise HTTPException(status_code=404, detail="Global knowledge not found for topic")
    return result

@router.post("/promotions")
def propose_knowledge_promotion(
    dto: KnowledgePromotionCreate,
    svc: KnowledgePromotionService = Depends(get_promotion_service)
) -> KnowledgePromotion:
    return svc.propose_promotion(dto)

@router.post("/consensus")
def build_household_consensus(
    dto: HouseholdConsensusCreate,
    svc: ConsensusService = Depends(get_consensus_service)
) -> HouseholdConsensus:
    return svc.build_consensus(dto)

@router.get("/privacy/{user_id}")
def get_consent_profile(
    user_id: str,
    repo: ConsentRepository = Depends(get_consent_repo)
) -> ConsentProfile:
    profile = repo.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Consent profile not found")
    return profile

@router.put("/privacy/{user_id}")
def update_consent_profile(
    user_id: str,
    dto: ConsentProfileUpdate,
    repo: ConsentRepository = Depends(get_consent_repo)
) -> ConsentProfile:
    profile = repo.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Consent profile not found")
    # For simplicity, we directly modify here in the router.
    # In a full CQRS approach, this should go through a CommandHandler.
    for k, v in dto.model_dump(exclude_unset=True).items():
        setattr(profile, k, v)
    return repo.save(profile)
