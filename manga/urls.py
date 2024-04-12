from manga import apis
from django.urls import path

app_name = 'mangas'

urlpatterns = [
    path('manga-list/', apis.manga_list,
         name='manga-list'),
]
