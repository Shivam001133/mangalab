from django.db import models
from django.utils.translation import gettext_lazy as _


class MenuTitle(models.Model):
    class MenuType(models.TextChoices):
        MENU = 'menu', _('Menu')
        GENERAL = 'general', _('General')

    title = models.CharField(max_length=50, null=False, blank=False)
    menu_type = models.CharField(
        choices=MenuType.choices, default=MenuType.GENERAL,
        max_length=30)
    img = models.ImageField(upload_to='media/menu_title')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MangaCategories(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
