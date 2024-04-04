from mangalab_web.models import MenuTitle, MangaCategories
from rest_framework import serializers


class MenuTitleSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = 'data_menu_title'
        model = MenuTitle
        fields = ('title', 'menu_type', 'img')


class MangaCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = 'data_manga_categories'
        model = MangaCategories
        fields = ('title', 'description')
