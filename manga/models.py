from django.db import models
from django.utils.translation import gettext_lazy as _
# from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field
from manga.helpers import messages as msg


class MnagaType(models.TextChoices):
    MANHWA = 'manhwa', _('Manhwa')
    MANGA = 'manga', _('Manga')
    MANHUA = 'manhua', _('Manhua')
    COMIC = 'comic', _('Comic')
    OTHER = 'other', _('Other')


class MangaList(models.Model):
    title = models.CharField(max_length=100, unique=True)
    manga_url = models.URLField(unique=True)
    manga_type = models.CharField(
        choices=MnagaType.choices, default=MnagaType.OTHER,
        max_length=30)
    description = CKEditor5Field(blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MangaSource(models.TextChoices):
    MANHWAZ = 'manhwaz', _('Manhwaz')
    MANGAKAKALOT = 'mangakakalot', _('Mangakakalot')
    OTHER = 'other', _('Other')


class TitleImage(models.Model):
    manga = models.ForeignKey(MangaList, on_delete=models.CASCADE,
                              related_name='mangaimage',
                              null=True, blank=True)
    image = models.URLField(unique=True)
    image_source = models.CharField(
        max_length=50, choices=MangaSource.choices,
        default=MangaSource.OTHER)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.manga.title


class ChapterList(models.Model):
    manga = models.ForeignKey(MangaList, on_delete=models.CASCADE,
                              related_name='mangachapter')
    chapter_no = models.IntegerField(null=True, blank=True)
    chapter_name = models.CharField(max_length=100, null=True, blank=True)
    volume_no = models.PositiveSmallIntegerField(default=1)
    latest = models.BooleanField(default=False)
    treanding = models.BooleanField(default=False)
    chapter_source = models.CharField(
        choices=MangaSource.choices, default=MangaSource.OTHER,
        max_length=50)
    chapter_url = models.URLField(unique=True)

    is_live = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.manga.title
