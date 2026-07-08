from typing import Dict, Any, List
import uuid
import time

class TimelineService:
    def __init__(self):
        # User ID -> List of immutable events
        self.events_store: Dict[str, List[Dict[str, Any]]] = {}
        
    def publish_event(self, user_id: str, event_type: str, payload: Dict[str, Any], timestamp: float = None):
        if user_id not in self.events_store:
            self.events_store[user_id] = []
            
        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": timestamp or time.time(),
            "type": event_type,
            "payload": payload
        }
        self.events_store[user_id].append(event)
        # Sort by timestamp to ensure strict chronological order
        self.events_store[user_id].sort(key=lambda x: x["timestamp"])
        return event

    def get_events(self, user_id: str, up_to_timestamp: float = None) -> List[Dict[str, Any]]:
        events = self.events_store.get(user_id, [])
        if up_to_timestamp:
            return [e for e in events if e["timestamp"] <= up_to_timestamp]
        return events


class ReplayService:
    def __init__(self, timeline_svc: TimelineService):
        self.timeline_svc = timeline_svc
        
    def reconstruct_net_worth(self, user_id: str, target_timestamp: float) -> float:
        """
        Time-Travel query to reconstruct exactly what the net worth was at a specific microsecond in history.
        """
        events = self.timeline_svc.get_events(user_id, up_to_timestamp=target_timestamp)
        
        net_worth = 0.0
        for event in events:
            if event["type"] == "LEDGER_CREDIT":
                net_worth += event["payload"].get("amount", 0.0)
            elif event["type"] == "LEDGER_DEBIT":
                net_worth -= event["payload"].get("amount", 0.0)
            elif event["type"] == "ASSET_APPRECIATION":
                net_worth += event["payload"].get("amount", 0.0)
                
        return net_worth
