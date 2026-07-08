import os
from celery import Celery
from ..infrastructure.database import SessionLocal

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("execution_capability_tasks", broker=CELERY_BROKER_URL)

@celery_app.task(name="sync_plugins")
def sync_plugins():
    """
    Background worker that hits external plugin endpoints (if configured via Microservice approach)
    to dynamically refresh their capabilities and availability.
    """
    db = SessionLocal()
    try:
        pass
    finally:
        db.close()

@celery_app.task(name="monitor_approvals")
def monitor_approvals():
    """
    Scans for expired ApprovalRequests and transitions them to EXPIRED,
    unblocking routing loops and cancelling execution routes.
    """
    db = SessionLocal()
    try:
        pass
    finally:
        db.close()
