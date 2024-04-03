from rest_framework import serializers
from .models import TitleImage, ChapterList, MangaList


class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'data_manga'
        model = MangaList
        fields = ('title', 'manga_url', 'manga_type', 'description',)


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'data_img'
        model = TitleImage
        fields = ('manga', 'image', 'image_source',)


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'data_chapter'
        model = ChapterList
        fields = ('manga', 'chapter_no', 'chapter_name', 'volume_no',
                  'latest', 'treanding', 'chapter_url', 'is_live')
