import sys
from os import getenv
import logging
from typing import AnyStr
import pandas as pd
from requests import HTTPError, RequestException
from db.base import engine
from updaters.us.interfaces import DataType, StatsType
from updaters.us.fred import metrics, collectors
from updaters.libs import exceptions
from updaters.libs import cleaners, statistics, helpers


def main_us() -> None:
    """Main function for US updater app."""
    US_METRICS_PLUGINS_PATH = "updaters/us/fred/metrics_plugins"
    FRED_BASE_URL = getenv("FRED_BASE_URL")
    API_KEY = getenv("FRED_API_KEY")

    selected_metrics = (
        metrics.get_metrics_from_plugins(US_METRICS_PLUGINS_PATH)
        )

    metrics_metadata: dict[str, dict[str, AnyStr]] = {}
    for metric in selected_metrics:
        metrics_metadata.update(
            {metric.code: metrics.extract_metric_metadata(metric)}
            )
        # Check whether data in db table is up-to-date.
        # If it is then no update for this metric.
        try:
            with engine.connect() as connection:
                last_date_in_db = metrics.find_last_metric_data_date_in_db(
                    metric, connection
                    )
            name_of_first_constituent = tuple(metric.constituents.keys())[0]
            const_url = collectors.get_constituent_url(
                name_of_first_constituent, limit=1,
                fred_base_url=FRED_BASE_URL, api_key=API_KEY
                )
            last_date_in_api = (
                collectors.fetch_constituent_data(const_url)
                ["observations"][0]["date"]
                )

            if last_date_in_db == last_date_in_api:
                continue

        # In case of sqlalchemy error if table not exists program runs
        # and create the table for the metric
        except exceptions.MissingFredApiKeyException:
            logging.error("FRED API key not set")
            sys.exit(1)
        except RequestException as e:
            logging.warning(e)
            continue
        except exceptions.NoTableFoundException:
            pass

        readings_limit = collectors.set_limit_of_readings(
            frequency=metric.frequency,
            period_limits=helpers.PeriodDataLimits
            )

        # Fetch and parse constituents data and gather into dataframe.
        metric_data: dict[str, dict[str, float]] = {}
        for const_code, const_name in metric.constituents.items():
            try:
                const_url = collectors.get_constituent_url(
                    const_code, limit=readings_limit,
                    fred_base_url=FRED_BASE_URL, api_key=API_KEY
                    )
                raw_data = collectors.fetch_constituent_data(const_url)
            except HTTPError as e:
                logging.warning(f"Error {metric.name}.{const_name} {e}")
            except exceptions.FredApiNoObservationsDataException:
                logging.warning(f"Invalid data for {metric.name}.{const_name}")
                continue
            data = collectors.parse_constituent_data(raw_data)
            const_name = const_name.replace(" ", "_").lower()
            metric_data[const_name] = data
                
        metric_data = pd.DataFrame(metric_data).sort_index()
        
        # Clean constituents series recently not reported.
        # and convert into percentage change series if relevant.  
        clean_metric_data = cleaners.remove_longer_not_reported(
            data=metric_data, last_not_reported=6
            )
        if metric.data == DataType.CHANGE:
            clean_metric_data = helpers.compute_period_to_period_change(
                metric=metric, data=metric_data
                )
            
        # Compute statistics of constituent series.
        stats = pd.DataFrame()
        for constituent in clean_metric_data.columns:
            data = clean_metric_data[constituent]
            year_readings_number = (
                helpers.set_full_year_readings_number(metric.frequency)
                )
            if metric.stats == StatsType.DIFFERENCE:
                stats_data = statistics.compute_statistics_difference(
                    data, year_readings_number
                    )
            elif metric.stats == StatsType.CHANGE:
                stats_data = statistics.compute_statistics_change(
                    data, year_readings_number
                    )
            stats_data.name = constituent.replace(" ", "_").lower()
            stats = pd.concat([stats, stats_data], axis=1)

        # Save metrics dataframes with
        # clean data and statistics in database.
        
        with engine.connect() as connection:

            clean_metric_data.to_sql(
                name=f"us_{metric.code}_data",
                con=connection,
                if_exists="replace",
                index=True,
                index_label="date"
                )

            stats.to_sql(
                name=f"us_{metric.code}_stats",
                con=connection,
                if_exists="replace",
                index=True,
                index_label="index"
                )
            
            connection.commit()

    # Create and save table with all metrics metadata.
    metrics_metadata_table = (pd.DataFrame(metrics_metadata)).transpose()
    
    with engine.connect() as connection:
        metrics_metadata_table.to_sql(
            name="us_metrics_metadata",
            con=connection,
            if_exists="replace",
            index=False
        )
        connection.commit()