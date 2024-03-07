import scrapy
import logging
from scrapy import Request
# from scrapy.loader import ItemLoader
# from scrapy.loader.processors import TakeFirst
import harvest.scraper.scraper_helper.model_save_helper as save_helper
from manga.models import ChapterList, MangaSource


logger = logging.getLogger(__name__)

class MangakakalotSpider(scrapy.Spider):
    name = "mangakakalot"
    allowed_domains = ["mangakakalot.com"]
    start_urls = ["https://mangakakalot.com/"]
    image_source = MangaSource.MANGAKAKALOT

    def parse(self, response):
        manga_list = response.css('div.doreamon div.itemupdate.first')

        for manga in manga_list:
            # image_item_loader = ItemLoader(item=ImageItem(), response=response)
            image = manga.css('a.tooltip.cover.bookmark_check img::attr(src)').get()
            title = manga.css('ul li a::text').get()
            link = manga.css('ul li a::attr(href)').get()
            # image_item_loader.add_value('image', image)
            # yield image_item_loader.load_item()

            # yield Request(url=link.strip(), callback=self.parse_manga)


            instance = save_helper.save_manga_list(data={
                'title': title.strip(),
                'manga_url': link.strip(),
            })

            data = {
                'manga': instance,
                'image': image.strip(),
                'image_source': self.image_source,
            }
            save_helper.save_title_image(data=data)
            
            logger.info(f"image data scraped *****: {title, link}")
    
    # def parse_manga(self, response):
    #     chapters_list = response.css('div.container div.main-wrapper div.leftCol div#chapter.chapter div.manga-info-chapter div.chapter-list div.row')

    #     for chapter in chapters_list:
    #         chapter_url = chapter.css('span a::attr(href)').get()
    #         chapter_name = chapter.css('span a::text').get()

    #         save_helper.save_chapter_list(data={
    #             'manga': ,
    #             'chapter_no': chapter_name.strip(),
    #             'chapter_url': chapter_url.strip(),
    #             'chapter_source': self.image_source,
            # })


