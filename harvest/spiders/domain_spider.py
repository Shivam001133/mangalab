# domain_scraper/spiders/domain_spider.py
from harvest.helpers.model_helpers import get_domain_info
from mangavault.models import MangaStatus, MangaCategory
from src.scrapy.domain_scrape import DomainScrape

# from harvesters.models import Harvester
from harvest.items import MangaVaultItem
import logging
import scrapy


logger = logging.getLogger(__name__)


class DomainSpider(scrapy.Spider):
    name = "domain_spider"
    allowed_domains = []

    def __init__(self, domain_name=None, *args, **kwargs):
        domain_name = domain_name.strip()
        harvest = get_domain_info(domain_name)
        self.domain_name = [
            harvest.domain_name,
        ]
        self.start_urls = [
            harvest.domain_url,
        ]
        self.allowed_domains = [
            harvest.domain_name,
        ]
        self.ds = DomainScrape(domain_name)
        self.manga_item = MangaVaultItem()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "errback": self.errback,
                },
            )

    def latest_manga(self, response):
        path = self.ds.Manhwaz.Treanding
        manga_list = response.css(path.MangaList)
        for manga in manga_list:
            title = manga.css(path.MANGA_TITLE).get()
            cover_img = manga.css(path.IMG_URL).get()
            vault_url = manga.css(path.MANGA_URL).get()

            manga_item = MangaVaultItem(
                title=title,
                cover_img=cover_img,
                vault_url=vault_url,
                category=MangaCategory.MANHUA,
                status=MangaStatus.ONGOING,
            )
            yield manga_item

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        self.latest_manga(response)

    async def errback(self, failure):
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()
        logger.error(f"Request failed: {failure}")
