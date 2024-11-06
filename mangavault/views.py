from django.shortcuts import render
from django.db.models import Q

# models
from utils.models import BannerImage


def home_view(request):
    banner = BannerImage.objects.filter(
        Q(image__isnull=False) & ~Q(image='') | Q(image_url__exact='')
    )
    banner = BannerImage.objects.all()
    context = {
        "banner": banner,
    }
    return render(request, "pages/home.html", context)
