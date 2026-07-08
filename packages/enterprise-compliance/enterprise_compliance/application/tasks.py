from celery import Celery
import os
import time

redis_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("enterprise_compliance", broker=redis_url, backend=redis_url)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task
def evaluate_portfolio_compliance(portfolio_id: str):
    # This task would typically run periodically or on event
    time.sleep(2)  # Mock computation
    print(f"Compliance checked for portfolio {portfolio_id}")
    return {"status": "success", "portfolio_id": portfolio_id}


@celery_app.task
def update_user_risk_profile(user_id: str, new_events: list):
    time.sleep(1)
    print(f"Risk profile updated for user {user_id}")
    return {"status": "success", "user_id": user_id}
