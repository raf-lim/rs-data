from typing import Protocol, Optional
import pandas as pd
import numpy as np
from statistics import mean

from updaters.us.interfaces import Frequency


class Metric(Protocol):
    frequency: Optional[str]


def compute_stats_difference(
        metric: Metric,
        input_data: pd.DataFrame,
    ) -> pd.DataFrame:
    """Compute statistics as difference between current and previous"""

    statistics: dict[str, list[float, float, float, str]] = {}
    for col in input_data.columns:
        # finding last not NaN value
        country_values = list(input_data[col].values)
        country_values.reverse()
        for n, value in enumerate(country_values):
            if not pd.isna(value):
                break
        # last_col_idx = n
        last = country_values[n]

        last_year_interval = 12
        if hasattr(metric, 'frequency') and metric.frequency.value == 'q':
            last_year_interval = 4

        not_nan_values = [value for value in country_values if not pd.isna(value)]
        average_3m = mean(not_nan_values[:3])
        average_6m = mean(not_nan_values[:6])
        average_12m = mean(not_nan_values[:12])

        if len(not_nan_values) > 1:
            last_vs_previous = last - float(country_values[n + 1])
        else:
            last_vs_previous = float(np.nan)

        if len(not_nan_values) > 12:
            last_vs_last_year = last - country_values[n + last_year_interval]
        else:
            last_vs_last_year = float(np.nan)

        min_of_entire_series = min(not_nan_values)
        max_of_entire_series = max(not_nan_values)
        percentile = (
            (last - min_of_entire_series) /
              (max_of_entire_series - min_of_entire_series)
        )

        statistics[col.replace(" ", "_").lower()] = {
            "average 3M": average_3m,
            "average 6M": average_6m,
            "average 12M": average_12m,
            "last - previous": last_vs_previous,
            "last - LY": last_vs_last_year,
            "precentile": percentile,
            "last - average 12M": "above" if (last - average_12m) > 0 else "below",
        }

    return pd.DataFrame(statistics)


def compute_stats_percent_change(
        metric: Metric, input_data: pd.DataFrame) -> pd.DataFrame:
    """Compute statistics as percentage change between current and previous"""

    stats: dict[str, list[float, float, float, str]] = {}
    for col in input_data.columns:
        # finding last not nan value
        country_values = list(input_data[col].values)
        country_values.reverse()
        for n, value in enumerate(country_values):
            if not pd.isna(value):
                break
        # last_col_idx = n
        last = country_values[n]

        ly_interval = 12
        if hasattr(metric, 'frequency') and metric.frequency.value == 'q':
            ly_interval = 4

        not_nan_values = [
            value for value in country_values if not pd.isna(value)
        ]
        average_3m = mean(not_nan_values[:3])
        average_6m = mean(not_nan_values[:6])
        average_12m = mean(not_nan_values[:12])

        if len(not_nan_values) > 1:
            previous = float(not_nan_values[n + 1])
            last_to_previous = (last - previous) / previous
        else:
            last_to_previous = float(np.nan)

        if len(not_nan_values) > 12:
            ly = not_nan_values[n + ly_interval]
            last_to_ly = (last - ly) / ly
        else:
            last_to_ly = float(np.nan)

        min_of_entire_series = min(country_values)
        max_of_entire_series = max(country_values)
        percentile = (
            (last - min_of_entire_series)
              / (max_of_entire_series - min_of_entire_series)
        )
        stats[col.replace(" ", "_").lower()] = {
            "last 3M average": average_3m,
            "last 6M average": average_6m,
            "last 12M average": average_12m,
            "last/previous": last_to_previous,
            "last/LY": last_to_ly,
            "precentile": percentile,
            "last - average 12M": "above" if (last - average_12m) > 0 else "below",
        }

    return pd.DataFrame(stats)


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
