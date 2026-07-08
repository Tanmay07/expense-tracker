from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .dependencies import get_db
from ..domain.models import (
    DecisionMemoryCreate,
    DecisionMemoryResponse,
    PatternCreate,
    PatternResponse,
    PersonalizationCreate,
    PersonalizationResponse,
    PolicyCacheCreate,
    PolicyCacheResponse,
    PredictionCreate,
    PredictionResponse,
    FinancialDNACreate,
    FinancialDNAResponse,
    BehaviorCreate,
    BehaviorResponse,
    LearningCreate,
    LearningResponse,
    ReplayResponse,
)
from ..infrastructure.repositories import (
    DecisionMemoryRepository,
    PatternRepository,
    PersonalizationRepository,
    PolicyDecisionCacheRepository,
    PredictionRepository,
    FinancialDNARepository,
    BehaviorRepository,
    LearningRepository,
    ReplayRepository,
)
from ..application.services import (
    DecisionMemoryService,
    PatternMiningService,
    PersonalizationService,
    PolicyDecisionCacheService,
    SuccessPredictionService,
    FinancialDNAService,
    BehaviorEvolutionService,
    ContinuousLearningService,
    LearningReplayService,
)

router = APIRouter()


# Memory
@router.post("/decision-memory", response_model=DecisionMemoryResponse)
def record_memory(data: DecisionMemoryCreate, db: Session = Depends(get_db)):
    service = DecisionMemoryService(DecisionMemoryRepository(db))
    return service.record_decision(data)


@router.get("/decision-memory/{decision_id}", response_model=DecisionMemoryResponse)
def get_memory(decision_id: str, db: Session = Depends(get_db)):
    service = DecisionMemoryService(DecisionMemoryRepository(db))
    memory = service.get_memory(decision_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory


# Patterns
@router.post("/patterns", response_model=PatternResponse)
def create_pattern(data: PatternCreate, db: Session = Depends(get_db)):
    service = PatternMiningService(PatternRepository(db))
    return service.create_pattern(data)


@router.get("/patterns/user/{user_id}", response_model=List[PatternResponse])
def get_patterns(user_id: str, db: Session = Depends(get_db)):
    service = PatternMiningService(PatternRepository(db))
    return service.get_patterns(user_id)


# Personalization
@router.put("/personalization/{user_id}", response_model=PersonalizationResponse)
def update_personalization(
    user_id: str, data: PersonalizationCreate, db: Session = Depends(get_db)
):
    service = PersonalizationService(PersonalizationRepository(db))
    return service.update_personalization(user_id, data)


@router.get("/personalization/{user_id}", response_model=PersonalizationResponse)
def get_personalization(user_id: str, db: Session = Depends(get_db)):
    service = PersonalizationService(PersonalizationRepository(db))
    p = service.get_personalization(user_id)
    if not p:
        raise HTTPException(status_code=404, detail="Personalization not found")
    return p


# Policy Cache
@router.post("/policy-cache", response_model=PolicyCacheResponse)
def cache_decision(data: PolicyCacheCreate, db: Session = Depends(get_db)):
    service = PolicyDecisionCacheService(PolicyDecisionCacheRepository(db))
    return service.cache_decision(data)


@router.get("/policy-cache/{decision_id}", response_model=PolicyCacheResponse)
def get_cache(decision_id: str, policy_version: int, db: Session = Depends(get_db)):
    service = PolicyDecisionCacheService(PolicyDecisionCacheRepository(db))
    c = service.check_cache(decision_id, policy_version)
    if not c:
        raise HTTPException(status_code=404, detail="Cache miss")
    return c


# Predictions
@router.post("/predictions", response_model=PredictionResponse)
def store_prediction(data: PredictionCreate, db: Session = Depends(get_db)):
    service = SuccessPredictionService(PredictionRepository(db))
    return service.store_prediction(data)


@router.get("/predictions/{decision_id}", response_model=PredictionResponse)
def get_prediction(decision_id: str, db: Session = Depends(get_db)):
    service = SuccessPredictionService(PredictionRepository(db))
    p = service.get_prediction(decision_id)
    if not p:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return p


# Financial DNA
@router.put("/financial-dna/{user_id}", response_model=FinancialDNAResponse)
def update_dna(user_id: str, data: FinancialDNACreate, db: Session = Depends(get_db)):
    service = FinancialDNAService(FinancialDNARepository(db))
    return service.update_dna(user_id, data)


@router.get("/financial-dna/{user_id}", response_model=FinancialDNAResponse)
def get_dna(user_id: str, db: Session = Depends(get_db)):
    service = FinancialDNAService(FinancialDNARepository(db))
    dna = service.get_dna(user_id)
    if not dna:
        raise HTTPException(status_code=404, detail="DNA not found")
    return dna


# Behavior Evolution
@router.post("/behavior", response_model=BehaviorResponse)
def record_evolution(data: BehaviorCreate, db: Session = Depends(get_db)):
    service = BehaviorEvolutionService(BehaviorRepository(db))
    return service.record_evolution(data)


@router.get("/behavior/user/{user_id}", response_model=List[BehaviorResponse])
def get_behavior(user_id: str, db: Session = Depends(get_db)):
    service = BehaviorEvolutionService(BehaviorRepository(db))
    return service.get_behavior_history(user_id)


# Continuous Learning
@router.post("/learning", response_model=LearningResponse)
def record_learning(data: LearningCreate, db: Session = Depends(get_db)):
    service = ContinuousLearningService(LearningRepository(db))
    return service.record_learning(data)


# Replay
@router.post("/replay/trigger")
def trigger_replay(session_id: str, replay_data: dict, db: Session = Depends(get_db)):
    service = LearningReplayService(ReplayRepository(db))
    service.trigger_replay(session_id, replay_data)
    return {"status": "triggered", "session_id": session_id}


@router.get("/replay/{session_id}", response_model=ReplayResponse)
def get_replay(session_id: str, db: Session = Depends(get_db)):
    service = LearningReplayService(ReplayRepository(db))
    r = service.get_replay(session_id)
    if not r:
        raise HTTPException(status_code=404, detail="Replay not found")
    return r
