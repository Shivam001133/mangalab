# urls.py
from django.urls import path
from . import views

app_name = "mangavault"

urlpatterns = [
    path("detail/<int:pk>/", views.manga_detail, name="manga_detail"),
    path("chapter/<int:pk>/", views.manga_read_chapter, name="read_chapter"),
]
