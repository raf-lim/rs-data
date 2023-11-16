import os
import requests
import pandas as pd
import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

# from config.settings.local import STATIC_ROOT, STATIC_URL
from frontend.libs import stylers


class MacroEuMetrics(LoginRequiredMixin, View):
    API_BASE_URL = os.getenv("API_BASE_URL")
    LIMIT = int(os.getenv("EU_LIMIT_METRICS"))

    def get(self, request):
        url = os.path.join(self.API_BASE_URL, "eu/metrics")
        response = requests.get(url)
        response.raise_for_status()

        metrics_metadata = response.json()

        metrics_tables = {}

        for metric_code, meta in metrics_metadata.items():
            metric_all_data_url = os.path.join(
                self.API_BASE_URL, "eu/metric", metric_code,
                )
            response = requests.get(metric_all_data_url)
            response.raise_for_status()

            metric_all_data = response.json()
            data = pd.DataFrame(metric_all_data["data"])[-self.LIMIT:]
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
            styled_table = table.style_table_index_with_difference_stats()

            metrics_tables[meta.get("code").title()] = styled_table.to_html()

        context = {"metrics_tables": metrics_tables}

        return render(request, "macro_eu/eu_metrics.html", context)


class MacroEuCountries(LoginRequiredMixin, View):
    pass
