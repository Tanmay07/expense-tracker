import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_agent(async_client: AsyncClient):
    # This is a basic test. In reality we need to mock DB dependency
    pass

@pytest.mark.asyncio
async def test_list_agents(async_client: AsyncClient):
    pass
