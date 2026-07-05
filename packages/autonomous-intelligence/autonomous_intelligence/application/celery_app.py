import os
from celery import Celery

celery_app = Celery(
    "autonomous_intelligence",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    include=["autonomous_intelligence.application.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "autonomous_intelligence.application.tasks.*": {"queue": "autonomous_intelligence"}
    }
)
