from aiohttp import ClientSession, ClientResponseError

from .auth_middleware import MeteoFranceApiAuthMiddleware
from .exception import MeteoFranceApiError
from .model import MeteoFranceApiVigilance, MeteoFranceApiToken


class MeteoFranceApiClient:
    """ Class to wrap access to Meteo France Vigilance product """
    VIGILANCE_URL: str = "https://public-api.meteofrance.fr/public/DPVigilance/v1/cartevigilance/encours"

    def __init__(self, session: ClientSession, api_key: str) -> None:
        """
        Initialize attributes.

        Args:
            application_id: The application ID used for identification.
        """
        self._session = session
        self._auth_middleware = MeteoFranceApiAuthMiddleware(api_key=api_key)

    async def authenticate(self) -> None:
        return await self._auth_middleware.authenticate(session=self._session)

    async def get_vigilance(self) -> MeteoFranceApiVigilance:
        """ Return vigilance data containing risk forecasts, including the chronology of events at national and departmental levels"""
        try:
            async with self._session.get(url=MeteoFranceApiClient.VIGILANCE_URL, middlewares=[self._auth_middleware]) as response:
                response.raise_for_status()
                payload = await response.json()
                result = MeteoFranceApiVigilance.model_validate(payload)
                return result

        except ClientResponseError as error:
            raise MeteoFranceApiError(message="Unknown error", api_code=error.status, api_message=error.message)

