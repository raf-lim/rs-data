import time
import logging
import pandas as pd


def fetch_data(spreadsheet_url: str):
    """Get data from excel spreadsheet published on the website"""
    try:
        df = pd.read_excel(spreadsheet_url)
        time.sleep(2)
        return df
    except FileNotFoundError as e:
        logging.warning(e)


def parse_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean data from raw table from spreadsheet"""
    try:
        data.columns = list(data.iloc[4, :])
        return data.iloc[5:, :].reset_index(drop=True)
    except IndexError as e:
        logging.warning(e)

    
