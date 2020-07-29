from django.test import TestCase
from django.urls import reverse, resolve
from .models import Article, Category, User
from .views import category_show

def create_user(username, email, password):
    return User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

def create_category(name):
    return Category.objects.create(name=name)

def create_article(author, title, content, categories = []):
    article = Article.objects.create(
        author=author,
        title=title,
        content=content
    )
    if categories:
        article.categories.set(categories)
        article.save()

    return article

class ArticleIndexViewTest(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No article here for now.")

    def test_one_article(self):
        robert = create_user('robert', 'robert@email.com', 'LoremIpsum78')
        create_article(robert, 'First article', 'Some content')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First article")
        self.assertContains(response, "Some content")

    def test_article_in_category(self):
        music_category = create_category('music')
        programming_category = create_category('programming')
        robert = create_user('robert', 'robert@email.com', 'LoremIpsum78')
        article = create_article(robert, 'How to program', 'Some content', [programming_category])

        programming_response = self.client.get(reverse('category_show', kwargs={'pk': programming_category.id}))
        self.assertEqual(programming_response.status_code, 200)
        self.assertContains(programming_response, "How to program")
        self.assertContains(programming_response, "Some content")

        music_response = self.client.get(reverse('category_show', kwargs={'pk': music_category.id}))
        self.assertEqual(music_response.status_code, 200)
        self.assertContains(music_response, "No article here for now.")