from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "rating", "city", "country"]
    search_fields = ["user__username", "city", "country"]
    list_filter = ["city", "country"]
