from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('vid/<int:uid>', views.vid, name='vid'),
    path('apis/revai/', views.revai_callback, name='revai_callback'),
]