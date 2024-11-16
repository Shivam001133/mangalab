import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# models
from mangavault.models import MangaVault, MangaChapter
from utils.models import BannerImage


def home_view(request):
    banner = BannerImage.objects.filter(
        Q(image__isnull=False) & ~Q(image="") | Q(image_url__exact="")
    )
    banner = BannerImage.objects.all()
    data = MangaVault.objects.filter(is_active=True)
    context = {"banner": banner, "data": data}
    return render(request, "pages/home.html", context)


def manga_detail(request, pk):
    manga = get_object_or_404(MangaVault, pk=pk)
    chapters = MangaChapter.objects.filter(manga=manga)
    return render(
        request, "pages/manga_detail.html", {"manga": manga, "chapters": chapters}
    )


def manga_read_chapter(request, pk):
    chapter = get_object_or_404(MangaChapter, pk=pk)
    manga = chapter.manga
    chapters = MangaChapter.objects.filter(manga=manga)
    next_chapter = chapters.filter(pk__gt=chapter.pk).order_by("pk").first()
    context = {
        "chapter": chapter,
        "manga_title": manga.title,
        "chapters": chapters,
        "next_chapter": next_chapter,
        "chapter_url": json.loads(chapter.chapter_list),
    }
    return render(request, "pages/manga_chapter.html", context)
