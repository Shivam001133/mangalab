from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from harvest.spiders.domain_spider import DomainSpider


class Command(BaseCommand):
    help = "Scrape data from given domain"

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain_name",
            "-d",
            dest="domain_name",
            type=str,
            help="The domain name to scrape",
        )

    def handle(self, *args, **kwargs):
        domain_name = kwargs["domain_name"]

        self.stdout.write(
            self.style.SUCCESS(f"Starting Scrapy spider for domain: {domain_name}")
        )

        process = CrawlerProcess(get_project_settings())
        process.crawl(DomainSpider, domain_name=domain_name)
        process.start()

        self.stdout.write(
            self.style.SUCCESS(f"Spider finished running for domain: {domain_name}")
        )
