import scrapy


class ManhwazSpider(scrapy.Spider):
    name = "manhwaz"
    allowed_domains = ["manhwaz.com"]
    start_urls = ["https://manhwaz.com/"]

    def parse(self, response):
        # manga_list = response.css("div.site-content div.container div.main-col.col-md-8.col-sm-8 div.manga-content div.row.px-2.list-item div.col-6.col-md-4.col-lg-3.badge-pos-1.px-2")
        manga_list = response.xpath("/html/body/div[2]/div/div/div[1]/div[2]/div")
        print("*******************************************")
        print(manga_list)
        for manga in manga_list:
            manga_title = manga.xpath("/div[1]/div/div[2]/div[1]/h3/a/text()").get()
            # manga_url = manga.xpath("/div[1]/div/div[2]/div[1]/h3/a/@href").get()
            yield {
                "title": manga_title,
                # "manga_url": manga_url,
            }
