import os
import importlib
from typing import AnyStr
from sqlalchemy import Connection, text
from sqlalchemy.exc import ProgrammingError
from updaters.us.interfaces import UsMetric
from updaters.libs import exceptions


def get_metrics_from_plugins(plugins_path: str) -> list[UsMetric]:
    """Get metrics objects from plugins files."""
    plugins = os.scandir(plugins_path)
    package_name = plugins_path.replace("/", ".")
    metrics: list[UsMetric] = []
    for plugin in plugins:
        if plugin.name.startswith("metric"):
            metric_plugin_name = plugin.name.rstrip("py").rstrip(".")
            metric_plugin = importlib.import_module(
                f".{metric_plugin_name}",
                package=package_name,
                )
            metrics.append(metric_plugin.Metric())

    return metrics


def extract_metric_metadata(metric: UsMetric) -> dict[str, AnyStr]:
    """Creates dict with selected US metric descriptors."""
    metric_metadata = {
        "code": metric.code,
        "name": metric.name,
        "frequency": metric.frequency,
        "data": metric.data,
        "stats": metric.stats,
    }

    return metric_metadata


def find_last_metric_data_date_in_db(
        metric: UsMetric, db_connection: Connection,
        ) -> str:
    """Get last date from metric's data table in database."""
    table_name = f"us_{metric.name.replace(' ', '_')}_data".lower()
    try:
        last_date = db_connection.scalar(
            text(f"SELECT date FROM {table_name} ORDER BY date DESC LIMIT 1")
            )
    except ProgrammingError:
        raise exceptions.NoTableFoundException
        
    return last_date
