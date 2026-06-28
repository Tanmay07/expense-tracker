from celery import Celery
import os
import time

redis_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "ai_copilot",
    broker=redis_url,
    backend=redis_url
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def analyze_behavior(user_id: str):
    # Simulates analyzing recent transactions and updating behavioral profile
    time.sleep(2)
    print(f"Analyzed behavior for {user_id}")
    return {"status": "success"}

@celery_app.task
def evaluate_goal_monitor():
    # Simulates checking all active goals for drift
    time.sleep(3)
    print("Evaluated goal health across users")
    return {"status": "success"}

@celery_app.task
def run_digital_twin_simulation(request_id: str):
    # Simulates a deep digital twin "what-if" scenario
    time.sleep(5)
    print(f"Completed simulation {request_id}")
    return {"status": "success"}
