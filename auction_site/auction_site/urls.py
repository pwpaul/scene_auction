from django.contrib import admin
from django.urls import path, include
from profiles import views as profile_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # for login/logout
    path("", include("profiles.urls")),  # dashboard/profile
    path("", include("scenes.urls")),  # auctions & scenes
    path("", profile_views.home, name="home"),
    path("dashboard/", profile_views.dashboard, name="dashboard"),
    path("profile/edit/", profile_views.edit_profile, name="edit_profile"),
    path("faq/", profile_views.faq, name="faq"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)