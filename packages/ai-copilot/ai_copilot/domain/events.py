from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
import uuid


class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None
    event_type: str
    payload: Dict[str, Any]


class CopilotModeChanged(DomainEvent):
    event_type: str = "CopilotModeChanged"


class GoalConversationCreated(DomainEvent):
    event_type: str = "GoalConversationCreated"


class ActionPlanCreated(DomainEvent):
    event_type: str = "ActionPlanCreated"


class ActionPlanApproved(DomainEvent):
    event_type: str = "ActionPlanApproved"


class BehaviorUpdated(DomainEvent):
    event_type: str = "BehaviorUpdated"


class MonitoringAlertGenerated(DomainEvent):
    event_type: str = "MonitoringAlertGenerated"


class SimulationRequested(DomainEvent):
    event_type: str = "SimulationRequested"
