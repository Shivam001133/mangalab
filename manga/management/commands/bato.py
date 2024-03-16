from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import harvest.harvest.settings as scrapy_settings
from harvest.harvest.spiders.bato import BatoSpider


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(scrapy_settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(BatoSpider)
        process.start()
