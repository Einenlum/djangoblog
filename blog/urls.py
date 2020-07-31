from django.urls import path

from . import views

urlpatterns = [
    path('', views.article.index, name='index'),
    path('articles/create', views.article.ArticleCreate.as_view(), name='article_create'),
    path('articles/<slug>/edit', views.article.ArticleEdit.as_view(), name='article_edit'),
    path('articles/search', views.article.article_search, name='article_search'),
    path('articles/<slug>', views.article.article_show, name='article_show'),
    path('<article_slug>/comment/create/', views.article.comment_create, name='comment_create'),
    path('categories', views.category.category_index, name='category_index'),
    path('categories/<pk>', views.category.category_show, name='category_show'),
    path('author/<username>', views.author.author_show, name='author_show'),
    path('auth/signup', views.Signup.as_view(), name='signup'),
]
