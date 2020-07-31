from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/create', views.ArticleCreate.as_view(), name='article_create'),
    path('articles/<slug>/edit', views.ArticleEdit.as_view(), name='article_edit'),
    path('articles/search', views.article_search, name='article_search'),
    path('articles/<slug>', views.article_show, name='article_show'),
    path('categories', views.category_index, name='category_index'),
    path('categories/<pk>', views.category_show, name='category_show'),
    path('author/<username>', views.author_show, name='author_show'),
    path('auth/signup', views.Signup.as_view(), name='signup'),
    path('<article_slug>/comment/create/', views.comment_create, name='comment_create')
]