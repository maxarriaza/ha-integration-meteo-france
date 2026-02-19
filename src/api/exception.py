class MeteoFranceApiError(Exception):
    """Base exception for Meteo France API errors."""

    def __init__(self, message: str, status_code: int) -> None:
        """Initialize with optional context.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
        """
        super().__init__(message)
        self._message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return f"MeteoFranceApiError: status_code={self.status_code}, message={self._message}"

    def __repr__(self) -> str:
        return f"MeteoFranceApiError: status_code={self.status_code}, message={self._message}"