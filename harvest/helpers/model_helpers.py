from django.db import models, transaction, IntegrityError
from src.message import logging_message
import logging

# custom files
from harvest_routes.models import Harvester
from mangavault.models import MangaGenre, MangaVault, MangaChapter, MangaStatus
from harvest_routes.models import ScrapingHarvest, MangasLogs, ChaptersLogs

logger = logging.getLogger(__name__)


def get_domain_info(domain_name: str) -> models:
    """Retrieve domain information based on the domain name."""
    if not domain_name:
        return None
    domain_name = domain_name.strip()
    try:
        return Harvester.objects.get(domain_name=domain_name, is_active=True)
    except Harvester.DoesNotExist:
        logger.exception(
            logging_message.MODELS_NOT_FOUND.format(MESSAGE=domain_name)
        )
        return None


def get_scraping_info(harvest: ScrapingHarvest) -> models:
    """Retrieve the scraping configuration for a given harvest."""
    return ScrapingHarvest.objects.filter(is_active=True, harvest=harvest).first()


def save_manga_to_db(manga_data, genre=None, status=None) -> None:
    """Save manga data to MangaVault model, handling both lists and dictionaries."""
    if genre:
        genre = genre_mapper(genre)
    if status:
        status_list = [
            MangaStatus.ONGOING, MangaStatus.COMPLETED,
            MangaStatus.PAUSED, MangaStatus.CANCELLED,
            MangaStatus.NONE]
        for _status in status_list:
            if status == _status:
                status = _status
                break

    with transaction.atomic():
        if isinstance(manga_data, list):
            for manga in manga_data:
                _save_or_log_manga(manga)
        elif isinstance(manga_data, dict):
            manga_data["status"] = status
            obj = _save_or_log_manga(manga_data, genre)
            print("****"*10, obj)
            return obj
    return None


def _save_or_log_manga(manga, genre) -> None:
    """Helper to save or log existing MangaVault entry."""
    try:
        obj, created = MangaVault.objects.get_or_create(**manga)
        obj.genre.set(genre)
        if created:
            logger.info(f"New entry created: {obj}")
            return obj
        if not created:
            logger.info(f"Existing entry found: {obj}")
            return obj
    except IntegrityError as err:
        MangasLogs.objects.create(
            variable=manga,
            error_log=err,
            is_active=True
        )
        return None


def save_chapter_to_db(chapter_data) -> None:
    """Save chapter data to MangaChapter model, handling both lists and dictionaries."""
    with transaction.atomic():
        if isinstance(chapter_data, list):
            for chapter in chapter_data:
                _save_or_log_chapter(chapter)
        elif isinstance(chapter_data, dict):
            _save_or_log_chapter(chapter_data)


def _save_or_log_chapter(chapter) -> None:
    """Helper to save or log existing MangaChapter entry."""
    try:
        obj, created = MangaChapter.objects.get_or_create(**chapter)
        if created:
            logger.info(f"New chapter entry created: {obj}")
        else:
            logger.info(f"Existing chapter entry found: {obj}")
    except IntegrityError as err:
        ChaptersLogs.objects.create(
            variable=chapter,
            error_log=err,
            is_active=True
        )


def genre_mapper(genre_list: list):
    """
    Map genre to the manga
    """
    return MangaGenre.objects.filter(title__in=genre_list)
