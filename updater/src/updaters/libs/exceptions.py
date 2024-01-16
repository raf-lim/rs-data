class MissingFredBaseUrlException(Exception):
    """Raised when FRED BASE URL is not set"""


class MissingFredApiKeyException(Exception):
    """Raised when FRED API key is not set"""


class FredApiNoObservationsDataException(Exception):
    """Raised when FRED API sends invalid data"""


class FredMetricPluginNotFoundException(Exception):
    """Raise when FRED metric plugin file not found in folder"""


class FredMetricsPluginsFolderEmpty(Exception):
    """Raised when no FRED metric plugin in folder"""


class NoTableFoundException(Exception):
    """Raised when table not found in database"""