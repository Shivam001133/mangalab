# urls.py
from django.urls import path
from . import views

app_name = "mangavault"

urlpatterns = [
    path("manga/<int:pk>/", views.manga_detail, name="manga_detail"),
]
