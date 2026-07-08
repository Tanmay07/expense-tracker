import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from collaboration_platform.api.main import app
from collaboration_platform.infrastructure.database import get_db_session

@pytest.fixture
def mock_db_session():
    return AsyncMock()

@pytest.fixture
def client(mock_db_session):
    async def override_get_db_session():
        yield mock_db_session
        
    app.dependency_overrides[get_db_session] = override_get_db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
