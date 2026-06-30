from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from hierarchical_learning.infrastructure.database import SessionLocal
from hierarchical_learning.infrastructure.repositories import (
    GlobalLearningRepository, RegionalLearningRepository, HouseholdLearningRepository,
    PersonalLearningRepository, KnowledgePromotionRepository, ConsentRepository,
    HouseholdConsensusRepository
)
from hierarchical_learning.application.services import (
    LearningHierarchyService, PersonalLearningService, KnowledgePromotionService,
    PrivacyBoundaryService, ConsensusService
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_global_repo(db: Session = Depends(get_db)) -> GlobalLearningRepository:
    return GlobalLearningRepository(db)

def get_regional_repo(db: Session = Depends(get_db)) -> RegionalLearningRepository:
    return RegionalLearningRepository(db)

def get_household_repo(db: Session = Depends(get_db)) -> HouseholdLearningRepository:
    return HouseholdLearningRepository(db)

def get_personal_repo(db: Session = Depends(get_db)) -> PersonalLearningRepository:
    return PersonalLearningRepository(db)

def get_consent_repo(db: Session = Depends(get_db)) -> ConsentRepository:
    return ConsentRepository(db)

def get_promotion_repo(db: Session = Depends(get_db)) -> KnowledgePromotionRepository:
    return KnowledgePromotionRepository(db)

def get_consensus_repo(db: Session = Depends(get_db)) -> HouseholdConsensusRepository:
    return HouseholdConsensusRepository(db)

def get_privacy_service(consent_repo: ConsentRepository = Depends(get_consent_repo)) -> PrivacyBoundaryService:
    return PrivacyBoundaryService(consent_repo)

def get_hierarchy_service(
    global_repo: GlobalLearningRepository = Depends(get_global_repo),
    regional_repo: RegionalLearningRepository = Depends(get_regional_repo),
    household_repo: HouseholdLearningRepository = Depends(get_household_repo),
    personal_repo: PersonalLearningRepository = Depends(get_personal_repo)
) -> LearningHierarchyService:
    return LearningHierarchyService(global_repo, regional_repo, household_repo, personal_repo)

def get_personal_service(
    repo: PersonalLearningRepository = Depends(get_personal_repo),
    privacy_svc: PrivacyBoundaryService = Depends(get_privacy_service)
) -> PersonalLearningService:
    return PersonalLearningService(repo, privacy_svc)

def get_promotion_service(
    repo: KnowledgePromotionRepository = Depends(get_promotion_repo)
) -> KnowledgePromotionService:
    return KnowledgePromotionService(repo)

def get_consensus_service(
    repo: HouseholdConsensusRepository = Depends(get_consensus_repo)
) -> ConsensusService:
    return ConsensusService(repo)
