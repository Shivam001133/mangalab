from django.db import models
from django.utils.translation import gettext_lazy as _


class HarvestType(models.TextChoices):
    MANGA = "manga", _("Manga")
    ANIME = "anime", _("Anime")
    BOTH = "both", _("Both")
    NONE = "none", _("None")


class Harvester(models.Model):
    domain_name = models.CharField(max_length=25)
    domain_url = models.URLField()
    harvest_type = models.CharField(
        max_length=15,
        choices=HarvestType.choices,
        default=HarvestType.NONE,
    )
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.domain_name


class ScrapingHarvest(models.Model):
    harvest = models.OneToOneField(Harvester, on_delete=models.SET_NULL, null=True)
    # manga information
    manga_list = models.TextField(default=dict)
    manga_title = models.CharField(max_length=150)
    manga_genre_list = models.TextField(default=dict)
    manga_genre = models.CharField(max_length=50)
    description_list = models.TextField(default=dict)
    description = models.CharField(max_length=250)
    re_title = models.TextField(default=dict)
    manga_url = models.CharField(max_length=250)
    re_url = models.TextField(default=dict)
    manga_cover_img = models.CharField(max_length=250)
    re_cover_img = models.TextField(default=dict)
    # chapter information
    chapter_list = models.TextField(default=list)
    chapter_title = models.CharField(max_length=250)
    re_chapter_title = models.TextField(default=dict)
    chapter_url = models.CharField(max_length=250)
    re_chapter_url = models.TextField(default=dict)
    # Configuration
    payload = models.TextField(default=dict)

    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.harvest.domain_name


class MangasLogs(models.Model):
    variable = models.TextField()
    error_log = models.TextField()
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.variable


class ChaptersLogs(models.Model):
    variable = models.TextField()
    error_log = models.TextField()
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.variable
