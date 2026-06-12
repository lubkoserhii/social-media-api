from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import Profile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (("Contact", {"fields": ("email",)}),)
    list_display = ("email", "username", "is_staff", "is_active")
    ordering = ("email",)


admin.site.register(Profile)
