import scrapy


class AnimenineSpider(scrapy.Spider):
    name = "animenine"
    allowed_domains = ["ww1.9animetv.pro"]
    start_urls = ["https://ww1.9animetv.pro/"]

    def parse(self, response):
        pass
