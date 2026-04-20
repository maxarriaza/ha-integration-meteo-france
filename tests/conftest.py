import pytest
from aiohttp import ClientSession


@pytest.fixture()
async def aiohttp_session():
    async with ClientSession() as session:
        yield session