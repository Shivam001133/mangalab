import scrapy


class BatoSpider(scrapy.Spider):
    name = "bato"
    allowed_domains = ["bato.to"]
    start_urls = ["https://bato.to/"]

    def parse(self, response):
        pass
