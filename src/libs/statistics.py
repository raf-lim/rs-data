from typing import Protocol
import pandas as pd

from updaters.us.interfaces import Frequency, StatsType


class Metric(Protocol):
    frequency: Frequency
    stats: StatsType


def compute_statistics(
        data: pd.Series,
        year_readings_number: int,
        stats_type: StatsType,
    ) -> dict[str, float | str]:
    """Compute statistics and comaparison to previous readings."""
    percentile = data.rank(pct=True).dropna().iloc[-1]
    average_L3 = data[-3:].mean()
    average_L6 = data[-6:].mean()
    average_1Y = data[-year_readings_number:].mean()
    last = data.dropna().iloc[-1]

    if stats_type == StatsType.DIFFERENCE:
        last_vs_previous = data.dropna().diff().iloc[-1]
        last_vs_last_year = (
            data.dropna().diff(year_readings_number).iloc[-1]
        )
    elif stats_type == StatsType.CHANGE:
        last_vs_previous = data.dropna().pct_change().iloc[-1]
        last_vs_last_year = (
            data.dropna().pct_change(year_readings_number).iloc[-1]
        )
    
    statistics = {}
    statistics["precentile"] = percentile
    statistics["average(3)"] = average_L3
    statistics["average(6)"] = average_L6
    statistics["average(1Y)"] = average_1Y
    statistics["last vs previous"] = last_vs_previous
    statistics["last vs LY"] = last_vs_last_year
    statistics["last-average 12M"] = (
        "above" if (last - average_1Y) > 0 else "below"
    )

    return pd.Series(data=statistics.values(), index=statistics.keys())
