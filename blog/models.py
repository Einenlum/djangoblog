from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class User(AbstractUser):
    username = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def get_author_absolute_url(self):
        return reverse("author_show", kwargs={"username": self.username})

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_show", kwargs={"pk": self.pk})
    


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    content = models.TextField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    published_at = models.DateTimeField(default=datetime.now)
    categories = models.ManyToManyField(Category, related_name='articles', blank=True)

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

    def get_absolute_url(self):
        return reverse("article_show", kwargs={"slug": self.slug})
    


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    published_at = models.DateTimeField(default=datetime.now)