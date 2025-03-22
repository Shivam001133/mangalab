from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# models
from mangavault.models import MangaVault, MangaChapter
from utils.models import BannerImage
import logging


def home_view(request):
    mangavoult = MangaVault.objects.all()

    return render(request, "pages/home.html", {
        "hero": mangavoult,
        "weekly_spotlight": mangavoult,
        "trending": mangavoult,
    })


def manga_detail(request, pk):
    manga = MangaVault.objects.get(pk=pk)
    chapters = MangaChapter.objects.filter(manga=manga)
    chapter_first = chapters.first()
    chapter_last = chapters.last()
    return render(request, 'pages/manga_detail.html', {
        "chapters": chapters,
        "manga": manga,
        "chapter_first": chapter_first.pk if chapter_first else None,
        "chapter_last": chapter_last.pk if chapter_last else None,})


def manga_read_chapter(request, pk):
    chapter = get_object_or_404(MangaChapter, pk=pk)
    manga = chapter.manga
    chapters = MangaChapter.objects.filter(manga=manga).order_by("pk")

    next_chapter = chapters.filter(pk__gt=chapter.pk).first()
    previous_chapter = chapters.filter(pk__lt=chapter.pk).last()

    context = {
        "chapter": chapter,
        "manga_title": manga.title,
        "chapters": chapters,
        "next_chapter": next_chapter,
        "previous_chapter": previous_chapter,
        "chapter_url": chapter.chapter_list,
        "comments": [],
    }
    return render(request, "pages/manga_chapter.html", context)
