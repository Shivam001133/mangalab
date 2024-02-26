import scrapy
from helpers import save_manga

class ManhwazSpider(scrapy.Spider):
    name = "manhwaz"
    allowed_domains = ["manhwaz.com"]
    start_urls = ["https://manhwaz.com"]

    def parse(self, response):
        items = response.css('#slide-top .item.col-4.col-md-2')
        for item in items:
            image_data  = response.css('.img-item')
            image_url = image_data.css('a img::attr(src)').get()
            chapter_url = image_data.css('.btn-link::attr(href)').get()
            chapter_name = image_data.css('.btn-link::text').get()
            title = item.css('.line-2 a::text').get()
            manga_url = item.css('.line-2 a::attr(href)').get()
            
            if title and manga_url:
                data = {
                    'title': title,
                    'manga_url': manga_url,
                    'image_url': image_url,
                    'chapter_url': chapter_url,
                    'chapter': chapter_name
                }
            save_manga(data)
