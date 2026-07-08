from typing import Dict, Any
import logging
from ..application.registry import ConnectorRegistryService
from ..domain.models import ConnectorStatus
from ..infrastructure.pfos_integration import FeatureFlagClient

logger = logging.getLogger(__name__)


class ConnectorManagerService:
    """
    Manages the installation, validation, and lifecycle of connectors for users.
    """

    def __init__(
        self, registry: ConnectorRegistryService, ff_client: FeatureFlagClient = None
    ):
        self.registry = registry
        self.ff_client = ff_client or FeatureFlagClient()
        # In production, uses a database to track installed connections per user

    async def install_connector(
        self, user_id: str, connector_id: str, config: Dict[str, Any]
    ) -> str:
        """
        Installs a new connection for a user.
        """
        connector = self.registry.get_connector(connector_id)
        if not connector:
            raise ValueError(f"Connector {connector_id} not found in registry")

        # PFOS Feature Flag Check
        if not self.ff_client.is_enabled(
            f"integration.connector.{connector_id}.enabled", {"user_id": user_id}
        ):
            raise PermissionError(
                f"Connector {connector_id} is currently disabled by feature flag."
            )

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
