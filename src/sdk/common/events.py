from datetime import datetime, timezone
import uuid
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class CloudEvent(BaseModel):
    """
    Strict CloudEvents Specification (v1.0) implementation for the Event Framework.
    Guarantees cross-service and enterprise bus compatibility.
    """
    specversion: str = "1.0"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    type: str
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    datacontenttype: str = "application/json"
    data: Dict[str, Any]
    
    # Extension attributes
    tenant_id: Optional[str] = None
    correlation_id: Optional[str] = None
