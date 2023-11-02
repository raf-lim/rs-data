from os import getenv
import datetime
import logging
import requests
from updaters.us.interfaces import Frequency
logging.basicConfig(level=logging.INFO)


FRED_BASE_URL = getenv("FRED_BASE_URL")
API_KEY = getenv("FRED_API_KEY")
START_DATE = getenv("FRED_START_DATE")
DAYS_BACK = getenv("NUMBER_OF_DAYS_DAILY_FREQ")
WEEKS_BACK= getenv("NUMBER_OF_WEEKS_WEEKLY_FREQ")


def set_fred_api_start_date(
        frequency: Frequency,
        start_date: str = START_DATE,
        days_back: str = DAYS_BACK,
        weeks_back: str = WEEKS_BACK,
) -> str:
    """
    Setting starting date for api endpoint
    depending on metric's data frequency.
    """
    if frequency == Frequency.DAILY:
        start_date = datetime.date.today() - datetime.timedelta(days=int(days_back))
        return datetime.datetime.strftime(start_date, format="%Y-%m-%d")
    elif frequency == Frequency.WEEKLY:
        start_date = datetime.date.today() - datetime.timedelta(weeks=int(weeks_back))
        return datetime.datetime.strftime(start_date, format="%Y-%m-%d")
    
    return start_date 


JSON = dict[str, str | int | float | list[dict[str | str]]]


def fetch_constituent_data(code: str, start_date: str) -> JSON:
    """
    Get US metric's constituent data form Fred API.
    """
    url = (
        f"{FRED_BASE_URL}{code}&api_key={API_KEY}"
        f"&observation_start={start_date}&file_type=json"
        )
    response = requests.get(url, timeout=None)
    response.raise_for_status()
    
    return response.json()


def parse_constituent_data(raw_data: JSON) -> dict[str, float]:
    """Parse US metric's constituent data from json response."""
    return {
        i["date"]: float(i["value"])
          for i in raw_data["observations"]
            if not i["value"] == "."
            }


# ConstituentDataGetterFn = Callable[[str, str], dict[str, float]]


# def get_together_constituents_data(
#         metric: Metric, start_date: str,
#         data_getter: ConstituentDataGetterFn) -> pd.DataFrame:
#     """Get all constituents data for a metric and convert into dataframe."""
#     metric_data: dict[str, dict[str, float]] = {}
#     for code, name in metric.constituents.items():
#         try:
#             data = data_getter(code, start_date)
#             name = name.replace(" ", "_").lower()
#             metric_data[name] = data
#         except Exception as e:
#             logging.warning(f"{name} failed {e}")
#             continue

#     return pd.DataFrame(metric_data).sort_index()
