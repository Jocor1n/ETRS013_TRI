from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect


urlpatterns = [
    path("trajet/", include("trajet.urls")),
    path("admin/", admin.site.urls),
    path("loginpage/", include("django.contrib.auth.urls")),
    path("loginpage/", include("loginpage.urls")),
    path('', lambda request: redirect('trajet/', permanent=True))
]