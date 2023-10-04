import logging
from db.base import engine
from apps.updater.us.fred import metrics, updater


if __name__ == "__main__":
    with engine.connect() as connection:
        for metric in metrics.metrics:
            data = updater.compile_metric_data(metric)
            data.to_sql(metric.name, connection, if_exists="replace")
        
        connection.commit()