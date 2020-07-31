from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from blog.models import Category


def category_index(request: HttpRequest):
    categories = Category.objects.all()
    p = Paginator(categories, 2)
    page = request.GET.get('page', 1)

    return render(request, 'category/index.html', {'page': p.get_page(page)})

def category_show(request: HttpRequest, pk):
    category = get_object_or_404(Category, pk=pk)
    p = Paginator(category.articles.order_by('-published_at'), 2)
    page = request.GET.get('page', 1)

    return render(request, 'category/show.html', {'category': category, 'page': p.get_page(page)})
