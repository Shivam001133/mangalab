from .apis import MangaListApi
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from rest_framework import routers
router = routers.SimpleRouter()

# router.register(r'xyz', MangaListApi,
#                 basename='manga-list')

urlpatterns = [
    path('list/', MangaListApi.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
