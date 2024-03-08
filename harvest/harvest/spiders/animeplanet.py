import scrapy


class AnimeplanetSpider(scrapy.Spider):
    name = "animeplanet"
    allowed_domains = ["www.anime-planet.com"]
    start_urls = ["https://www.anime-planet.com/"]

    def parse(self, response):
        pass
