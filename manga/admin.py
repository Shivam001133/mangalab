from django.contrib import admin
from .models import (MangaList, TitleImage, ChapterList)


class MangaListAdmin(admin.ModelAdmin):
    list_display = ('title', 'manga_type', 'is_active', 'created_at')
    list_filter = ('manga_type', 'is_active', 'created_at', 'updated_at')
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

