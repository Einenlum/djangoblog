from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound, HttpRequest
from django.views.defaults import page_not_found
from .models import Article, Category, User

def index(request: HttpRequest):
    articles = Article.objects.order_by('-published_at')
    p = Paginator(articles, 2)
    page = request.GET.get('page', 1)

    return render(request, 'index.html', {'page': p.get_page(page)})

def article_show(request: HttpRequest, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    
    return render(request, 'article_show.html', {'article': article})

def category_index(request: HttpRequest):
    categories = Category.objects.all()
    p = Paginator(categories, 2)
    page = request.GET.get('page', 1)

    return render(request, 'category_index.html', {'page': p.get_page(page)})

def category_show(request: HttpRequest, pk):
    category = get_object_or_404(Category, pk=pk)
    p = Paginator(category.articles.all(), 2)
    page = request.GET.get('page', 1)

    return render(request, 'category_show.html', {'category': category, 'page': p.get_page(page)})

def author_show(request: HttpRequest, username):
    author = get_object_or_404(User, username=username)
    p = Paginator(author.articles.all(), 2)
    page = request.GET.get('page', 1)

    return render(request, 'author_show.html', {'author': author, 'page': p.get_page(page)})

def handler404(request: HttpRequest, exception, template_name="error_404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response