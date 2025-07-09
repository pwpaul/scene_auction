from django.urls import path
from . import views

urlpatterns = [
    path("auctions/", views.auction_list, name="auction_list"),
    path("auctions/<int:auction_id>/scene/", views.add_scene, name="add_scene"),
]
