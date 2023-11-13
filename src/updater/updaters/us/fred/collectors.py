from os import getenv
import logging
import requests
from updaters.us.interfaces import Frequency
from updaters.us import exceptions
logging.basicConfig(level=logging.INFO)


FRED_BASE_URL = getenv("FRED_BASE_URL")
API_KEY = getenv("FRED_API_KEY")
LIMIT_FRED_DAILY = getenv("LIMIT_FRED_DAILY")
LIMIT_FRED_WEEKLY=getenv("LIMIT_FRED_WEEKLY")
LIMIT_FRED_MONTHLY=getenv("LIMIT_FRED_MONTHLY")
LIMIT_FRED_QUARTERLY=getenv("LIMIT_FRED_QUARTERLY")


def set_limit_of_readings(frequency: Frequency) -> int:
    """
    Setting number of readings to be requested from API
    depending on metric's data frequency.
    """
    match frequency:
        case Frequency.DAILY:
            limit = int(LIMIT_FRED_DAILY)
        case Frequency.WEEKLY:
            limit = int(LIMIT_FRED_WEEKLY)
        case Frequency.MONTHLY:
            limit = int(LIMIT_FRED_MONTHLY)
        case Frequency.QUARTERLY:
            limit = int(LIMIT_FRED_QUARTERLY)

    return limit


JSON = dict[str, str | int | float | list[dict[str | str]]]


def fetch_constituent_data(code: str, limit: int) -> JSON:
    """
    Get US metric's constituent data form Fred API.
    """
    url = (
        f"{FRED_BASE_URL}{code}&api_key={API_KEY}"
        f"&sort_order=desc&limit={limit}&file_type=json"
        )
    response = requests.get(url, timeout=None)
    response.raise_for_status()
    
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
