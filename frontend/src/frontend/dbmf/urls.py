from django.urls import path
from frontend.dbmf import views

app_name = 'dbmf'
urlpatterns = [
    path("", views.DbmfView.as_view(), name='dbmf'),
]
