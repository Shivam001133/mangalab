from django.contrib import admin
from .models import (MangaList, TitleImage, ChapterList)
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
    list_display = ('title', 'description', 'manga_type', 'is_active', 'created_at')
    list_filter = ('manga_type', DescriptionFilter, 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    # search_fields = ('title', 'manga_url')


class TitleImageAdmin(admin.ModelAdmin):
    list_display = ('manga', 'image_source', 'is_active', 'created_at')
    list_filter = ('image_source', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    # search_fields = ('manga', 'image')

class ChapterListAdmin(admin.ModelAdmin):
    list_display = ('manga', 'chapter_no', 'latest', 'treanding', 'chapter_source', 'is_live', 'created_at')
    list_filter = ('latest', 'treanding', 'chapter_source', 'is_live', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    # search_fields = ('manga', 'chapter_no', 'chapter_url')

admin.site.register(MangaList, MangaListAdmin)
admin.site.register(TitleImage, TitleImageAdmin)
admin.site.register(ChapterList, ChapterListAdmin)

