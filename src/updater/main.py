import os
import logging
from typing import AnyStr
import pandas as pd
from requests import HTTPError
from sqlalchemy.exc import ProgrammingError
from db.base import engine
from updaters.us.interfaces import DataType
from updaters.us.fred import metrics, collectors
from updaters.us import exceptions
from updaters.libs import cleaners, statistics, helpers

US_METRICS_PLUGINS_PATH = os.getenv("US_METRICS_PLUGINS_PATH")


def main_us() -> None:

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
                    metric, connection,
                    )
            name_of_first_constituent = tuple(metric.constituents.keys())[0]
            last_date_in_api = collectors.fetch_constituent_data(
                    name_of_first_constituent, limit=1,
                    )["observations"][0]["date"]

            if last_date_in_db == last_date_in_api:
                continue

        # In case of sqlalchemy error if table not exists program runs
        # and create the table for the metric
        except ProgrammingError as e:
            pass

        readings_limit = collectors.set_limit_of_readings(metric.frequency)

        # Fetch and parse constituents data and gather into dataframe.
        metric_data: dict[str, dict[str, float]] = {}
        for const_code, const_name in metric.constituents.items():
            try:
                raw_data = collectors.fetch_constituent_data(
                    const_code, readings_limit
                    )
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
            data=metric_data, last_not_reported=6,
            )
        if metric.data == DataType.CHANGE:
            clean_metric_data = helpers.compute_period_to_period_change(
                metric=metric, data=metric_data,
                )
            
        # Compute statistics of constituent series.
        stats = pd.DataFrame()
        for constituent in clean_metric_data.columns:
            data = clean_metric_data[constituent]
            year_readings_number = (
                helpers.set_full_year_readings_number(metric.frequency)
                )
            stats_data = statistics.compute_statistics(
                    data, year_readings_number, metric.stats
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
                index_label="metric"
                )
            
            connection.commit()

    # Create and save table with all metrics metadata.
    metrics_metadata_table = (
        pd.DataFrame(metrics_metadata)
        ).transpose()
    
    with engine.connect() as connection:
        metrics_metadata_table.to_sql(
            name="us_metrics_metadata",
            con=connection,
            if_exists="replace",
            index=False,
        )
        connection.commit()

if __name__ == "__main__":
    main_us()

