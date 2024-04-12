from mangalab_web import apis
from django.urls import path
from mangalab_web import views
# from rest_framework import routers
# router = routers.SimpleRouter()

app_name = 'web'

urlpatterns = [
    # path('menu-title/', apis.menu_title, name='menu_title'),
    path('categories/', apis.manga_categories, name='manga_categories'),
    # path('', views.indexView, name='home-page'),
    # path('deatil/', views.animeDetailView, name='anime-detail'),
    # path('watch/', views.amimeWatchView, name='anime-watch'),
    # path('blog/', views.blogView, name='blog'),
    # path('blog-detail/', views.blogDetailView, name='blog-detail'),
    # path('categories/', views.categoriesView, name='catego;ries')
    ]
