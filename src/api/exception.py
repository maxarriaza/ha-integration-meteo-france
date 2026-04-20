class MeteoFranceApiError(Exception):
    """Base exception for Meteo France API errors."""

    def __init__(self, message: str, api_code: int, api_message: str) -> None:
        """Initialize with optional context.

        Args:
            message: Error message
        """
        super().__init__(message)
        self._message = message
        self._api_code = api_code
        self._api_message = api_message

    def __str__(self) -> str:
        return f"MeteoFranceApiError: {self._message}"

class MeteoFranceApiAuthenticationError(MeteoFranceApiError):
    """ Exception for Meteo France API authentication error """
    def __init__(self, api_code: int, api_message: str) -> None:
        super().__init__("Invalid api key", api_code, api_message)

class MeteoFranceApiInvalidCredentialError(MeteoFranceApiError):
    """ Exception for Meteo France API credential error """
    def __init__(self, api_code: int, api_message: str) -> None:
        super().__init__("Invalid credentials", api_code, api_message)
