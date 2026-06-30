import pytest
from fastapi.testclient import TestClient
from platform_release.api.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
