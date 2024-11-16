from django.contrib import admin
from harvest_routes.models import Harvester, ScrapingHarvest, MangasLogs, ChaptersLogs


@admin.register(Harvester)
class HarvesterAdmin(admin.ModelAdmin):
    list_display = (
        "domain_name",
        "harvest_type",
        "is_active",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_filter = (
        "harvest_type",
        "is_active",
    )


@admin.register(ScrapingHarvest)
class ScrapingHarvestAdmin(admin.ModelAdmin):
    list_display = ("harvest", "is_active", "updated_at")
    fieldsets = (
        (None, {"fields": ("harvest",)}),
        (
            "Manga Scraping Path",
            {
                "fields": (
                    "manga_list",
                    "manga_title",
                    "manga_genre",
                    "description",
                    "manga_url",
                    "manga_cover_img",
                    "manga_payload",
                )
            },
        ),
        (
            "Chapter Scraping Path",
            {
                "fields": (
                    "chapter_list",
                    "chapter_title",
                    "chapter_url",
                    "chapter_content",
                    "chapter_payload",
                )
            },
        ),
        (
            "Configuration",
            {"fields": ("payload",)},
        ),
        (
            "Infomations",
            {
                "fields": (
                    "is_active",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_filter = (
        "harvest",
        "is_active",
    )


@admin.register(MangasLogs)
class MangasLogsAdmin(admin.ModelAdmin):
    list_display = ("variable", "is_active", "updated_at")
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active",)


@admin.register(ChaptersLogs)
class ChaptersLogsAdmin(admin.ModelAdmin):
    list_display = ("variable", "is_active", "updated_at")
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active",)
