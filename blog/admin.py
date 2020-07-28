from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Article, User


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'published_at', 'title', 'slug')
    exclude = ('published_at', 'slug')
    

admin.site.register(User, UserAdmin)
admin.site.register(Article, ArticleAdmin)