from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<article_slug>', views.article_show, name='article_show'),
]