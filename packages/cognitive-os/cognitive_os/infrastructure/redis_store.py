from typing import Dict, Any, Optional

class TransientStateStore:
    """
    Redis abstraction for transient cognition state.
    Used for in-flight mission planning, consensus voting, distributed locks,
    temporary reasoning artifacts, retry metadata, etc.
    All data is treated as disposable with TTLs.
    """
    def __init__(self):
        # Stub for Redis client
        self._store: Dict[str, Dict[str, Any]] = {}

    def save_in_flight_state(self, key: str, state: Dict[str, Any], ttl_seconds: int = 3600):
        """Saves transient state with a TTL."""
        self._store[key] = {
            "data": state,
            "ttl": ttl_seconds # In real implementation, pass TTL to redis SETEX
        }

    def get_in_flight_state(self, key: str) -> Optional[Dict[str, Any]]:
        record = self._store.get(key)
        return record["data"] if record else None

    def delete_state(self, key: str):
        if key in self._store:
            del self._store[key]
