from typing import Dict, Any
from .registry import ConnectorRegistryService
from ..domain.models import ConnectorStatus

class ConnectorManagerService:
    """
    Manages the lifecycle (installation, updates, uninstallation) of Connectors.
    """
    def __init__(self, registry: ConnectorRegistryService):
        self.registry = registry

    async def install_connector(self, connector_id: str, config: Dict[str, Any]) -> bool:
        """
        Installs and configures a connector.
        """
        connector = self.registry.get_connector(connector_id)
        if not connector:
            raise ValueError(f"Connector {connector_id} not found in registry.")

        is_valid = await connector.validate_configuration(config)
        if not is_valid:
            return False

        # In production, persist configuration securely via Authentication/Credential service
        
        # Mark as active (pseudo-code, metadata should be immutable or handled via DB)
        metadata = connector.get_metadata()
        metadata.status = ConnectorStatus.ACTIVE
        return True

    async def check_health_all(self) -> Dict[str, bool]:
        """
        Iterates through active connectors and triggers their health checks.
        """
        health_status = {}
        for metadata in self.registry.list_active_connectors():
            connector = self.registry.get_connector(metadata.connector_id)
            if connector:
                is_healthy = await connector.health_check()
                health_status[metadata.connector_id] = is_healthy
                
        return health_status
