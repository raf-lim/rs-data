class NoTableFoundException(Exception):
    """Raised if no requested table found in database"""


class NoEuMetricTableFound(Exception):
    """Raised if no metrics's table found in database"""


class NoEuCountryTableFound(Exception):
    """Raised if no country's table found in database"""