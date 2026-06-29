import pytest
from src.main import app
from src.presentation.api import get_current_user_id

@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user_id] = lambda: "mock_user_123"
    yield
    app.dependency_overrides.clear()
