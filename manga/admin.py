from django.contrib import admin
from .models import (MangaList, TitleImage, ChapterList)
from django.template.defaultfilters import truncatechars
from django.db.models import Q


class DescriptionFilter(admin.SimpleListFilter):
    title = 'description'
    parameter_name = 'description'

    def lookups(self, request, model_admin):
        return (
            ('has_description', 'Has Description'),
            ('no_description', 'No Description'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'has_description':
            return queryset.filter(
                Q(description__isnull=False) &
                ~Q(description__exact=''))
        if self.value() == 'no_description':
            return queryset.filter(
                Q(description__isnull=True) |
                Q(description__exact=''))





class MangaListAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'manga_type', 'is_active', 'created_at', )
    list_filter = ('manga_type', DescriptionFilter, 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    # search_fields = ('title', 'manga_url')

    def short_description(self, obj):
        return truncatechars(obj.description, 100)
    short_description.short_description = 'Short Description'


class TitleImageAdmin(admin.ModelAdmin):
    list_display = ('manga_title', 'image_source', 'is_active', 'created_at')
    list_filter = ('image_source', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    # search_fields = ('manga', 'image')

    def manga_title(self, obj):
        return truncatechars(obj.manga.title, 30)
    manga_title.short_description = 'Manga Title'

class ChapterListAdmin(admin.ModelAdmin):
    list_display = ('manga_title', 'chapter_no', 'latest', 'treanding', 'chapter_source', 'is_live', 'created_at')
    list_filter = ('latest', 'treanding', 'chapter_source', 'is_live', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    # search_fields = ('manga', 'chapter_no', 'chapter_url')

    def manga_title(self, obj):
        return truncatechars(obj.manga.title, 30)
    manga_title.short_description = 'Manga Title'

admin.site.register(TitleImage, TitleImageAdmin)
admin.site.register(ChapterList, ChapterListAdmin)
admin.site.register(MangaList, MangaListAdmin)
