class MissingFredBaseUrlException(Exception):
    """Raised when FRED BASE URL is not set"""


class MissingFredApiKeyException(Exception):
    """Raised when FRED API key is not set"""


class FredApiNoObservationsDataException(Exception):
    """Raised when FRED API sends invalid data"""


class NoTableFoundException(Exception):
    """Raised when table not found in database"""