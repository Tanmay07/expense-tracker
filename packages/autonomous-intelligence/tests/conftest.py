import pytest
import pytest_asyncio
import httpx
from httpx import AsyncClient
from autonomous_intelligence.presentation.api import app

@pytest_asyncio.fixture
async def async_client():
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
