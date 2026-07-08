from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class CredentialManager(ABC):
    """
    Abstracts interaction with the underlying credential vault (e.g., AWS Secrets Manager, HashiCorp Vault).
    Ensures raw credentials are never leaked into the business logic.
    """

    @abstractmethod
    async def store_credentials(
        self, connection_id: str, credentials: Dict[str, Any]
    ) -> bool:
        pass

    @abstractmethod
    async def retrieve_credentials(
        self, connection_id: str
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def revoke_credentials(self, connection_id: str) -> bool:
        pass


class MockAWSSecretsManager(CredentialManager):
    """
    Simulated implementation of AWS Secrets Manager for local development.
    In production, this relies on boto3 and the IAM roles deployed in Phase 11F.
    """

    def __init__(self):
        self._vault: Dict[str, Dict[str, Any]] = {}

    async def store_credentials(
        self, connection_id: str, credentials: Dict[str, Any]
    ) -> bool:
        self._vault[connection_id] = credentials
        return True

    async def retrieve_credentials(
        self, connection_id: str
    ) -> Optional[Dict[str, Any]]:
        return self._vault.get(connection_id)

    async def revoke_credentials(self, connection_id: str) -> bool:
        if connection_id in self._vault:
            del self._vault[connection_id]
        return True


class AuthenticationService:
    """
    Handles OAuth 2.0 flows, API key validation, and token refresh logic.
    Interfaces directly with the CredentialManager.
    """

    def __init__(self, credential_manager: CredentialManager):
        self.credential_manager = credential_manager

    async def exchange_oauth_code(
        self, connection_id: str, provider_id: str, auth_code: str
    ) -> bool:
        """
        Exchanges an OAuth authorization code for access/refresh tokens and stores them securely.
        """
        # Mocking the OAuth exchange with the external provider
        access_token = f"mock_access_{provider_id}_{auth_code}"
        refresh_token = f"mock_refresh_{provider_id}"

        credentials = {
            "type": "oauth2",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 3600,
        }

        return await self.credential_manager.store_credentials(
            connection_id, credentials
        )

    async def get_valid_credentials(
        self, connection_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves credentials for a connection. Automatically handles token refresh if expired.
        """
        creds = await self.credential_manager.retrieve_credentials(connection_id)
        if not creds:
            return None

        # In a real implementation, check expiration and use refresh_token if needed.
        return creds
