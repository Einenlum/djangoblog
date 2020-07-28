from django.shortcuts import render, get_object_or_404
from .models import Article

def index(request):
    articles = Article.objects.order_by('-published_at')

    return render(request, 'index.html', {'articles': articles})


def article_show(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    
    return render(request, 'article_show.html', {'article': article})