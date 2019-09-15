from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('vid/<int:id>/', views.vid, name='vid'),
    path('vid/<int:id>/update/', views.update, name='update'),
    path('browse/', views.browse, name='browse'),
    path('apis/revai/', views.revai_callback, name='revai_callback'),
]
