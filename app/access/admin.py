from django.contrib import admin

from .models import AccessGroup


@admin.register(AccessGroup)
class AccessGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    search_fields = ("name", "slug")
