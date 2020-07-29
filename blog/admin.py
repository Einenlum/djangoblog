from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Article, Category, Comment, User


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'author', 'slug')
    exclude = ('published_at', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'published_at', 'article', 'content')
    

admin.site.register(User, UserAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)