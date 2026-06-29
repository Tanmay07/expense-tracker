import os
from celery import Celery
from ..infrastructure.database import SessionLocal
from ..infrastructure.repositories import CandidateRepository
from .services import OptimizationService, OpportunityCostService

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("decision_intelligence_tasks", broker=CELERY_BROKER_URL)

@celery_app.task(name="optimize_portfolio")
def optimize_portfolio(user_id: str, profile_data: dict):
    db = SessionLocal()
    try:
        repo = CandidateRepository(db)
        svc = OptimizationService(repo)
        svc.generate_candidates(user_id, profile_data)
        # Would emit a domain event here to notify Mission Control
    finally:
        db.close()

@celery_app.task(name="calculate_opportunity_cost")
def calculate_opportunity_cost(candidate_id: str):
    db = SessionLocal()
    try:
        repo = CandidateRepository(db)
        svc = OpportunityCostService(repo)
        svc.calculate_cost(candidate_id)
    finally:
        db.close()
