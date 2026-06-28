from celery import Celery
import os
import time

redis_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "ai_financial_coach",
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
def summarize_conversation(conversation_id: str):
    time.sleep(2)
    print(f"Summarized conversation {conversation_id}")
    return {"status": "success", "conversation_id": conversation_id}

@celery_app.task
def generate_embeddings(text: str):
    time.sleep(1)
    print(f"Generated embeddings for text")
    return {"status": "success"}
