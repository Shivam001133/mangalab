from django.contrib import admin
from .models import MenuTitle, MangaCategories


class MenuTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu_type', 'is_active',)
    list_filter = ('menu_type', 'is_active')
    search_fields = ('title', 'menu_type')
    list_per_page = 30
    date_hierarchy = 'created_at'


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_per_page = 30
    ordering = ('-title',)


admin.site.register(MenuTitle, MenuTitleAdmin)
admin.site.register(MangaCategories, CategoriesAdmin)
