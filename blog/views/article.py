from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from pprint import pprint

from blog.models import Article


def index(request: HttpRequest):
    articles = Article.objects.order_by('-published_at')
    p = Paginator(articles, 2)
    page = request.GET.get('page', 1)

    return render(request, 'article/index.html', {'page': p.get_page(page)})

def article_show(request: HttpRequest, slug):
    article = get_object_or_404(Article, slug=slug)
    
    return render(request, 'article/show.html', {'article': article})


class ArticleCreate(LoginRequiredMixin, generic.CreateView):
    model = Article
    fields = ('title', 'content', 'cover', 'categories')
    template_name = 'article/create.html'

    def form_valid(self, form):
        pprint(form)
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        

        return super().form_valid(form)
        #return redirect(article.get_absolute_url())


def article_search(request):
    query = request.GET.get('query', '')
    articles = Article.objects.filter(Q(title__icontains=query)|Q(content__icontains=query)).order_by('-published_at')
    p = Paginator(articles, 4)
    page = request.GET.get('page', 1)

    return render(request, 'article/search.html', {'page': p.get_page(page), 'query': query})

class ArticleEdit(LoginRequiredMixin, generic.UpdateView):
    model = Article
    fields = ('title', 'content', 'cover', 'categories')
    template_name = 'article/edit.html'

    def get(self, *args, **kwargs):
        # super().get populates the article in the self.object attribute
        template_response = super(generic.UpdateView, self).get(*args, **kwargs)
        if self.object.author != self.request.user:
            raise PermissionDenied()

        return template_response


@login_required
def comment_create(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    comment = Comment.create(request.user, article, request.POST.get('comment_content'))
    comment.save()

    return redirect(article.get_absolute_url())
