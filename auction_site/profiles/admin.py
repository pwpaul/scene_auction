from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "is_staff", "must_change_password")
    list_filter = ("is_staff", "is_superuser", "must_change_password")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "pronouns", "avatar_tag", "ready")
    list_filter = ("ready",)
    search_fields = ("user__username", "name", "pronouns")

    def avatar_tag(self, obj):
        return format_html(
            '<img src="{}" style="width:40px; height:40px; border-radius:50%;">',
            obj.get_avatar_url()
        )
    avatar_tag.short_description = 'Avatar'


admin.site.register(User, UserAdmin)

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User, Profile


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = "Profile"


# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline,)
#     list_display = ("username", "email", "is_staff", "must_change_password")
#     list_filter = ("is_staff", "is_superuser", "must_change_password")


# admin.site.register(User, UserAdmin)
# admin.site.register(Profile)
