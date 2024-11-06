from django.contrib import admin
from utils.models import BannerImage


class BannerImageAdmin(admin.ModelAdmin):
    list_display = ("manga", "source_type", "is_active", "created_at")
    search_fields = (
        "manga",
        "source_type",
    )
    list_filter = ["manga", "source_type", "is_active", "created_at"]


admin.site.register(BannerImage, BannerImageAdmin)
