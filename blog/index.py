from .models import Article


from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register


@register(Article)
class ArticleIndex(AlgoliaIndex):
    fields = ['content', 'title']
    settings = {'searchableAttributes': ['content', 'title']}
    index_name = 'articles'