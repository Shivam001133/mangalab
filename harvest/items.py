# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from mangavault.models import MangaVault


class MangaVaultItem(DjangoItem):
    django_model = MangaVault
