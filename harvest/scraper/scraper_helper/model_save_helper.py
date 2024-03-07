import logging
from manga.models import MangaList, ChapterList, TitleImage

logger = logging.getLogger(__name__)

def save_title_image(data=None):
    """
    Save the title image of the manga
    """
    required_keys = ['manga', 'image', 'image_source']
    if all(key in data for key in required_keys):
        try:
            obj, created=TitleImage.objects.update_or_create(**data)
            if obj:
                logger.info(f"Updated title image: {data['manga'].title}")
            elif created:
                logger.info(f"created title image: {data['manga'].title}")
        except TitleImage.DoesNotExist as e:
            logger.error(f"Error: {e}")
            
def save_manga_list(data=None):
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
            obj, mangalist = MangaList.objects.update_or_create(**data)
            if obj:
                logger.info(f"Updated title image: {data['title']}")
                return mangalist
            elif mangalist:
                logger.info(f"created title image: {data['title']}")
                return mangalist
        except MangaList.DoesNotExist as e:
            print(f"Error: {e}")
        

def save_chapter_list(data=None):
    """

    Args:
        data (_type_, optional): _description_. Defaults to None.
    """
    required_keys = ['manga', 'chapter_no', 'chapter_url', 'chapter_source']
    if all(key in data for key in required_keys):
        try:
            obj, chapter = ChapterList.objects.update_or_create(**data)
            if obj:
                logger.info(f"Updated title image: {data['manga'].title}")
                return chapter
            elif chapter:
                logger.info(f"created title image: {data['manga'].title}")
                return chapter
        except ChapterList.DoesNotExist as e:
            logger.error(f"Error: {e}")
