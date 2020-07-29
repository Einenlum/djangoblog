from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound, HttpRequest
from django.urls import reverse_lazy
from django.views.defaults import page_not_found
from django.views import generic
from .models import Article, Category, User
from .forms import CustomUserCreationForm

def index(request: HttpRequest):
    articles = Article.objects.order_by('-published_at')
    p = Paginator(articles, 2)
    page = request.GET.get('page', 1)

    return render(request, 'index.html', {'page': p.get_page(page)})

def article_show(request: HttpRequest, slug):
    article = get_object_or_404(Article, slug=slug)
    
    return render(request, 'article_show.html', {'article': article})

def category_index(request: HttpRequest):
    categories = Category.objects.all()
    p = Paginator(categories, 2)
    page = request.GET.get('page', 1)

    return render(request, 'category_index.html', {'page': p.get_page(page)})

def category_show(request: HttpRequest, pk):
    category = get_object_or_404(Category, pk=pk)
    p = Paginator(category.articles.order_by('-published_at'), 2)
    page = request.GET.get('page', 1)

    return render(request, 'category_show.html', {'category': category, 'page': p.get_page(page)})

def author_show(request: HttpRequest, username):
    author = get_object_or_404(User, username=username)
    p = Paginator(author.articles.order_by('-published_at'), 2)
    page = request.GET.get('page', 1)

    return render(request, 'author_show.html', {'author': author, 'page': p.get_page(page)})

def handler404(request: HttpRequest, exception, template_name="error_404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


class ArticleCreate(LoginRequiredMixin, generic.CreateView):
    model = Article
    fields = ('title', 'content', 'categories')
    template_name = 'article_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()

        return redirect(article.get_absolute_url)


class ArticleEdit(LoginRequiredMixin, generic.UpdateView):
    model = Article
    fields = ('title', 'content', 'categories')
    template_name = 'article_edit.html'

    def get(self, *args, **kwargs):
        # super().get populates the article in the self.object attribute
        template_response = super(generic.UpdateView, self).get(*args, **kwargs)
        if self.object.author != self.request.user:
            raise PermissionDenied()

        return template_response


class Signup(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'