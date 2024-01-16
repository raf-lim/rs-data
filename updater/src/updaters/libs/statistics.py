import pandas as pd


def compute_statistics_difference(
        data: pd.Series, year_readings_number: int,
        ) -> dict[str, float | str]:
    """Compute statistics and comaparison to previous readings."""
    percentile = data.rank(pct=True).dropna().iloc[-1]
    average_L3 = data[-3:].mean()
    average_1Y = data[-year_readings_number:].mean()
    last = data.dropna().iloc[-1]

    diff_last_previous = data.dropna().diff().iloc[-1]
    diff_last_last_year = (
        data.dropna().diff(year_readings_number).iloc[-1]
    )

    statistics = {}
    statistics["precentile"] = percentile
    statistics["last-previous"] = diff_last_previous
    statistics["last-LY"] = diff_last_last_year
    statistics["last-average(3)"] = last - average_L3
    statistics["last-average(1Y)"] = last - average_1Y

    return pd.Series(data=statistics.values(), index=statistics.keys())


def compute_statistics_change(
        data: pd.Series, year_readings_number: int,
        ) -> dict[str, float | str]:
    """Compute statistics and comaparison to previous readings."""
    percentile = data.rank(pct=True).dropna().iloc[-1]
    average_L3 = data[-3:].mean()
    average_1Y = data[-year_readings_number:].mean()
    last = data.dropna().iloc[-1]

    change_last_previous = data.dropna().pct_change().iloc[-1]
    change_last_last_year = (
        data.dropna().pct_change(year_readings_number).iloc[-1]
    )
    
    statistics = {}
    statistics["precentile"] = percentile
    statistics["last/previous"] = change_last_previous
    statistics["last/LY"] = change_last_last_year
    statistics["last/average(3)"] = last / average_L3
    statistics["last/average(1Y)"] = last / average_1Y

    return pd.Series(data=statistics.values(), index=statistics.keys())
