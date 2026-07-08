import pytest
from typing import Dict, Any

from integration_platform.application.registry import ConnectorRegistryService
from integration_platform.application.manager import ConnectorManagerService
from integration_platform.application.auth import (
    AuthenticationService,
    MockAWSSecretsManager,
)
from integration_platform.application.sync import SynchronizationService
from integration_platform.application.normalization import NormalizationEngine
from integration_platform.infrastructure.event_bus import MockEventPublisher
from integration_platform.infrastructure.pfos_integration import (
    FeatureFlagClient,
    GovernanceClient,
    ObservabilityClient,
)
from integration_platform.sdk.connector_base import ConnectorBase, SyncContext


class MockPlaidConnector(ConnectorBase):
    @property
    def id(self) -> str:
        return "plaid_v1"

    @property
    def name(self) -> str:
        return "Mock Plaid Connector"

    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        return credentials.get("type") == "oauth2"

    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        return "client_id" in config

    async def discover_capabilities(self) -> list[str]:
        return ["transactions", "balances"]

    async def initial_sync(self, context: SyncContext) -> Dict[str, Any]:
        return {
            "raw_data": [
                {"transaction_id": "tx1", "amount": 100.50, "name": "Coffee Shop"},
                {"transaction_id": "tx2", "amount": 20.00, "name": "Bookstore"},
            ],
            "next_sync_token": "cursor_001",
        }

    async def incremental_sync(self, context: SyncContext) -> Dict[str, Any]:
        return {
            "raw_data": [
                {"transaction_id": "tx3", "amount": 15.00, "name": "Grocery Store"}
            ],
            "next_sync_token": "cursor_002",
        }

    async def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return raw_data

    async def health_check(self) -> bool:
        return True

    async def disconnect(self) -> bool:
        return True

    def get_metadata(self) -> Any:
        from integration_platform.domain.models import (
            ConnectorMetadata,
            ConnectorType,
            ConnectorStatus,
        )

        return ConnectorMetadata(
            connector_id=self.id,
            name=self.name,
            version="1.0.0",
            type=ConnectorType.BANK,
            provider="plaid",
            status=ConnectorStatus.ACTIVE,
            capabilities=["transactions", "balances"],
        )


@pytest.mark.asyncio
async def test_end_to_end_efcip_flow():
    # 1. Setup Platform Infrastructure
    registry = ConnectorRegistryService()
    registry.register(MockPlaidConnector())

    cred_manager = MockAWSSecretsManager()
    auth_service = AuthenticationService(cred_manager)

    manager = ConnectorManagerService(registry, FeatureFlagClient())
    sync_service = SynchronizationService(
        registry, auth_service, ObservabilityClient(), GovernanceClient()
    )

    normalizer = NormalizationEngine()
    event_publisher = MockEventPublisher()

    # 2. Simulate User connecting an account (OAuth Flow)
    connection_id = "conn_user1_plaid"
    user_id = "user_123"

    # Store credentials in Vault
    await auth_service.exchange_oauth_code(connection_id, "plaid_v1", "authcode_xxx")

    # Install the connector
    await manager.install_connector(user_id, "plaid_v1", {"client_id": "mock_client"})

    # 3. Trigger Initial Sync (via API or CRON)
    sync_result = await sync_service.trigger_sync(
        connection_id, "plaid_v1", user_id, sync_type="initial"
    )

    assert sync_result["status"] == "success"
    assert sync_result["records_fetched"] == 2
    assert sync_result["next_sync_token"] == "cursor_001"

    # Get raw data from the connector directly for normalizer
    # (In real flow, SyncService would pass this or it's fetched directly)
    # Simulating the pipeline:
    connector = registry.get_connector("plaid_v1")
    context = SyncContext(
        connection_id=connection_id,
        user_id=user_id,
        last_sync_token=None,
        parameters={},
    )
    raw_payload = (await connector.initial_sync(context))["raw_data"]

    # 4. Normalize Data
    canonical_txs = normalizer.normalize("plaid", raw_payload, connection_id, user_id)

    assert len(canonical_txs) == 2
    assert canonical_txs[0].amount == 100.50
    assert canonical_txs[0].description == "Coffee Shop"

    # 5. Publish to Event Bus
    published = await event_publisher.publish_transactions(canonical_txs)

    assert published is True
    assert len(event_publisher.published_events) == 2

    print("Integration flow tested successfully.")
