from django.core.management.base import BaseCommand

from harvest_routes.models import Harvester
from harvest_routes.models import ScrapingHarvest


class Command(BaseCommand):
    help = "Create harvester and scraping configuration for toonily.com"

    def handle(self, *args, **kwargs):
        harvest_domain, _ = Harvester.objects.update_or_create(
            domain_name="toonily.com",
            defaults={
                "domain_url": "https://toonily.com/",
                "harvest_type": "MANHWA",
                "is_active": True,
            }
        )

        ScrapingHarvest.objects.update_or_create(
            harvest=harvest_domain,
            defaults={
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
                },
                "payload": '{}',
                "is_active": True,
            }
        )
        self.stdout.write(self.style.SUCCESS("✅ Successfully created config for toonily.com"))

