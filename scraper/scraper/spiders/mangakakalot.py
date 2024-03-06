import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from scraper.scraper.items import ImageItem


class MangakakalotSpider(scrapy.Spider):
    name = "mangakakalot"
    allowed_domains = ["mangakakalot.com"]
    start_urls = ["https://mangakakalot.com/"]

    def parse(self, response):
        property_loader = ItemLoader(item=ImageItem(), response=response)
        property_loader.default_output_processor = TakeFirst()
        manga_list = response.css('div.doreamon div.itemupdate.first')

        for manga in manga_list:
            image = manga.css('a.tooltip.cover.bookmark_check img::attr(src)').get()
            property_loader.add_value('image', image)
            yield property_loader.load_item()
            
            print("********************************************************************")
            print(property_loader.load_item())