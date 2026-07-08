from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel
from ..domain.models import ConnectorMetadata

class SyncContext(BaseModel):
    connection_id: str
    user_id: str
    last_sync_token: str | None = None
    parameters: Dict[str, Any] = {}

class ConnectorBase(ABC):
    """
    The abstract base class that every EFCIP Connector must implement.
    Ensures a standardized lifecycle across all integrations.
    """
    
    @abstractmethod
    def get_metadata(self) -> ConnectorMetadata:
        """Returns the static metadata defining this connector."""
        pass

    @abstractmethod
    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Validates credentials (API keys, OAuth tokens) with the provider."""
        pass

    @abstractmethod
    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """Validates user-provided configuration."""
        pass

    @abstractmethod
    async def discover_capabilities(self, connection_id: str) -> List[str]:
        """Discovers what data is actually available for this specific connection."""
        pass

    @abstractmethod
    async def initial_sync(self, context: SyncContext) -> Dict[str, Any]:
        """Performs the first, historical sync of data."""
        pass

    @abstractmethod
    async def incremental_sync(self, context: SyncContext) -> Dict[str, Any]:
        """Performs a delta sync based on the last_sync_token."""
        pass

    @abstractmethod
    async def normalize_data(self, raw_data: Any, schema_type: str) -> BaseModel:
        """Converts provider-specific schemas into canonical PFOS domain models."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Validates connectivity to the provider's API."""
        pass

    @abstractmethod
    async def disconnect(self, connection_id: str) -> bool:
        """Cleans up webhooks and revokes tokens."""
        pass
