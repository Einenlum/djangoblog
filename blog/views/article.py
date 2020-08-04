from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, Case, When, Value
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from algoliasearch_django import raw_search

from blog.models import Article, Comment


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
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        

        return super().form_valid(form)
        #return redirect(article.get_absolute_url())


def article_search(request):
    query = request.GET.get('query', '')
    response = raw_search(Article, query)
    ids = [article['objectID'] for article in response['hits']]
    # Allow to get the articles in the specific sequence of ids we gave, thanks to case when id = x then pos=1…
    whens = Case(*[When(id=id, then=Value(pos)) for (pos, id) in enumerate(ids)])

    # We prefer to have real django orm objects instead of algolia objects, to be able to use the paginator
    articles = Article.objects.filter(id__in=ids).order_by(whens)
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
