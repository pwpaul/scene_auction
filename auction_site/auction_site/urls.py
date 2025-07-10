from django.contrib import admin
from django.urls import path, include
from profiles import views as profile_views
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # for login/logout
    path("", include("profiles.urls")),  # dashboard/profile
    path("", include("scenes.urls")),  # auctions & scenes
    path("", profile_views.home, name="home"),
    path("dashboard/", profile_views.dashboard, name="dashboard"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

]
