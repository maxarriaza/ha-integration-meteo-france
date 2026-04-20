from aiohttp import ClientRequest, ClientResponse, ClientHandlerType, ClientResponseError, ClientSession

from .exception import MeteoFranceApiAuthenticationError
from .model import MeteoFranceApiToken


class MeteoFranceApiAuthMiddleware:
    """ Class to handle authentication to Meteo France API """
    _TOKEN_URL: str = "https://portail-api.meteofrance.fr/token"

    def __init__(self, api_key: str):
        """ Initialize authentication middleware """
        self._api_key: str = api_key
        self._access_token: str | None = None

    async def authenticate(self, session: ClientSession) -> None:
        headers = {"Authorization": f"Basic {self._api_key}"}
        data = {"grant_type": "client_credentials"}
        try:
            async with session.post(url=MeteoFranceApiAuthMiddleware._TOKEN_URL, headers=headers, data=data) as response:
                response.raise_for_status()
                payload = await response.json()
                result = MeteoFranceApiToken.model_validate(payload)
                self._access_token = result.access_token
                return None

        except ClientResponseError as error:
            raise MeteoFranceApiAuthenticationError(api_code=error.status, api_message=error.message)

    async def __call__(self, request: ClientRequest, handler: ClientHandlerType) -> ClientResponse:
        """ Middleware handler function"""
        if self._access_token is None:
            await self.authenticate(request.session)

        request.headers.add("Authorization", f"Bearer {self._access_token}")
        return await handler(request)
