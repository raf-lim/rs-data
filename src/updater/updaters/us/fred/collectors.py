import logging
from enum import Enum
import requests
from requests import HTTPError, RequestException
from updaters.us.interfaces import Frequency
from updaters.libs.helpers import PeriodDataLimits
from updaters.libs import exceptions
logging.basicConfig(level=logging.INFO)


def set_limit_of_readings(
        frequency: Frequency,
        period_limits: PeriodDataLimits,
        ) -> int:
    """
    Setting number of readings to be requested from API
    depending on metric's data frequency.
    """
    match frequency:
        case Frequency.DAILY:
            limit = int(period_limits.LIMIT_FRED_DAILY)
        case Frequency.WEEKLY:
            limit = int(period_limits.LIMIT_FRED_WEEKLY)
        case Frequency.MONTHLY:
            limit = int(period_limits.LIMIT_FRED_MONTHLY)
        case Frequency.QUARTERLY:
            limit = int(period_limits.LIMIT_FRED_QUARTERLY)

    return limit


JSON = dict[str, str | int | float | list[dict[str, str]]]


def get_constituent_url(
        code: str,
        limit: int,
        fred_base_url: str,
        api_key: str
        ) -> str:
    """Create endpoint URL fro FRED metric's constituent."""

    return (
        f"{fred_base_url}{code}&api_key={api_key}"
        f"&sort_order=desc&limit={limit}&file_type=json"
        )


def fetch_constituent_data(url: str) -> JSON:
    """
    Get US metric's constituent data form Fred API.
    """
    response = requests.get(url, timeout=None)
    try:
        response.raise_for_status()
    except HTTPError:
        raise RequestException
    
    return response.json()


def parse_constituent_data(raw_data: JSON) -> dict[str, float]:
    """Parse US metric's constituent data from json response."""
    if not "observations" in raw_data or len(raw_data["observations"]) == 0:
        raise exceptions.FredApiNoObservationsDataException(
            "No observations data in FRED API response."
            )
     
    return {
        i["date"]: float(i["value"]) for i in raw_data["observations"]
            if i["value"] != "."
            }
