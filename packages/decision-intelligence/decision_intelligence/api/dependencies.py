from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.repositories import CandidateRepository
from ..application.services import OptimizationService

def get_candidate_repo(db: Session = Depends(get_db)):
    return CandidateRepository(db)

def get_optimization_svc(
    repo: CandidateRepository = Depends(get_candidate_repo)
) -> OptimizationService:
    return OptimizationService(repo)
