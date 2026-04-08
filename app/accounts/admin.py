from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CardScanUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("CardScan", {"fields": ("role",)}),)
    list_display = ("username", "email", "role", "is_active", "is_staff")
