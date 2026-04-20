from aiohttp import ClientRequest, ClientResponse, ClientHandlerType, ClientResponseError, ClientSession

from .exception import MeteoFranceApiError
from .model import MeteoFranceApiToken


class MeteoFranceApiAuthMiddleware:
    """ Class to handle authentication to Meteo France API """
    _AUTH_URL: str = "https://portail-api.meteofrance.fr/token"

    def __init__(self, api_key: str):
        """ Initialize authentication middleware """
        self._api_key: str = api_key
        self._access_token: str | None = None

    async def authenticate(self, session: ClientSession) -> None:
        headers = {"Authorization": f"Basic {self._api_key}"}
        data = {"grant_type": "client_credentials"}
        try:
            response = await session.post(url=MeteoFranceApiAuthMiddleware._AUTH_URL, data=data, headers=headers)
            response.raise_for_status()
            result: MeteoFranceApiToken = await response.json(loads=MeteoFranceApiToken.model_validate_json)
            self._access_token = result.access_token
        except ClientResponseError as error:
            raise MeteoFranceApiError(status_code=error.status, message=error.message)

    async def __call__(self, request: ClientRequest, handler: ClientHandlerType) -> ClientResponse:
        """ Middleware handler function"""
        if self._access_token is None:
            await self.authenticate(request.session)

        request.headers.add("Authorization", f"Bearer {self._access_token}")
        return await handler(request)