from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/<article_slug>', views.article_show, name='article_show'),
    path('categories', views.category_index, name='category_index'),
    path('categories/<pk>', views.category_show, name='category_show'),
]