from django.urls import path
from . import views

app_name = "arrivals"

urlpatterns = [
    path("", views.index, name="index"),
    path("arrival/", views.arrival_info, name="arrival"),
]
