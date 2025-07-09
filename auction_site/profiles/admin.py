from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "is_staff", "must_change_password")
    list_filter = ("is_staff", "is_superuser", "must_change_password")


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
