from manga.models import (Manga, TitleImage, Chapter,
                          MangaSource)
import logging
# from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


def get_chaper_no(chapter_name=None):
    if chapter_name:
        chapter_name = chapter_name.strip().split(' ')
        chapter_no = [i for i in chapter_name if i.isdigit()]
        return chapter_no[0]
    return None

def save_manga(data):
    if data:
        if data['source'] in MangaSource.choices:
            logger.info(f"***************Source: {data['source']}")
            manga_source = MangaSource.choices[data['source']]
        else:
            manga_source = MangaSource.OTHER
        manga = Manga.objects.get_or_create(
            title=data['title'], manga_type=manga_source)
        manga = Manga.objects.filter(
            title=data['title'])
        if manga.exists():
            manga = manga.first()

            data = {
                'manga': manga,
                'chapter_source': manga_source,
                'chapter_url': data['chapter_url'].strip(),
            }
            Chapter.objects.create(data)

            data = {
                'manga': manga,
                'chapter_source': manga_source,
                'chapter_url': data['chapter_url'].strip(),
            }

            _, _ = TitleImage.objects.get_or_create(
                manga=manga, image=data['image_url'],
                image_source=manga_source)


