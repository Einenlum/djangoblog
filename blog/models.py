from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify


class User(AbstractUser):
    pass


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    content = models.TextField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    published_at = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    published_at = models.DateTimeField(default=datetime.now)