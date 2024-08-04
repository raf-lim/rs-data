from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from libs import exceptions


def extract_tickers_from_db(
        db: Session
    ) -> dict[str, dict[str, str]]:
    """Extract DBMF ticker from ticker's table in database"""
    try:
        data = pd.read_sql_table(
            table_name="dbmf_tickers",
            con=db.connection(),
            index_col="TICKER",
        )
    except ValueError:
        raise exceptions.NoTableFoundException

    if len(data) < 1:
        raise exceptions.NoDbmfTickerFoundException

    return data.to_dict()


def get_position_stats(
        ticker: str, db: Session) -> dict[str, dict[str, float | None]]:
    """Fetch position status from ticker's stats table in db"""
    try:
        data = pd.read_sql_table(
            table_name=f"dbmf_{ticker.lower()}_perf",
            con=db.connection(),
            index_col="index",
        )
    except ValueError:
        raise exceptions.NoTableFoundException
    
    data.index = data.index.astype(str)
    data.replace(to_replace=np.NaN, value=None, inplace=True)

    return data.to_dict()
    
