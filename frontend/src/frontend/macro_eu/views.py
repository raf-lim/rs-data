import os
import requests
from requests import HTTPError
import pandas as pd
import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

# from config.settings.local import STATIC_ROOT, STATIC_URL
from frontend.libs import stylers

LIMIT = int(os.getenv("EU_LIMIT_MONTHS"))


class MacroEuMetrics(LoginRequiredMixin, View):
    """Represents EU countries performance - metrics perspective."""
    API_BASE_URL = os.getenv("API_BASE_URL")

    def get(self, request):
        url = os.path.join(self.API_BASE_URL, "eu/metrics")
        response = requests.get(url, timeout=None)
        try:
            response.raise_for_status()
        except HTTPError:
            return render(
                request,
                "404.html",
                {"exception": (
                    f"Not a single EU metric's table in the database. "
                    f"Try feeding the database using updater service."
                    )})

        metrics_metadata = response.json()

        metrics_tables = {}
        for metric_code, meta in metrics_metadata.items():
            metric_all_data_url = os.path.join(
                self.API_BASE_URL, "eu/metric", metric_code,
                )
            response = requests.get(metric_all_data_url)
            try:
                response.raise_for_status()
            except HTTPError:
                continue

            metric_all_data = response.json()
            data = pd.DataFrame(metric_all_data["data"])[-LIMIT:]
            stats_dict = metric_all_data["statistics"]
            stats = pd.DataFrame(
                stats_dict.values(), stats_dict.keys(),
                ).transpose()

            data_with_stats = (
                pd.concat([data, stats]).transpose().fillna(np.NaN)
                )
            table = stylers.MetricTableStyler(data_with_stats)
            styled_table = table.style_table_index_with_difference_stats()

            metrics_tables[meta.get("code").title()] = styled_table.to_html()

        context = {"tables": metrics_tables}

        return render(request, "macro_eu/eu_metrics.html", context)


class MacroEuCountries(LoginRequiredMixin, View):
    """Represents EU countries performance - country perspective."""
    API_BASE_URL = os.getenv("API_BASE_URL")

    def get(self, request):
        countries_codes_url = os.path.join(self.API_BASE_URL, "eu/countries")
        response = requests.get(countries_codes_url, timeout=None)
        print(response)
        try:
            response.raise_for_status()
        except HTTPError:
            return render(
                request,
                "404.html",
                {"exception": (
                    f"Not a single EU country's table in the database. "
                    f"Try feeding the datbase using updater service.")},
                )

        countries_codes: list[str] = response.json()

        countries_tables = {}
        for country_code in countries_codes:
            country_data_url = os.path.join(
                self.API_BASE_URL, "eu/country", country_code, "data",
                )
            country_stats_url = os.path.join(
                self.API_BASE_URL, "eu/country", country_code, "stats",
                )

            response_data = requests.get(country_data_url)
            try:
                response_data.raise_for_status()
            except HTTPError:
                continue
            country_data = response_data.json()

            response_stats = requests.get(country_stats_url)
            try:
                response_stats.raise_for_status()
            except HTTPError:
                continue
            country_stats = response_stats.json()

            data = pd.DataFrame(country_data)[-LIMIT:]
            stats = pd.DataFrame(country_stats)
            data_with_stats = pd.concat([data, stats]).transpose()
            table = stylers.MetricTableStyler(data_with_stats)
            styled_table = table.style_table_index_with_difference_stats()

            countries_tables[country_code.upper()] = styled_table.to_html()

        context = {"tables": countries_tables}

        return render(request, "macro_eu/eu_countries.html", context)
