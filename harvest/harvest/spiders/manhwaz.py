import scrapy
import logging
from scrapy import Request
from harvest.harvest.scraper_helper import model_save_helper as save_helper
from harvest.harvest.scraper_helper.specifie_helper import extract_chapter_number
from manga.models import MangaSource

logger = logging.getLogger(__name__)


class ManhwazSpider(scrapy.Spider):
    name = "manhwaz"
    allowed_domains = ["manhwaz.com"]
    start_urls = ["https://manhwaz.com/"]
    image_source = MangaSource.MANHWAZ

    def parse(self, response):
        manga_list = response.css("div.manga-content div.row.px-2.list-item div.col-6")

        for manga in manga_list:
            manga_title = manga.css('.item-summary .line-2 a::text').get()
            manga_url = manga.css('.item-summary .line-2 a::attr(href)').get()

            print("Title:", manga_title)
            print("URL:", manga_url)

            instance = save_helper.save_manga_list(data={
                'title': manga_title.strip(),
                'manga_url': manga_url.strip(),
            })

            if instance:
                yield Request(url=manga_url.strip(), callback=self.parse_manga, meta={'instance': instance})

                logger.info(f"manga {instance.title} saved")

    def parse_manga(self, response):
        instance = response.meta['instance']

        manga_desc = response.css("div.summary__content p::text").get()
        if manga_desc and not instance.description:
            instance.description = manga_desc
            instance.save()
        logger.info(f"description updated {instance.title}")

        manga_img = response.css("div.summary_image a img::attr(src)").get()
        data = {
            'manga': instance,
            'image': manga_img.strip(),
            'image_source': self.image_source,
        }
        save_helper.save_title_image(data=data)
        logger.info(f"image data saved {instance.title} ")

        chapter_list = response.css("div.list-chapter ul.list-item li.wp-manga-chapter")
        for chapter in chapter_list:
            chapter_url = chapter.css("a::attr(href)").get()
            chapter_name = chapter.css("a::text").get()

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
