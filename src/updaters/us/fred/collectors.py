import os
from typing import Callable
import logging
import requests
import pandas as pd
from updaters.us.interfaces import Metric
logging.basicConfig(level=logging.INFO)

FRED_BASE_URL = os.getenv("FRED_BASE_URL")
API_KEY = os.getenv("FRED_API_KEY")
START_DATE = os.getenv("FRED_START_DATE")


def get_constituent_data(code: str) -> dict[str, float]:
    """
    Get US metric's constituent data form Fred API.
    """
    url = (
        f"{FRED_BASE_URL}{code}&api_key={API_KEY}"
        f"&observation_start={START_DATE}&file_type=json"
    )
    response = requests.get(url, timeout=None)
    data = response.json()

    return {
        i["date"]: float(i["value"])
          for i in data["observations"]
            if not i["value"] == "."
    }


ConstituentDataGetterFn = Callable[[str], dict[str, float]]


def get_together_constituents_data(
        metric: Metric,
        data_getter: ConstituentDataGetterFn
    ) -> pd.DataFrame:
    """Get all constituents data for a metric and convert into dataframe."""
    metric_data: dict[str, dict[str, float]] = {}
    for code, name in metric.constituents.items():
        try:
            data = data_getter(code)
            name = name.replace(" ", "_").lower()
            metric_data[name] = data
        except Exception as e:
            logging.warning(f"{name} failed {e}")
            continue

    return pd.DataFrame(metric_data).sort_index()
