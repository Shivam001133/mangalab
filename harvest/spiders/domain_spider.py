import scrapy
import json
import logging
from asgiref.sync import sync_to_async
from harvest.helpers.model_helpers import (
    get_domain_info,
    get_scraping_info,
    save_manga_to_db,
    save_chapter_to_db,
)
from harvest.helpers.scrape_helper import extract_chapter_no, extract_manga_title

logger = logging.getLogger(__name__)


class DomainSpider(scrapy.Spider):
    name = "domain_spider"
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
    }

    def __init__(self, domain_name=None):
        domain_name = domain_name.strip()
        self.harvest_domain = get_domain_info(domain_name)
        self.scraping_harvest = get_scraping_info(self.harvest_domain)
        self.domain_name = [self.harvest_domain.domain_name]
        self.start_urls = [self.harvest_domain.domain_url]
        self.allowed_domains = [self.harvest_domain.domain_name]
        print("*"*100)
        print(self.allowed_domains)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "errback": self.errback,
                },
                callback=self.parse,
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await self.scroll_page(page)
        # get list contanig manga
        manga_list_items = json.loads(self.scraping_harvest.manga_list)
        cover_img_selectors = self.scraping_harvest.manga_payload.get("re_cover_img", [])

        for manga_list_item in manga_list_items.get("list"):
            manga_items = response.css(manga_list_item)
            for i, manga in enumerate(manga_items):
                manga_title = manga.css(self.scraping_harvest.manga_title).get()
                title, title_list = extract_manga_title(manga_title)
                vault_url = manga.css(self.scraping_harvest.manga_url).get()

                cover_img = await self._get_cover_image(page, manga, cover_img_selectors)

                mangavault_data = {
                    "website": self.harvest_domain,
                    "title": title,
                    "manga_title": title_list,
                    "vault_url": vault_url,
                    "cover_img": cover_img,
                    "is_active": True,
                }
                if i == 2:
                    break

                yield scrapy.Request(
                    url=vault_url,
                    meta={
                        "mangavault_data": mangavault_data,
                        "playwright": True,
                        "playwright_include_page": True,
                        "errback": self.errback,
                    },
                    callback=self.parse_chapter,
                )

        await page.close()

    async def scroll_page(self, page, scrolls=10, wait_ms=1000):
        """Scrolls the page to load JS-rendered content."""
        for _ in range(scrolls):
            await page.evaluate("window.scrollBy(0, window.innerHeight);")
            await page.wait_for_timeout(wait_ms)

    async def _get_cover_image(self, page, manga, selectors):
        for img_path in selectors:
            try:
                await page.wait_for_selector(img_path.strip(), timeout=5000)
                cover_img = manga.css(self.scraping_harvest.manga_cover_img).get()
                if cover_img:
                    return cover_img
            except Exception:
                continue
        return None

    async def parse_chapter(self, response):
        page = response.meta["playwright_page"]
        await self.scroll_page(page)
        mangavault_data = response.meta.get("mangavault_data")
        genre_list = []
        status = "unknown"

        if not mangavault_data.get("cover_img"):
            cover_img = response.css(
                self.scraping_harvest.manga_payload.get("detail_img")
            ).get()
            mangavault_data["cover_img"] = cover_img

        manga_description = response.css(self.scraping_harvest.description).get()
        if manga_description:
            mangavault_data["description"] = manga_description

        genre_scrape = self.scraping_harvest.manga_payload
        for items in response.css(genre_scrape.get("status_list")):
            heading = (items.css(genre_scrape.get("status_heading")).get() or "").strip().lower()
            if heading == "status":
                status = (items.css(genre_scrape.get("status")).get() or "").strip().lower()
            elif "genre" in heading:
                genre_list = [
                    (genre.css(self.scraping_harvest.manga_genre).get() or "").strip().capitalize()
                    for genre in items.css(genre_scrape.get("list"))
                ]
        print("*"*100)
        print(mangavault_data)
        manga_obj = await sync_to_async(save_manga_to_db)(
            mangavault_data, genre=genre_list, status=status
        )
        logger.info(f"Manga data saved: {mangavault_data['title']}")

        for i, chapter in enumerate(response.css(self.scraping_harvest.chapter_list.get("chapter_list"))):
            chapter_title = chapter.css(self.scraping_harvest.chapter_title).get()
            chapter_url = chapter.css(self.scraping_harvest.chapter_url).get()

            chapter_data = {
                "chapter_title": chapter_title,
                "manga": manga_obj,
                "chapter_url": chapter_url,
                "chapter_number": extract_chapter_no(chapter_title),
            }
            if i ==2 :
                break

            yield scrapy.Request(
                url=chapter_url,
                meta={
                    "chapter_data": chapter_data,
                    "playwright": True,
                    "playwright_include_page": True,
                    "errback": self.errback,
                },
                callback=self.parse_chapter_content,
            )
        await page.close()

    async def parse_chapter_content(self, response):
        page = response.meta["playwright_page"]
        await self.scroll_page(page)
        chapter_data = response.meta.get("chapter_data")
        chapter_content = response.css(
            self.scraping_harvest.chapter_payload.get("content_list")
        )
        img_list = [
            img.css(self.scraping_harvest.chapter_content).get()
            for img in chapter_content
        ]
        chapter_data["chapter_list"] = img_list
        print("*"*100)
        print(chapter_data)
        await sync_to_async(save_chapter_to_db)(chapter_data)
        logger.info(f"Chapter saved: {chapter_data['chapter_title']}")
        await page.close()

    async def errback(self, failure):
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()
