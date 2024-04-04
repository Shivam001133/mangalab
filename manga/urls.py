from manga import apis
from django.urls import path

urlpatterns = [
    path('manga-list/', apis.manga_list,
         name='manga-list'),
]
