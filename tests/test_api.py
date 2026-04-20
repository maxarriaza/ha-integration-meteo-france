import pytest
from aioresponses import aioresponses
from aiohttp import ClientSession
from custom_components.meteo_france.api.client import MeteoFranceApiClient
from custom_components.meteo_france.api.exception import MeteoFranceApiAuthenticationError


@pytest.mark.asyncio
async def test_authenticate_with_valid_api_key(aiohttp_session: ClientSession):
    """ Test authenticate with valid api key """
    with aioresponses() as mock:
        mock.post("https://portail-api.meteofrance.fr/token", status=200, headers={"Content-Type": "application/json"}, payload={"access_token":"access_token","scope":"default","token_type":"Bearer","expires_in":3600})
        client = MeteoFranceApiClient(session=aiohttp_session, api_key="api_key")
        await client.authenticate()

@pytest.mark.asyncio
async def test_authenticate_with_invalid_api_key(aiohttp_session: ClientSession):
    """ Test authenticate with invalid api key """
    with aioresponses() as mock:
        with pytest.raises(MeteoFranceApiAuthenticationError):
            mock.post("https://portail-api.meteofrance.fr/token", status=200, headers={"Content-Type": "text/html"})
            client = MeteoFranceApiClient(session=aiohttp_session, api_key="api_key")
            await client.authenticate()

@pytest.mark.asyncio
async def test_vigilance_with_success(aiohttp_session: ClientSession):
    """ Test authenticate with invalid api key """
    with aioresponses() as mock:
        mock.post("https://portail-api.meteofrance.fr/token", status=200, headers={"Content-Type": "application/json"}, payload={"access_token": "access_token", "scope": "default", "token_type": "Bearer", "expires_in": 3600})
        mock.get("https://public-api.meteofrance.fr/public/DPVigilance/v1/cartevigilance/encours", status=200, headers={"Content-Type": "application/json"}, payload={})
        client = MeteoFranceApiClient(session=aiohttp_session, api_key="api_key")
        result = await client.get_vigilance()