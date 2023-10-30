import logging
import pandas as pd
from db.base import engine
from updaters.us.interfaces import DataType
from updaters.us.fred import metrics
from updaters.us.fred import collectors
from libs import cleaners, statistics, helpers


def main_us(db_connection):

    for metric in metrics.metrics:
        try:
            metric_data = collectors.get_together_constituents_data(
                metric=metric,
                data_getter=collectors.get_constituent_data
            )
        except Exception as e:
            logging.warning(f"Collecting data for {metric.name} failed. {e}")
            continue

        clean_metric_data = cleaners.remove_longer_not_reported(
            data=metric_data,
            last_not_reported=6,
        )
        if metric.data == DataType.CHANGE:
            clean_metric_data = helpers.compute_period_to_period_change(
                metric=metric,
                frequency=metric.frequency,
                data=metric_data,
            )
        
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
