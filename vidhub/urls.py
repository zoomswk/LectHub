from django.urls import path

from . import views
from . import upload

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/',upload.index, name='upload')
]