import os
import importlib
from updaters.us.interfaces import UsMetric


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