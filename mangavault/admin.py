from django.contrib import admin
from mangavault.models import (
    MangaVault,
    MangaGenre,
    MangaChapter,
)


@admin.register(MangaVault)
class MangaVaultAdmin(admin.ModelAdmin):
    list_display = ("title", "website", "is_active", "updated_at")
    readonly_fields = ("updated_at", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)


@admin.register(MangaGenre)
class MangaGenreAdmin(admin.ModelAdmin):
    list_display = ("title", "related_to", "is_active", "updated_at")
    readonly_fields = ("updated_at", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(MangaChapter)
class MangaChapterAdmin(admin.ModelAdmin):
    list_display = ("chapter_title", "manga", "is_active", "updated_at")
    readonly_fields = ("updated_at", "created_at")
    list_filter = ("is_active", "is_new", "is_latest", "is_trending")
    search_fields = ("chapter_title", "manga")
