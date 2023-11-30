class NoTableFoundException(Exception):
    """Raised if no requested table found in database"""


class NoEuMetricTableFoundException(Exception):
    """Raised if no metrics's table found in database"""


class NoEuCountryTableFoundException(Exception):
    """Raised if no country's table found in database"""