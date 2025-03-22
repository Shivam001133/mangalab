from django.core.management.base import BaseCommand
<<<<<<< HEAD
from harvest_routes.models import Harvester
from harvest_routes.models import ScrapingHarvest


class Command(BaseCommand):
    help = "Create harvester and scraping configuration for mangareader.to"

    def handle(self, *args, **kwargs):
        harvest_domain, _ = Harvester.objects.update_or_create(
            domain_name="mangareader.to",
            defaults={
                "domain_url": "https://mangareader.to/home",
                "harvest_type": "MANGA",
=======
from harvest_routes.models import Harvester, ScrapingHarvest


class Command(BaseCommand):
    help = "Create harvester and scraping configuration for toonily.com"

    def handle(self, *args, **kwargs):
        harvest_domain, _ = Harvester.objects.update_or_create(
            domain_name="toonily.com",
            defaults={
                "domain_url": "https://toonily.com/",
                "harvest_type": "MANHWA",
>>>>>>> 7fe7b48 (ui fix for manga)
                "is_active": True,
            }
        )

        ScrapingHarvest.objects.update_or_create(
            harvest=harvest_domain,
            defaults={
<<<<<<< HEAD
                "manga_list": '{"list": [".popular__item"]}',
                "manga_title": ".popular__item__title::text",
                "manga_genre": ".genres a::text",
                "description": ".description__text::text",
                "manga_url": "a::attr(href)",
                "manga_cover_img": "img::attr(src)",
                "manga_payload": {
                    "re_cover_img": ["img"],
                    "detail_img": ".detail__cover img::attr(src)",
                    "status_list": ".detail__meta .meta",
                    "status_heading": "span.label::text",
                    "status": "span.value::text",
                    "list": "a",
                },
                "chapter_list": {
                    "chapter_list": ".chapters__list .chap__item"
                },
                "chapter_title": "a span.name::text",
                "chapter_url": "a::attr(href)",
                "chapter_content": "img::attr(src)",
                "chapter_payload": {
                    "content_list": ".reader__content img"
=======
                "manga_list": '{"list": [".page-item-detail"]}',
                "manga_title": ".item-summary .post-title a::text",
                "manga_genre": ".genres-content a::text",
                "description": ".summary__content p::text",
                "manga_url": ".item-summary .post-title a::attr(href)",
                "manga_cover_img": ".item-thumb img::attr(data-src)",
                "manga_payload": {
                    "re_cover_img": ["img"],
                    "detail_img": ".summary_image img::attr(data-src)",
                    "status_list": ".post-content .post-status",
                    "status_heading": "div > b::text",
                    "status": "div::text",
                    "list": "a",
                },
                "chapter_list": {
                    "chapter_list": "ul.main li.wp-manga-chapter"
                },
                "chapter_title": "a::text",
                "chapter_url": "a::attr(href)",
                "chapter_content": "img::attr(data-src)",
                "chapter_payload": {
                    "content_list": ".reading-content img"
>>>>>>> 7fe7b48 (ui fix for manga)
                },
                "payload": '{}',
                "is_active": True,
            }
        )

<<<<<<< HEAD
        self.stdout.write(self.style.SUCCESS("✅ Successfully created config for mangareader.to"))
=======
        self.stdout.write(self.style.SUCCESS("✅ Successfully created config for toonily.com"))
>>>>>>> 7fe7b48 (ui fix for manga)
