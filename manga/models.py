from django.db import models
from django.utils.translation import ugettext_lazy as _


class MnagaType(models.CharField):
    MANHWA = 'manhwa', _('Manhwa')
    MANGA = 'manga', _('Manga')
    MANHUA = 'manhua', _('Manhua')
    COMIC = 'comic', _('Comic')


class Manga(models.Model):
    title = models.CharField(max_length=100)

    manga_type = models.CharField(choise=MnagaType, default=MnagaType.MANGA)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MangaSource(models.CharField):
    MANHWAZ = 'manhwaz', _('Manhwaz')
    OTHER = 'other', _('Other')


class TitleImage(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE,
                              related_name='mangaimage')
    image = models.URLField()
    image_source = models.CharField(
        max_length=50, choise=MangaSource, 
        default=MangaSource.OTHER)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.manga.title


class Chapter(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE,
                              related_name='mangachapter')
    latest = models.BooleanField(default=False)
    treanding = models.BooleanField(default=False)
    chapter_source = models.CharField(
        choise=MangaSource, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.manga.title
    
