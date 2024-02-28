from calendar import c
import scrapy
from harvest.items import MangaItem, ChapterItem, TitleImageItem
from harvest.helpers import get_chaper_no
# from helpers import save_manga

class ManhwazSpider(scrapy.Spider):
    name = "manhwaz"
    allowed_domains = ["manhwaz.com"]
    start_urls = ["https://manhwaz.com/"]

    def parse(self, response):
        items = response.css('#slide-top .item.col-4.col-md-2')
        manga = MangaItem()
        chapter = ChapterItem()
        title_image = TitleImageItem()

        for item in items:
            image_data  = response.css('.img-item')
            title_image['image'] = image_data.css('a img::attr(src)').get()
            chapter['chapter_url'] = image_data.css('.btn-link::attr(href)').get()
            chapter_name = image_data.css('.btn-link::text').get()
            manga['title'] = item.css('.line-2 a::text').get()
            manga['manga_url'] = item.css('.line-2 a::attr(href)').get()

            chapter['chapter_no'] = get_chaper_no(chapter_name)
            
            # if title and manga_url:
            #     data = {
            #         'title': title,
            #         'manga_url': manga_url,
            #         'image_url': image_url,
            #         'chapter_url': chapter_url,
            #         'chapter': chapter_name
            #     }
            # save_manga(data)
