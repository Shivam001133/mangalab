from django.shortcuts import render


def home_view(request):
    context = {
        "data": range(1, 9999),
    }
    return render(request, "pages/home.html", context)
