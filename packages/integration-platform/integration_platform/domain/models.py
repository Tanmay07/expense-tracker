from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum

class ConnectorStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DEGRADED = "DEGRADED"
    ERROR = "ERROR"

class ConnectorType(str, Enum):
    BANK = "BANK"
    BROKERAGE = "BROKERAGE"
    CREDIT_CARD = "CREDIT_CARD"
    TAX = "TAX"
    PAYROLL = "PAYROLL"
    HRIS = "HRIS"
    EMAIL = "EMAIL"
    CALENDAR = "CALENDAR"
    STORAGE = "STORAGE"
    CUSTOM = "CUSTOM"

class ConnectorMetadata(BaseModel):
    connector_id: str = Field(..., description="Unique ID for the connector (e.g., plaid, stripe)")
    name: str = Field(..., description="Human readable name")
    version: str = Field(..., description="Version of the connector implementation")
    provider: str = Field(..., description="The underlying provider")
    type: ConnectorType = Field(..., description="The category of the connector")
    capabilities: List[str] = Field(..., description="List of supported capabilities (e.g., transactions, balances)")
    status: ConnectorStatus = Field(default=ConnectorStatus.INACTIVE)
    features_flags: List[str] = Field(default_factory=list)
    permissions_required: List[str] = Field(default_factory=list)
