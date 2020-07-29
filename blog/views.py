from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.views.defaults import page_not_found
from .models import Article

def index(request):
    articles = Article.objects.order_by('-published_at')

    return render(request, 'index.html', {'articles': articles})

def article_show(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    
    return render(request, 'article_show.html', {'article': article})

def handler404(request, exception, template_name="error_404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response