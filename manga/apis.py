from .models import MangaList
from .serializers import MangaSerializer
from helpers.helper import get_paginated_data
from rest_framework.decorators import api_view
from rest_framework.response import Response


# class MangaListView(APIView):
@api_view(['GET'])
def manga_list(request, *args, **kwargs):
    list_type = request.query_params.get("list_type")
    if list_type == 'trending':
        manga_list = MangaList.objects.filter(treanding=True)
    elif list_type == 'latest':
        manga_list = MangaList.objects.filter(latest=True)
    elif list_type == 'rank':
        manga_list = MangaList.objects.all()
    else:
        return Response({"error": "Invalid list type"}, status=400)

    paginator, paginated_manga_list = get_paginated_data(request, manga_list)
    serializer = MangaSerializer(paginated_manga_list, many=True)

    # response = paginator.get_paginated_response(serializer.data)
    # response.data['isSuccess'] = "Success"

    # return Response(data=response.data, status=status.HTTP_200_OK)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def manga_chapter(request, *args, **kwargs):
    manga_id = request.data.get("manga_id")
    manga = MangaList.objects.get(id=manga_id)
    serializer = MangaSerializer(manga)

    return Response(data=serializer.data, status=200)
