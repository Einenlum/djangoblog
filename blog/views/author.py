from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from blog.models import User


def author_show(request: HttpRequest, username):
    author = get_object_or_404(User, username=username)
    p = Paginator(author.articles.order_by('-published_at'), 2)
    page = request.GET.get('page', 1)

    return render(request, 'author/show.html', {'author': author, 'page': p.get_page(page)})
