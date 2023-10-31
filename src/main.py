import logging
import pandas as pd
from requests import HTTPError
from db.base import engine
from updaters.us.interfaces import DataType
from updaters.us.fred import metrics
from updaters.us.fred import collectors
from libs import cleaners, statistics, helpers


def main_us(db_connection):

    for metric in metrics.selected_metrics:
        start_date = collectors.set_fred_api_start_date(metric.frequency)

        # Fetch and parse constituents data and gather into dataframe.
        metric_data: dict[str, dict[str, float]] = {}
        for const_code, const_name in metric.constituents.items():
            try:
                raw_data = collectors.fetch_constituent_data(
                    const_code, start_date
                    )
                # logging.info(f"OK {metric.name}.{const_name}")
            except HTTPError as e:
                logging.warning(f"Error {metric.name}.{const_name} {e}")
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
        metric_name = metric.name.replace(" ", "_").lower()
        
        clean_metric_data.to_sql(
            name=f"us_{metric_name}_data",
            con=db_connection,
            if_exists="replace",
            index=True,
            index_label="date"
            )

        stats.to_sql(
            name=f"us_{metric_name}_stats",
            con=db_connection,
            if_exists="replace",
            index=True,
            index_label="metric"
            )
    

if __name__ == "__main__":

    with engine.connect() as connection:
        main_us(connection)

        connection.commit()
