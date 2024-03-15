import scrapy
import logging
from scrapy import Request
# from scrapy.loader import ItemLoader
# from scrapy.loader.processors import TakeFirst
from  harvest.harvest.scraper_helper import model_save_helper as save_helper
from harvest.harvest.scraper_helper.specifie_helper import extract_chapter_number
from manga.models import MangaSource


logger = logging.getLogger(__name__)

class MangakakalotSpider(scrapy.Spider):
    name = "mangakakalot"
    allowed_domains = ["mangakakalot.com"]
    start_urls = ["https://mangakakalot.com/"]
    image_source = MangaSource.MANGAKAKALOT

    def parse(self, response):
        manga_list = response.css('div.doreamon div.itemupdate.first')

        for manga in manga_list:
            image = manga.css('a.tooltip.cover.bookmark_check img::attr(src)').get()
            title = manga.css('ul li a::text').get()
            link = manga.css('ul li a::attr(href)').get()

            instance = save_helper.save_manga_list(data={
                'title': title.strip(),
                'manga_url': link.strip(),
            })

            yield Request(url=link.strip(), callback=self.parse_manga, meta={'instance': instance})

            data = {
                'manga': instance,
                'image': image.strip(),
                'image_source': self.image_source,
            }
            save_helper.save_title_image(data=data)
            
            logger.info(f"image data scraped {data} and manga {instance.title} saved")

    def parse_manga(self, response):
        instance = response.meta['instance']

        scraper_data = response.css('div.container div.main-wrapper div.leftCol')
        chapters_list = scraper_data.css('div#chapter.chapter div.manga-info-chapter div.chapter-list div.row')

        manga_description = scraper_data.css('div#noidungm::text').getall()
        description = ''
        for info in manga_description:
            description += info.strip()
        if not instance.description:
            instance.description = description
            instance.save()

        manga_description = response.xpath('//*[@id="panel-story-info-description"]/text()').getall()
        for info in manga_description:
            description += info.strip()
        if description:
            instance.description = description
            instance.save()

        for chapter in chapters_list:
            chapter_url = chapter.css('span a::attr(href)').get()
            chapter_name = chapter.css('span a::text').get()

            volume, chapter_no = extract_chapter_number(chapter_name)
            if volume is None or volume == '':
                volume = 1

            try:
                save_helper.save_chapter_list(data={
                    'manga': instance,
                    'chapter_no': chapter_no,
                    'chapter_name': chapter_name.strip(),
                    'volume_no': volume,
                    'chapter_url': chapter_url.strip(),
                    'chapter_source': self.image_source,
                })
            except Exception as e:
                logger.error(f"\n\nError: {e}\n\n")

            logger.info(f"Chapter {chapter_name} saved for {instance.title}")

