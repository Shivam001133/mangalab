from mangalab_web import apis
from django.urls import path
from rest_framework import routers
router = routers.SimpleRouter()


urlpatterns = [
    path('menu-title/', apis.menu_title, name='menu_title'),
    path('categories/', apis.manga_categories, name='manga_categories'),
]
