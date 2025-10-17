from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("config.apps.accounts.urls")),
    path("", include("config.apps.arrivals.urls")),
    path("accounts/", include("allauth.urls")),  # /accounts/google/login/ 등
]
