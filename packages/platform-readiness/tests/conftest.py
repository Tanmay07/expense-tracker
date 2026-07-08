import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import MagicMock


@pytest.fixture(scope="session")
def db_engine():
    yield MagicMock()


@pytest.fixture(scope="function")
def db_session(db_engine):
    session_mock = MagicMock()
    yield session_mock


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    from platform_readiness.api.main import app
    from platform_readiness.api.dependencies import get_db

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
