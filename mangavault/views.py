import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# models
from mangavault.models import MangaVault, MangaChapter
from utils.models import BannerImage


def home_view(request):
    weekly_spotlight = [
        ("AFK", "images/afk.jpg", "Action"),
        ("The Mad Gate", "images/mad_gate.jpg", "Fantasy"),
        ("Chaos Girl", "images/chaos_girl.jpg", "Sci-Fi"),
        ("Carrier of the Mask", "images/carrier.jpg", "Drama"),
        ("Sunshine Cafe", "images/sunshine.jpg", "Slice of Life"),
        ("Dishonor", "images/dishonor.jpg", "Thriller"),
    ]

    trending = [
        ("The Delinquent Heiress", "images/heiress.jpg"),
        ("Spirit Tracer", "images/spirit_tracer.jpg"),
        ("Mastery", "images/mastery.jpg"),
        ("Tales of the Dragon Consort", "images/dragon_consort.jpg"),
        ("Magmeli of the Azure Sea", "images/magmeli.jpg"),
    ]

    return render(request, "pages/home.html", {
        "weekly_spotlight": weekly_spotlight,
        "trending": trending,
    })


def manga_detail(request):
    context = {
        'title': "The Zombie Won’t Bite Me",
        'rating': 2.9,
        'vote_count': 68,
        'author': "Updating",
        'status': "Ongoing",
        'views': "18,582",
        'genres': "Action, Drama, Manhwa, Adventure",
        'cover_image': "images/zombie-cover.jpg",
        'summary': """
            The Zombie Won’t Bite Me is a manga/manhwa series... (summary content goes here)
        """,
        'chapters': [
            {'name': 'Chapter 15', 'views': '726 views', 'time': '17 hours ago'},
            {'name': 'Chapter 14', 'views': '567 views', 'time': '17 hours ago'},
            {'name': 'Chapter 13', 'views': '600 views', 'time': '17 hours ago'},
            {'name': 'Chapter 12', 'views': '922 views', 'time': '1 day ago'},
            {'name': 'Chapter 11', 'views': '823 views', 'time': '1 day ago'},
        ],
        'comments': [
            {'user': 'Aj3theone', 'time': '3 hours ago', 'text': 'Chapter 5 repeater in peak even when the earth is in apocalypse'},
            {'user': 'Reader01', 'time': '13 hours ago', 'text': 'Thanks ❤️'},
        ]
    }
    return render(request, 'pages/detail.html', context)


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
