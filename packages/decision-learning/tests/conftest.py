import pytest
from fastapi.testclient import TestClient
from decision_learning.api.main import app
from decision_learning.api.dependencies import get_db

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

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
