from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # for login/logout
    path("", include("profiles.urls")),  # dashboard/profile
    path("", include("scenes.urls")),  # auctions & scenes
]
