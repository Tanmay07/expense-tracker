from typing import Dict, Any
from ..application.registry import ConnectorRegistryService
from ..application.auth import AuthenticationService
from ..sdk.connector_base import SyncContext

class SynchronizationService:
    """
    Stateful engine responsible for executing the synchronization lifecycle 
    for connected external providers.
    """
    def __init__(self, registry: ConnectorRegistryService, auth_service: AuthenticationService):
        self.registry = registry
        self.auth_service = auth_service
        # In production, uses a durable store for last_sync_tokens and sync history

    async def trigger_sync(self, connection_id: str, connector_id: str, user_id: str, sync_type: str = "incremental") -> Dict[str, Any]:
        """
        Executes a sync task. Resolves credentials, loads the connector, and triggers the sync.
        """
        connector = self.registry.get_connector(connector_id)
        if not connector:
            raise ValueError(f"Connector {connector_id} not found in registry.")

        # 1. Retrieve credentials securely
        credentials = await self.auth_service.get_valid_credentials(connection_id)
        if not credentials:
            raise PermissionError(f"No valid credentials found for connection {connection_id}")

        # 2. Authenticate the connector instance (injecting credentials)
        auth_success = await connector.authenticate(credentials)
        if not auth_success:
            raise PermissionError("Connector authentication failed with external provider.")

        # 3. Prepare sync context
        # In production, we'd look up the last_sync_token from PostgreSQL for this connection
        last_sync_token = "mock_cursor_001" if sync_type == "incremental" else None
        
        context = SyncContext(
            connection_id=connection_id,
            user_id=user_id,
            last_sync_token=last_sync_token,
            parameters={}
        )

        # 4. Execute Sync
        try:
            if sync_type == "initial":
                sync_result = await connector.initial_sync(context)
            else:
                sync_result = await connector.incremental_sync(context)
                
            # 5. Checkpoint the new sync token securely
            # In production, save sync_result.get("next_sync_token") to PostgreSQL
            
            return {
                "status": "success",
                "sync_type": sync_type,
                "records_fetched": len(sync_result.get("raw_data", [])),
                "next_sync_token": sync_result.get("next_sync_token")
            }
        except Exception as e:
            # Implement retry mechanisms or DLQ here
            return {
                "status": "failed",
                "error": str(e)
            }
