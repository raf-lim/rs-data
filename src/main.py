import logging
from sqlalchemy import text
from db.base import engine, get_db
from updaters.us.interfaces import DataType, StatsType
from updaters.us.fred import metrics
from updaters.us.fred import collectors
from libs import cleaners, statistics


if __name__ == "__main__":

    with engine.connect() as connection:
        # connection.execute(text("CREATE SCHEMA IF NOT EXISTS fred"))
        for metric in metrics.metrics:
            try:
                data = collectors.get_together_constituents_data(
                    metric=metric,
                    data_getter=collectors.get_constituent_data
                )
            except Exception as e:
                logging.warning(f"Collecting data for {metric.name} failed. {e}")
                continue

            data = cleaners.remove_longer_not_reported(
                data=data,
                last_not_reported=6,
            )
            if metric.data == DataType.CHANGE:
                data = statistics.compute_period_to_period_change(
                    metric=metric,
                    frequency=metric.frequency,
                    data=data,
                )

            if metric.stats == StatsType.DIFFERENCE:
                stats = statistics.compute_stats_difference(metric, data)
            elif metric.stats == StatsType.CHANGE:
                stats = statistics.compute_stats_percent_change(metric, data)

            metric_name = metric.name.replace(" ", "_").lower()

            data.to_sql(
                name=f"{metric_name}_data",
                con=connection,
                # schema="fred",
                if_exists="replace",
                index=True,
                index_label="date"
            )

            stats.to_sql(
                name=f"{metric_name}_stats",
                con=connection,
                if_exists="replace",
                index=True,
                index_label="date"
            )
        
        connection.commit()

        #TODO: set index and column names properelly!