import scrapy


class GogoanimeSpider(scrapy.Spider):
    name = "gogoanime"
    allowed_domains = ["ww4.gogoanime2.org"]
    start_urls = ["https://ww4.gogoanime2.org/home"]

    def parse(self, response):
        pass
