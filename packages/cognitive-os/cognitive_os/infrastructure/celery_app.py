import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "cognitive_os",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["cognitive_os.infrastructure.workers"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "cognitive_os.infrastructure.workers.execute_mission": {"queue": "planning"},
        "cognitive_os.infrastructure.workers.reflect_on_mission": {"queue": "reflection"}
    }
)
