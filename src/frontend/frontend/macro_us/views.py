import os

import requests
# import httpx
import pandas as pd

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.shortcuts import render
from django.views import View

from config.settings.local import STATIC_ROOT, STATIC_URL
from frontend.libs import stylers



class MacroUsMetrics(LoginRequiredMixin, View):
    # imgs_dir = os.path.join(STATIC_ROOT, "img_us")
    API_BASE_URL = os.getenv("API_BASE_URL", default="https://rs-data-api.up.railway.app")

    def get(self, request):
        url = os.path.join(self.API_BASE_URL, "us/metric/housing/all")
        response = requests.get(url)
        response.raise_for_status()

        raw_data = response.json()

        data = pd.DataFrame(raw_data["data"])[-6:]
        stats = pd.DataFrame(raw_data["statistics"])

        res = pd.concat([data, stats]).transpose()

        res = stylers.MetricTableStyler(res).style_table_index_with_change_stats()


        context = {"housing": res.to_html()}

        return render(request, "macro_us/us_metrics.html", context)

