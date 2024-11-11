from django.contrib import admin
from django.db.models import Q
from mangavault.models import (
    MangaVault,
    MangaGenre,
    MangaChapter,
)


class CustomFilter(admin.SimpleListFilter):
    title = "Cover Image Filter"
    parameter_name = "cover_img"

    def lookups(self, request, model_admin):
        return [
            ("with_value", "With Value"),
            ("without_value", "Without Value"),
            ("empty_value", "Empty Value"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "with_value":
            return queryset.filter(Q(cover_img__isnull=False) & ~Q(cover_img=""))
        if self.value() == "without_value":
            return queryset.filter(Q(cover_img__isnull=True) | Q(cover_img=""))
        if self.value() == "empty_value":
            return queryset.filter(cover_img="")
        return queryset


@admin.register(MangaVault)
class MangaVaultAdmin(admin.ModelAdmin):
    list_display = ("title", "website", "is_active", "updated_at")
    readonly_fields = ("updated_at", "created_at")
    list_filter = (
        CustomFilter,
        "is_active",
    )
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
