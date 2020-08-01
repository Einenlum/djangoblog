from django.test import TestCase
from django.urls import resolve, reverse

from .models import Article, Category, User
from .views.category import category_show


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
    
    def test_article_in_authors_list(self):
        robert = create_user('robert', 'robert@email.com', 'LoremIpsum78')
        mitchell = create_user('mitchell', 'mitchell@email.com', 'IL0veY0u77')
        article = create_article(robert, 'How to program', 'Some content')

        robert_response = self.client.get(reverse('author_show', kwargs={'username': robert.username}))
        self.assertEqual(robert_response.status_code, 200)
        self.assertContains(robert_response, "How to program")
        self.assertContains(robert_response, "Some content")

        mitchell_response = self.client.get(reverse('author_show', kwargs={'username': mitchell.username}))
        self.assertEqual(mitchell_response.status_code, 200)
        self.assertNotContains(mitchell_response, "How to program")
        self.assertContains(mitchell_response, "No article here for now.")

    def test_article_search(self):
        robert = create_user('robert', 'robert@email.com', 'LoremIpsum78')
        article_1 = create_article(robert, 'How to program', 'Some content')
        article_2 = create_article(robert, 'How to cook', 'Some content')

        response = self.client.get(reverse('article_search') + '?query=cook')
        self.assertContains(response, 'cook')
        self.assertNotContains(response, 'program')


class SecurityTest(TestCase):
    def test_signup_page_shows_up(self):
        with self.settings(DISABLE_SIGNUP=False):
            response = self.client.get(reverse('signup'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Sign up')

    def test__signup_is_disabled(self):
        with self.settings(DISABLE_SIGNUP=True):
            response = self.client.get(reverse('signup'))

            self.assertEqual(response.status_code, 403)