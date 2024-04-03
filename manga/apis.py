from .models import MangaList, TitleImage, ChapterList
from .serializers import MangaSerializer, ImgSerializer, ChapterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class MangaListApi(APIView):
    def get(self, request, format=None):
        manga_data = MangaList.objects.all()

        latest = request.query_params.get('latest', None)
        treanding = request.query_params.get('treanding', None)
        manga_rank = request.query_params.get('manga_rank', None)

        if latest:
            manga_data = manga_data.filter(latest=True)
        if treanding:
            manga_data = manga_data.filter(treanding=True)
        if manga_rank:
            manga_data = manga_data.filter(manga_rank__gte=manga_rank)

        serializer = MangaSerializer(manga_data, many=True)
        return Response(serializer.data)
