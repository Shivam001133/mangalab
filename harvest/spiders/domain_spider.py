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
from scrapy_playwright.page import PageCoroutine
from harvest.helpers.scrape_helper import (
    extract_chapter_no, extract_manga_title)

logger = logging.getLogger(__name__)

class DomainSpider(scrapy.Spider):
    name = "domain_spider"
    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
    }

    def __init__(self, domain_name=None):
        domain_name = domain_name.strip()
        self.harvest_domain = get_domain_info(domain_name)
        self.scraping_harvest = get_scraping_info(self.harvest_domain)
        self.domain_name = [self.harvest_domain.domain_name]
        self.start_urls = [self.harvest_domain.domain_url]
        self.allowed_domains = [self.harvest_domain.domain_name]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_coroutines": self._scroll_actions(),
                    "errback": self.errback,
                },
                callback=self.parse,
            )

    def _scroll_actions(self, scroll_count=5, wait_time=2000):
        """Helper to return a list of page coroutines for scrolling."""
        return [
            PageCoroutine("evaluate", "window.scrollBy(0, document.body.scrollHeight)")
            for _ in range(scroll_count)
        ] + [PageCoroutine("wait_for_timeout", wait_time)]

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await self._perform_scrolling(page)

        manga_list_items = json.loads(self.scraping_harvest.manga_list)
        cover_img_selectors = json.loads(
            self.scraping_harvest.re_cover_img).get("re_cover_img", [])
        for manga_list_item in manga_list_items.get("list"):
            manga_items = response.css(manga_list_item)
            for manga in manga_items:
                manga_title = manga.css(self.scraping_harvest.manga_title).get()
                title, title_list = extract_manga_title(manga_title)
                vault_url = manga.css(self.scraping_harvest.manga_url).get()

                cover_img = await self._get_cover_image(
                    page, manga, cover_img_selectors)

                mangavault_data = {
                    "website": self.harvest_domain,
                    "title": title,
                    "manga_title": title_list,
                    "vault_url": vault_url,
                    "cover_img": cover_img,
                    "is_active": True,
                }
                yield response.follow(
                    vault_url,
                    meta={
                        "mangavault_data": mangavault_data,
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_coroutines": self._scroll_actions(),
                        "errback": self.errback,
                    },
                    callback=self.parse_chapter,
                )
        await page.close()

    async def _perform_scrolling(self, page, scroll_count=5, wait_time=2000):
        """Helper to perform page scrolling with delay."""
        for _ in range(scroll_count):
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_timeout(wait_time)

    async def _get_cover_image(self, page, manga, selectors):
        """Tries to retrieve cover image based on multiple selectors."""
        for img_path in selectors:
            await page.wait_for_selector(img_path.strip(), timeout=500)
            cover_img = manga.css(self.scraping_harvest.manga_cover_img).get()
            if cover_img:
                return cover_img
        return None

    async def parse_chapter(self, response):
        page = response.meta["playwright_page"]
        mangavault_data = response.meta.get("mangavault_data")
        await self._perform_scrolling(page)

        chapter_list = json.loads(self.scraping_harvest.chapter_list)
        manga_description = response.css(self.scraping_harvest.description).get()

        if not mangavault_data["cover_img"]:
            cover_img = response.css(json.loads(
                self.scraping_harvest.re_cover_img).get("detail_img")).get()
            mangavault_data["cover_img"] = cover_img

        if manga_description:
            mangavault_data["description"] = manga_description

        genre_scrape = json.loads(self.scraping_harvest.manga_genre_list)
        for items in (response.css(genre_scrape.get("status_list"))):
            heading = (items.css(genre_scrape.get("status_heading")).get()
                       ).strip().lower()
            if  heading == "status":
                status = items.css(genre_scrape.get("status")).get().strip().lower()
            if "genre" in heading:
                genre_list = [
                    (genre.css(self.scraping_harvest.manga_genre).get()
                     ).strip().capitalize()
                    for genre in items.css(genre_scrape.get("list"))
                ]

        # Save manga and chapter data to the database
        manga_obj = await sync_to_async(save_manga_to_db)(
            mangavault_data, genre=genre_list, status=status)
        print("############"*10, manga_obj)
        # logger.info(f"Manga data: {mangavault_data} saved")

        chapters = []
        for chapter in response.css(chapter_list.get("chapter_list")):
            chapter_title = chapter.css(self.scraping_harvest.chapter_title).get()
            chapter_url = chapter.css(self.scraping_harvest.chapter_url).get()

            chapters.append({
                "chapter_title": chapter_title,
                "manga": manga_obj,
                "chapter_url": chapter_url,
                "chapter_number": extract_chapter_no(chapter_title),
            })
        await page.close()

        for chapter_data in chapters:
            await sync_to_async(save_chapter_to_db)(chapter_data)
            logger.info(f"Chapter data: {chapter_data} saved")

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
