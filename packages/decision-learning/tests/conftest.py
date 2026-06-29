import pytest
from fastapi.testclient import TestClient
from decision_learning.api.main import app
from decision_learning.infrastructure.database import Base, engine, SessionLocal
from decision_learning.api.dependencies import get_db

@pytest.fixture(scope="session")
def db_engine():
    # In a real app we might use an in-memory SQLite or a dedicated test DB.
    # For now, we'll create tables in the existing DB for testing.
    # Base.metadata.create_all(bind=engine)
    yield engine
    # Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
