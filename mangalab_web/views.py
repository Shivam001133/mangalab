from django.shortcuts import render
from manga.models import MangaList, TitleImage


# def indexView(request):
#     data = []
#     mangas = list(TitleImage.objects.all())
#     print(mangas)
#     for img in mangas[:7]:
#         data.append({
#             "title": img.manga.title,
#             "img": img.image
#         })
#     print(data)
#     for i in data:
#         print(f"**** {i}")

#     return render(request, 'anime-main/index.html', context={"context": data})

# def animeDetailView(request):
#     return render(request, 'anime-main/anime-details.html')

# def amimeWatchView(request):
#     return render(request, 'anime-main/anime-watching.html')

# def blogView(request):
#     return render(request, 'anime-main/blog.html')

# def blogDetailView(request):
#     return render(request, 'anime-main/blog-details.html')


# def categoriesView(request):
#     return render(request, 'anime-main/categories.html')

# def amimeWatchView(request):
#     return render(request, 'anime-main/anime-watching.html')