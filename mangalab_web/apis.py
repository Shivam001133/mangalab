from mangalab_web.models import MenuTitle, MangaCategories
from mangalab_web.serializers import (
    MenuTitleSerializers, MangaCategoriesSerializers
)
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def menu_title(request):
    menu_title = MenuTitle.objects.filter(is_active=True)
    serializer = MenuTitleSerializers(menu_title, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def manga_categories(request):
    manga_categories = MangaCategories.objects.filter(is_active=True)
    serializer = MangaCategoriesSerializers(manga_categories, many=True)
    return Response(serializer.data)
