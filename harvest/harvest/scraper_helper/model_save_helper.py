import logging
from manga.models import MangaList, ChapterList, TitleImage
from django.db.utils import IntegrityError
from manga.helpers import messages as msg
# from django.db.models import Q

logger = logging.getLogger(__name__)


def save_title_image(data: dict = None):
    """
    Save the title image of the manga
    """
    required_keys = ['manga', 'image', 'image_source']
    if all(key in data for key in required_keys):
        try:
            obj, created = TitleImage.objects.get_or_create(**data)
            if created:
                logger.info(f"created title image: {data['manga'].title}")
            else:
                logger.info(f"get title image: {data['manga'].title}")
        except IntegrityError as e:
            logger.error(f"Error: {e}")


def save_manga_list(data: dict = None):
    """
    Save the manga list

    Args:
        data (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    required_keys = ['title', 'manga_url']
    if all(key in data for key in required_keys):
        try:
            obj, created = MangaList.objects.get_or_create(**data)
            if not created:
                if obj.description == msg.DEFAULT_DESCRIPTION:
                    return None
                return obj
            else:
                logger.info(f"created title image: {data['title']}")
                return obj
        except IntegrityError as e:
            print(f"Error: {e}")


def save_chapter_list(data: dict = None):
    """

    Args:
        data (_type_, optional): _description_. Defaults to None.
    """
    required_keys = ['manga', 'chapter_no', 'chapter_url', 'chapter_source']
    if all(key in data for key in required_keys):
        try:
            obj, created = ChapterList.objects.get_or_create(**data)
            if created:
                logger.info(f"Updated title image: {data['manga'].title}")
                return obj
            else:
                logger.info(f"created title image: {data['manga'].title}")
                return obj
        except IntegrityError as e:
            logger.error(f"Error: {e}")


def MnagaDescription(instance=None):
    """
    Save the manga description
    """
    try:
        MangaList.objects.filter(description__isnull=True)
        logger.info(f"Updated title image: {instance.title}")
    except Exception as e:
        logger.error(f"Error: {e}")
