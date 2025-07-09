from django.contrib import admin
from .models import Auction, Scene, EligibleBidder
from adminsortable2.admin import SortableAdminMixin


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("name", "date")
    search_fields = ("name",)


from adminsortable2.admin import SortableAdminMixin


@admin.register(Scene)
class SceneAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "auction", "profile", "order", "ready")
    list_editable = ("ready",)  # don't need 'order' editable now
    list_filter = ("auction", "ready")
    search_fields = ("title", "profile__name", "profile__user__username")


@admin.register(EligibleBidder)
class EligibleBidderAdmin(admin.ModelAdmin):
    list_display = ("code", "desc")
    search_fields = ("code", "desc")
