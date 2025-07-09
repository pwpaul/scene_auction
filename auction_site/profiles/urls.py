from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.edit_profile, name="edit_profile"),
    path(
        "force-password-change/",
        views.force_password_change,
        name="force_password_change",
    ),
]
