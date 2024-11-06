from django.db import models
from django.utils.translation import gettext_lazy as _

# imported models
from mangavault.models import MangaVault

import logging


logger = logging.getLogger(__name__)


class BannerImage(models.Model):
    class BannerSourceType(models.TextChoices):
        Image = "image", _("Image")
        video = "video", _("video")

    manga = models.ForeignKey(
        MangaVault, on_delete=models.CASCADE, related_name="banner_image"
    )
    image = models.ImageField(upload_to="upload/BannerImages/", null=True, blank=True)
    image_url = models.URLField(blank=True)
    source_type = models.CharField(
        choices=BannerSourceType.choices, default=BannerSourceType.Image, max_length=10
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.source_type is self.BannerSourceType.Image:
            return "img_banner-" + self.manga.title
        if self.source_type is self.BannerSourceType.video:
            return "video_banner" + self.manga.title
        return self.manga.title
