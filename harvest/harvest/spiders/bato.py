import scrapy
import logging
from scrapy import Request
from harvest.harvest.scraper_helper import model_save_helper as save_helper
from harvest.harvest.scraper_helper.specifie_helper import extract_chapter_number
from manga.models import MangaSource

logger = logging.getLogger(__name__)


class BatoSpider(scrapy.Spider):
    name = "bato"
    image_source = MangaSource.BATO
    base_url = "https://bato.to"
    # allowed_domains = ["bato.to"]
    # start_urls = ["https://bato.to/"]

    def start_requests(self):
        url = "https://bato.to/"
        yield scrapy.Request(url, meta={'playwright': True})

    def parse(self, response):
        manga_list = response.css("#series-list div.item")
        for manga in manga_list:
            manga_title = manga.css('div.item-text a::text').get()
            manga_url = manga.css('div.item-text a::attr(href)').get()
            manga_img = response.css(".rounded::attr(src)").get()

            manga_url = self.base_url + manga_url.strip()
            instance = save_helper.save_manga_list(data={
                'title': manga_title.strip(),
                'manga_url': self.base_url + manga_url.strip(),
            })

            if instance:
                yield Request(url=manga_url, callback=self.parse_manga, meta={'instance': instance})
                logger.info(f"manga {instance.title} saved")

            data = {
                'manga': instance,
                'image': manga_img.strip(),
                'image_source': self.image_source,
            }
            save_helper.save_title_image(data=data)
            if instance:
                logger.info(f"image data saved {instance.title} ")
            logger.info("manga img saved")

    def parse_manga(self, response):
        instance = response.meta['instance']

        manga_desc = response.css("div.mt-3 .limit-html::text").get()

        if manga_desc and not instance.description:
            instance.description = manga_desc
            instance.save()
        logger.info(f"description updated {instance.title}")

        chapter_list = response.css("div.main div.flex-column")
        for chapter in chapter_list:
            chapter_url = chapter.css("a::attr(href)").get()
            chapter_data = chapter.css(".visited.chapt b::text").get()
            chapter_name = chapter.css(".visited.chapt span::text").get()
            chapter_url = self.base_url + chapter_url.strip()

            volume, chapter_no = extract_chapter_number(chapter_data)
            if volume is None or volume == '':
                volume = 1

            if chapter_name:
                chapter_name = chapter_name.replace(":", "").replace(" ", "")
            else:
                chapter_name = ''

            try:
                save_helper.save_chapter_list(data={
                    'manga': instance,
                    'chapter_no': chapter_no,
                    'chapter_name': chapter_name,
                    'volume_no': volume,
                    'chapter_url': chapter_url,
                    'chapter_source': self.image_source,
                })
            except Exception as e:
                logger.error(f"\n\nError: {e}\n\n")

            logger.info(f"Chapter {chapter_name} saved for {instance.title}")
