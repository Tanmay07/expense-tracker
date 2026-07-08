import os
from celery import Celery
from ..infrastructure.database import SessionLocal

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("decision_lifecycle_tasks", broker=CELERY_BROKER_URL)


@celery_app.task(name="monitor_blocked_states")
def monitor_blocked_states():
    """
    Background worker that scans for decisions in BLOCKED state for too long
    and emits alerts or triggers rollbacks.
    """
    db = SessionLocal()
    try:
        # Implementation would query repo for blocked states
        pass
    finally:
        db.close()


@celery_app.task(name="evaluate_checkpoints")
def evaluate_checkpoints():
    """
    Evaluates in-progress execution plans against their milestones.
    """
    db = SessionLocal()
    try:
        pass
    finally:
        db.close()
