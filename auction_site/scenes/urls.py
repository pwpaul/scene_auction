from django.urls import path
from . import views

urlpatterns = [
    path("auctions/", views.auction_list, name="auction_list"),
    path("auctions/<int:auction_id>/scene/", views.add_scene, name="add_scene"),
    path("admin-scenes/", views.admin_scene_dashboard, name="admin_scene_dashboard"),
    path(
        "admin-scenes/toggle-ready/<int:scene_id>/",
        views.toggle_scene_ready,
        name="toggle_scene_ready",
    ),
    path(
        "projection/<int:scene_id>-<slug:slug>/",
        views.projection_view,
        name="projection_view",
    ),
]
