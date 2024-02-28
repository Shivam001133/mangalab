# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from manga.models import Manga, Chapter, TitleImage

class MangaItem(DjangoItem):
    django_model = Manga

class TitleImageItem(DjangoItem):
    django_model = TitleImage

class ChapterItem(DjangoItem):
    django_model = Chapter

class HarvestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
