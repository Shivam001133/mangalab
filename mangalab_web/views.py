from django.shortcuts import render


def indexView(request):
    return render(request, 'anime-main/index.html')
