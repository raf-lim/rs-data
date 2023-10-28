from typing import Protocol, Optional
import pandas as pd
import numpy as np
from statistics import mean

from updaters.us.interfaces import Frequency


class Metric(Protocol):
    frequency: Optional[str]


def set_full_year_readings_number(frequency: Frequency) -> int:
    """
    Set number of readings for the full year depending on
    readings frequency.
    """
    match frequency:
        case Frequency.QUARTERLY:
            interval = 4
        case Frequency.MONTHLY:
            interval = 12
        case Frequency.WEEKLY:
            interval = 52
        case Frequency.DAILY:
            interval = 252
    
    return interval


def compute_period_to_period_change(
        metric: Metric,
        frequency: Frequency,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
    """Create dataframe with period to period changes."""

    match metric.frequency:
        case frequency.WEEKLY:
            y_interval = 52
            m_interval = 4
            t_suffix = 'mtm'
        case frequency.MONTHLY:
            y_interval = 12
            t_suffix = 'mtm'
        case frequency.QUARTERLY:
            y_interval = 4
            t_suffix = 'qtq'

    constituents_data: list[pd.DataFrame] = []
    for col in data.columns:
        col_t = f'{col} {t_suffix}'
        col_y = f'{col} yoy'

        if metric.frequency == frequency.WEEKLY:
            data[col_t] = data[col].pct_change(periods=m_interval)
        else:
            data[col_t] = data[col].pct_change()
        data[col_y] = data[col].pct_change(periods=y_interval)

        constituents_data.append(data[[col_t, col_y]])

    return pd.concat(constituents_data, axis=1).sort_index()