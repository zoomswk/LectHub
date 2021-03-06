from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('vid/<int:id>/', views.vid, name='vid'),
    path('vid/<int:id>/th/', views.vid_th, name='vid_th'),
    path('vid/<int:id>/update/', views.update, name='update'),
    path('browse/', views.browse, name='browse'),
    path('faq/', views.faq, name='faq'),
    path('apis/revai/', views.revai_callback, name='revai_callback'),
]
