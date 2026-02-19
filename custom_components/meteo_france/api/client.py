from aiohttp import ClientSession, ClientResponseError

from .auth_middleware import MeteoFranceApiAuthMiddleware
from .exception import MeteoFranceApiError
from .model import MeteoFranceApiVigilance


class MeteoFranceApiClient:
    """ Class to wrap access to Meteo France Vigilance product """
    BASE_URL: str = "https://public-api.meteofrance.fr/public/DPVigilance/v1"

    def __init__(self, session: ClientSession, api_key: str) -> None:
        """
        Initialize attributes.

        Args:
            application_id: The application ID used for identification.
        """
        self._session = session
        self._auth_middleware = MeteoFranceApiAuthMiddleware(api_key=api_key)

    async def authenticate(self) -> None:
        return await self._auth_middleware.authenticate(self._session)

    async def get_vigilance(self) -> MeteoFranceApiVigilance:
        """ Return vigilance data containing risk forecasts, including the chronology of events at national and departmental levels"""
        url = "https://public-api.meteofrance.fr/public/DPVigilance/v1/cartevigilance/encours"
        try:
            response = await self._session.get(url, middlewares=[self._auth_middleware])
            response.raise_for_status()
            return await response.json(loads=MeteoFranceApiVigilance.model_validate_json)
        except ClientResponseError as error:
            raise MeteoFranceApiError(status_code=error.status, message=error.message)