# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from manga.models import (Manga, TitleImage, Chapter,
                          MangaSource)


class Mandga(DjangoItem):
    django_model = Manga


class HarvestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
