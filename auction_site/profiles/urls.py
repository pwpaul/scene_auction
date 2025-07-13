from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.edit_profile, name="edit_profile"),
    path(
        "force-password-change/",
        views.force_password_change,
        name="force_password_change",
    ),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
