from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


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

    @property
    def read_in_minutes(self) -> int:
        word_count = self.content.split()
        minutes = int(len(word_count) / 250)

        if minutes:
            return minutes

        return 1

    @property
    def get_absolute_url(self):
        return reverse("article_show", kwargs={"article_slug": self.slug})
    


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    published_at = models.DateTimeField(default=datetime.now)