import os
import logging
from typing import Any
import requests
import pandas as pd


logging.basicConfig(level=logging.INFO)


def compile_endpoint_url(
        base_url: str, country_code: str, metric_code: str,
        ) -> str:
    """Compile endpoint url to get metric data for a country."""
    
    return os.path.join(
            base_url, f"?geo={country_code}&indic={metric_code}&s_adj=SA",
            )


def get_data(url: str) -> pd.DataFrame:
    """Get Eurostat data for a metric of a country."""
    response = requests.get(url, timeout=None)
    response.raise_for_status()

    return response.json()


JSON = dict[str, str | dict[str | Any]]


def parse_country_metric_data(data: JSON):
    """Parse data received from Eurostat API."""
    dates = pd.Series(
        data['dimension']['time']['category']['index'],
        dtype='object',
        )
    dates.index.name = 'date'
    dates = dates.to_frame().reset_index().drop(columns=[0])

    values = pd.Series(data['value'], dtype=float)
    values.index = values.index.astype(int)
    values = values.to_frame()
    
    return dates.join(values).set_index('date').sort_index()
    