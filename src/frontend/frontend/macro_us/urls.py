from django.urls import path
from frontend.macro_us import views

app_name = 'macro_us'
urlpatterns = [
    path("metrics/", views.MacroUsMetrics.as_view(), name='macro_us_metrics'),
    # path("ism-manu/", views.MacroUsIsmManu.as_view(), name='macro_us_ism_manu'),
    # path("ism-serv/", views.MacroUsIsmServ.as_view(), name='macro_us_ism_serv'),
]
