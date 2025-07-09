from django.contrib import admin
from .models import Auction, Scene


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("name", "date")
    search_fields = ("name",)


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ("title", "auction", "profile", "role", "ready")
    list_filter = ("auction", "role", "ready")
    search_fields = ("title", "profile__user__username")
