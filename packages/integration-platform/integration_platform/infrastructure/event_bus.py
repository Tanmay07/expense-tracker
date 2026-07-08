import json
import logging
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from ..application.normalization import CanonicalTransaction

logger = logging.getLogger(__name__)

class EventPublisher(ABC):
    """
    Abstracts the event bus publishing mechanism.
     Ensures integration platform is decoupled from the specific streaming technology (Kafka/Redis).
    """
    @abstractmethod
    async def publish_transactions(self, transactions: List[CanonicalTransaction]) -> bool:
        pass


class RedisEventPublisher(EventPublisher):
    """
    Implementation of EventPublisher using Redis Pub/Sub or Streams.
    Used for local development and lightweight deployments.
    """
    def __init__(self, redis_client):
        self.redis = redis_client
        self.stream_name = "events:financial:transactions"

    async def publish_transactions(self, transactions: List[CanonicalTransaction]) -> bool:
        try:
            for tx in transactions:
                payload = tx.model_dump_json()
                # Assuming aioredis or redis-py async interface
                await self.redis.xadd(self.stream_name, {"payload": payload})
            
            logger.info(f"Published {len(transactions)} transactions to {self.stream_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish transactions to Redis: {e}")
            return False


class MockEventPublisher(EventPublisher):
    """
    Mock publisher for testing without requiring a running Redis/Kafka instance.
    """
    def __init__(self):
        self.published_events = []

    async def publish_transactions(self, transactions: List[CanonicalTransaction]) -> bool:
        self.published_events.extend(transactions)
        logger.info(f"MOCK: Published {len(transactions)} transactions.")
        return True
