from django.contrib import admin
from .models import (Manga, TitleImage, Chapter)


admin.site.register(Manga)
admin.site.register(TitleImage)
admin.site.register(Chapter)

