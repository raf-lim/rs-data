import os
import pathlib
import importlib

from updaters.us.interfaces import UsMetric

plugins_path = os.path.join(os.getcwd(), "updaters/us/fred/metrics_plugins")
plugins = os.scandir(plugins_path)

selected_metrics: list[UsMetric] = []

for plugin in plugins:
    if plugin.name.startswith("metric"):
        metric_plugin_name = plugin.name.rstrip("py").rstrip(".")
        metric_plugin = importlib.import_module(
            f".{metric_plugin_name}", package="updaters.us.fred.metrics_plugins",
            )

        selected_metrics.append(metric_plugin.Metric())
