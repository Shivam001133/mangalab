
from django.urls import path
# from rest_framework.authtoken import views
from users import views as uviews

urlpatterns = [
    path('login/', uviews.loginView,
         name='login'),
]
