from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from social.models import Comment, Post, Profile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (("Contact", {"fields": ("email",)}),)
    list_display = ("email", "username", "is_staff", "is_active")
    ordering = ("email",)


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
