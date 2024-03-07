import logging
from manga.models import MangaList, ChapterList, TitleImage

logger = logging.getLogger(__name__)

def save_title_image(data=None):
    required_keys = ['manga', 'image', 'image_source']
    if all(key in data for key in required_keys):
        try:
            TitleImage.objects.create(**data)
            logger.info(f"Saved title image: {data['manga'].title}")
        except TitleImage.DoesNotExist as e:
            logger.error(f"Error: {e}")
            
def save_manga_list(data=None):
    required_keys = ['title', 'manga_url']
    if all(key in data for key in required_keys):
        try:
            mangalist = MangaList.objects.create(**data)
            logger.info(f"Saved manga list: {data['title']}")
            return mangalist
        except MangaList.DoesNotExist as e:
            print(f"Error: {e}")
        

def save_chapter_list(data=None):
    required_keys = ['manga', 'chapter_no', 'chapter_url', 'chapter_source']
    if all(key in data for key in required_keys):
        try:
            ChapterList.objects.create(**data)
            logger.info(f"Saved chapter list: {data['manga'].title}")
        except ChapterList.DoesNotExist as e:
            logger.error(f"Error: {e}")
