import scrapy


class MangafoxfullSpider(scrapy.Spider):
    name = "mangafoxfull"
    allowed_domains = ["mangafoxfull.com"]
    start_urls = ["https://mangafoxfull.com/"]

    def parse(self, response):
        pass
