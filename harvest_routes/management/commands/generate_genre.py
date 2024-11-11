import requests
import logging
from django.core.management.base import BaseCommand
from harvest_routes.models import HarvestType
from mangavault.models import MangaGenre

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Sync MangaGenre with Jikan API. Use -m for manga only, "
        "-a for anime only, or run without options to sync both."
    )
    # Define API URLs
    anime_url = "https://api.jikan.moe/v4/genres/anime"
    manga_url = "https://api.jikan.moe/v4/genres/manga"

    def add_arguments(self, parser):
        parser.add_argument(
            "-m", "--manga", action="store_true", help="Sync only manga genres"
        )
        parser.add_argument(
            "-a", "--anime", action="store_true", help="Sync only anime genres"
        )

    def api_to_json(self, res):
        res.raise_for_status()
        data = res.json().get("data", [])
        if data:
            return [genre["name"] for genre in data]
        return None

    def genre_to_db(self, sync_manga, sync_anime):
        if sync_manga and sync_anime:
            logger.error("Please use only one of -m or -a, or no options for both.")

        if not sync_manga and not sync_anime:
            sync_manga = sync_anime = True

        try:
            anime_genres = {}
            if sync_anime:
                anime_genres = self.api_to_json(requests.get(self.anime_url, timeout=5))

            manga_genres = {}
            if sync_manga:
                manga_genres = self.api_to_json(requests.get(self.manga_url, timeout=5))

        except requests.RequestException as e:
            logger.info(f"Error fetching data: {e}")

        combined_genres = set(anime_genres).union(set(manga_genres))
        for genre_name in combined_genres:
            if genre_name in anime_genres and genre_name in manga_genres:
                related_to = HarvestType.BOTH
            elif genre_name in anime_genres:
                related_to = HarvestType.ANIME
            elif genre_name in manga_genres:
                related_to = HarvestType.MANGA
            else:
                continue

            MangaGenre.objects.update_or_create(
                title=genre_name,
                defaults={
                    "title": genre_name,
                    "description": "",
                    "related_to": related_to,
                    "is_active": True,
                },
            )

    def handle(self, *args, **options):
        sync_manga = options["manga"]
        sync_anime = options["anime"]
        self.genre_to_db(sync_manga, sync_anime)

        self.stdout.write(self.style.SUCCESS("Genres synchronized successfully."))
