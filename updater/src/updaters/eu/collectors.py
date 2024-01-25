import os
import logging
from typing import Any
import requests
from requests.exceptions import HTTPError, RequestException
import pandas as pd

logging.basicConfig(level=logging.INFO)


def compile_endpoint_url(
        base_url: str, country_code: str, metric_code: str,
        ) -> str:
    """Compile endpoint url to get metric data for a country."""
    
    return f"{base_url}?geo={country_code}&indic={metric_code}&s_adj=SA"


def fetch_data(url: str) -> pd.DataFrame:
    """Get Eurostat data for a metric of a country."""
    response = requests.get(url, timeout=None)
    try:
        response.raise_for_status()
    except HTTPError:
        raise RequestException

    return response.json()


JSON = dict[str, str | dict[str | Any]]


def parse_country_metric_data(raw_data: JSON):
    """Parse data received from Eurostat API."""
    readings = raw_data["value"]
    dates = raw_data["dimension"]["time"]["category"]["index"]
    
    for date, idx in dates.items():
        dates.update({date: readings[str(idx)]})

    data = pd.DataFrame({"date": dates.keys(), "value": dates.values()})
    data = data.sort_index().set_index("date")

    return data 
    