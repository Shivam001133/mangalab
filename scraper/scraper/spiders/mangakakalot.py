import scrapy


class MangakakalotSpider(scrapy.Spider):
    name = "mangakakalot"
    allowed_domains = ["mangakakalot.com"]
    start_urls = ["https://mangakakalot.com/"]


    def parse(self, response):
        manga_list = response.xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div[@class='itemupdate first']")
        
        for manga in manga_list:
            yield {
                "title": manga.css("tooltip img::attr(src)").get(),
            }
