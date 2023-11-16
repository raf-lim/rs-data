from django.urls import path
from frontend.macro_eu import views

app_name = 'macro_eu'
urlpatterns = [
    path("metrics/", views.MacroEuMetrics.as_view(), name='macro_eu_metrics'),
    path("countries/", views.MacroEuCountries.as_view(), name='macro_eu_countries'),
]
