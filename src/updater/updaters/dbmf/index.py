import os
import time
import pandas as pd
import logging
from sqlalchemy import text
import pandas as pd

from db.base import engine

logging.basicConfig(level=logging.INFO)


DBMF_URL = os.getenv('DBMF_URL')
DB_SCHEMA = 'public'


def get_data():
    """Get data from excel spreadsheet published on the website"""
    df = pd.read_excel(DBMF_URL)
    time.sleep(2)
    df.columns = list(df.iloc[4, :])
    df = df.iloc[5:, :].reset_index(drop=True)

    return df


def main_dbmf() -> None:
    """Update DBMF positioning and save to database"""
    data = get_data().set_index('TICKER')
    with engine.connect() as conn:
        tickers_table_exists = conn.scalar(text(
            '''SELECT EXISTS(
                SELECT FROM information_schema.tables
                WHERE table_schema
                LIKE :schema AND table_name = :table_name
                )'''
            ), {'schema': DB_SCHEMA, 'table_name': 'dbmf_tickers'}
        )
        if tickers_table_exists:
            existing_tickers = pd.read_sql_table(
                table_name='dbmf_tickers',
                con=conn,
                schema=DB_SCHEMA,
                index_col='TICKER',
            )
            new_tickers = set(data.index).difference(set(existing_tickers.index))
            if len(new_tickers) > 0:
                new_data = data.loc[list(new_tickers)].loc[:, 'DESCRIPTION']
                new_data.to_sql(
                    name='dbmf_tickers',
                    con=conn,
                    schema=DB_SCHEMA,
                    if_exists='append',
                )
                logging.info('New data added to dbmf_tickers table.')
            else:
                logging.info('Table dbmf_tickers is up to date.')
        else:
            dbmf_tickers = data.loc[:, 'DESCRIPTION']
            dbmf_tickers.to_sql(
                name='dbmf_tickers',
                con=conn,
                schema=DB_SCHEMA,
                if_exists='replace',
            )
            logging.info('Table dbmf_tickers created.')
        conn.commit()

        for ticker in data.index:
            ticker_data = data.loc[[ticker]][[
                'DATE', 'SHARES', 'BASE_MV', 'PCT_HOLDINGS']]
            ticker_data['DATE'] = pd.to_datetime(
                ticker_data['DATE'], format='%Y%m%d').dt.date
            try:
                existing_data = pd.read_sql_table(
                    table_name=f'dbmf_{ticker.lower()}',
                    con=conn,
                    schema=DB_SCHEMA,
                )
                existing_dates = existing_data.loc[:, ['DATE']]
                existing_dates['DATE'] = pd.to_datetime(
                    existing_dates['DATE'], format='%Y%m%d').dt.date
                
                if (
                    ticker_data.loc[ticker, 'DATE'] not in
                    tuple(existing_dates['DATE']) and 
                    ticker_data.loc[ticker, 'SHARES'] != 
                    existing_data.loc[existing_data.index[-1], 'SHARES']
                    ):
                    ticker_data.to_sql(
                        name=f'dbmf_{ticker.lower()}',
                        con=conn,
                        schema=DB_SCHEMA,
                        if_exists='append',
                        index=False
                    )
                    logging.info(f'Ticker {ticker} data updated.' )
                else:
                    logging.info(f'Ticker {ticker} data up-to-date.')
            except:
                ticker_data.to_sql(
                    name=f'dbmf_{ticker.lower()}',
                    con=conn,
                    schema=DB_SCHEMA,
                    if_exists='replace',
                    index=False
                    )
                logging.info(f'New ticker {ticker} table added.')
        conn.commit()

        tickers = pd.read_sql_table(
            table_name='dbmf_tickers',
            con=conn,
            schema=DB_SCHEMA,
            index_col='TICKER',
            )
        
        for ticker in tickers.index:
            try:
                df = pd.read_sql_table(
                    table_name=f'dbmf_{ticker.lower()}',
                    con=conn,
                    schema=DB_SCHEMA,
                    index_col='DATE',
                    ).sort_index()
                df.index = pd.to_datetime(df.index).date
                df['SHARES'] = df['SHARES'].astype('float64')
                df['BASE_MV'] = df['BASE_MV'].astype('float64')
                if len(df) > 1:
                    df['SHARES change %'] = (
                        df['SHARES'].diff() / df['SHARES'].abs().shift()
                        )
                    df['BASE_MV change %'] = (
                        df['BASE_MV'].diff() / df['BASE_MV'].abs().shift()
                        )       
                    df = df[[
                        'SHARES',
                        'SHARES change %',
                        'BASE_MV',
                        'BASE_MV change %',
                        'PCT_HOLDINGS',
                        ]]
            except ValueError as e:
                logging.info(e)
                continue

            df.to_sql(
                name=f'dbmf_{ticker.lower()}_perf',
                con=conn,
                schema=DB_SCHEMA,
                if_exists='replace'
                )
        conn.commit()
