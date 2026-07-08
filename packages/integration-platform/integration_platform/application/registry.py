from typing import Dict, List, Optional
from ..domain.models import ConnectorMetadata
from ..sdk.connector_base import ConnectorBase

class ConnectorRegistryService:
    """
    Central registry for discovering and loading installed Connectors.
    """
    def __init__(self):
        self._connectors: Dict[str, ConnectorBase] = {}

    def register(self, connector: ConnectorBase):
        metadata = connector.get_metadata()
        self._connectors[metadata.connector_id] = connector

    def get_connector(self, connector_id: str) -> Optional[ConnectorBase]:
        return self._connectors.get(connector_id)

    def list_connectors(self) -> List[ConnectorMetadata]:
        return [c.get_metadata() for c in self._connectors.values()]

    def list_active_connectors(self) -> List[ConnectorMetadata]:
        return [c.get_metadata() for c in self._connectors.values() if c.get_metadata().status.value == "ACTIVE"]
