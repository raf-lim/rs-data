import os
import logging
import requests
import pandas as pd
from apps.updater.us.interfaces import Metric

logging.basicConfig(level=logging.INFO)

FRED_BASE_URL = os.getenv("FRED_BASE_URL")
API_KEY = os.getenv("FRED_API_KEY")
START_DATE = os.getenv("FRED_START_DATE")


def get_constituent_url(code: str) -> str:
    """
    Get end point url of metric's constituent.
    """
    return (
        f'{FRED_BASE_URL}{code}&api_key={API_KEY}'
        f'&observation_start={START_DATE}&file_type=json'
    )


def get_constituent_data(code: str) -> dict[str, float]:
    """
    Get Us metric's constituent data form Fred API.
    """
    url = get_constituent_url(code)
    response = requests.get(url, timeout=None)
    data = response.json()
    
    return {i["date"]: i["value"] for i in data["observations"]}


def get_and_metric_data(metric: Metric) -> pd.DataFrame:
    metric_data: dict[str, dict[str, float]] = {}
    for code, name in metric.constituents.items():
        try:
            metric_data[name] = get_constituent_data(code)
            return pd.DataFrame(metric_data).sort_index()
        except Exception as e:
            logging.warning(f"{name} failed {e}")
