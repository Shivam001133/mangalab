import scrapy
from helpers import get_chaper_no

class ManhwazSpider(scrapy.Spider):
    name = "manhwaz"
    allowed_domains = ["manhwaz.com"]
    start_urls = ["https://manhwaz.com"]

    def parse(self, response):
        items = response.css('#slide-top .item.col-4.col-md-2')
        for item in items:
            image_data  = response.css('.img-item')
            image_url = image_data.css('a img::attr(src)').get()
            latest_url = image_data.css('.btn-link::attr(href)').get()
            latest_chapter = image_data.css('.btn-link::text').get()
            manga_name = item.css('.line-2 a::text').get()
            manga_url = item.css('.line-2 a::attr(href)').get()
            # title = item.css('a::text').get()
            # url = item.css('a::attr(href)').get()
            
            yield {
                '': '******************************',
                'image': image_url,
                'url': latest_url,
                'lt': latest_chapter,
                'manga_name': manga_name,
            }
