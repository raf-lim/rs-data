import pandas as pd


def remove_longer_not_reported(
        data: pd.DataFrame,
        last_not_reported: int,
    ) -> pd.DataFrame:
    """Remove column if number of last N/A >= last_not_reported"""
    data = data.dropna(
        axis=1, how='all', subset=data.index[-last_not_reported:],
    )

    return data