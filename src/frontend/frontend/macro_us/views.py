import os
import requests
import pandas as pd
import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from config.settings.local import STATIC_ROOT, STATIC_URL
from frontend.libs import stylers


class MacroUsMetrics(LoginRequiredMixin, View):
    # imgs_dir = os.path.join(STATIC_ROOT, "img_us")
    API_BASE_URL = os.getenv("API_BASE_URL")

    def get(self, request):
        url = os.path.join(self.API_BASE_URL, "us/metrics")
        response = requests.get(url)
        response.raise_for_status()

        metrics_metadata = response.json()

        metrics_tables = {}

        for metric_code, meta in metrics_metadata.items():
            metric_all_data_url = os.path.join(
                self.API_BASE_URL, "us/metric", metric_code,
                )
            response = requests.get(metric_all_data_url)
            response.raise_for_status()

            metric_all_data = response.json()
            data = pd.DataFrame(metric_all_data["data"])[-6:]
            stats_dict = metric_all_data["statistics"]
            stats = pd.DataFrame(
                stats_dict.values(), stats_dict.keys(),
                ).transpose()

            data_with_stats = (
                pd.concat([data, stats])
                .transpose()
                .fillna(np.NaN)
                )

            table = stylers.MetricTableStyler(data_with_stats)

            if meta["data"] == "index" and meta["stats"] == "difference":
                styled_table = table.style_table_index_with_difference_stats()
            elif meta["data"] == "index" and meta["stats"] == "change":
                styled_table = table.style_table_index_with_change_stats()
            elif meta["data"] == "change" and meta["stats"] == "difference":
                styled_table = table.style_table_change_with_difference_stats()

            metrics_tables[meta.get("name")] = styled_table.to_html()

        context = {"metrics_tables": metrics_tables}

        return render(request, "macro_us/us_metrics.html", context)

