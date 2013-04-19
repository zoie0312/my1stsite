from django.test import TestCase
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from ..models import *


class InfoholicTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.category = Category.objects.create(
            name='test_Cat'
            )
        self.category.owners.add(self.user)
        self.feed = Feed.objects.create(
            title='test_Feed',
            category=self.category
            )
        self.feed.owners.add(self.user)
   
    def create_article(self):
        return Article.objects.create(
            title='test article',
            content='for testing purpose',
            link='http://test.html',
            reader=self.user,
            category=self.category,
            source=self.feed
            )

    def test_article_creation(self):
        article = self.create_article()
        self.assertTrue(isinstance(article, Article))
        self.assertEqual(article.__unicode__(), article.title)
        self.assertEqual(article.slug, slugify(article.link))
        
    def test_category_creation(self):
        category = Category.objects.create(name='test_Cat')
        category.owners.add(self.user)
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__unicode__(), category.name)
        self.assertEqual(category.slug_name, slugify(category.name))

    def test_feed_creation(self):
        feed = Feed.objects.create(
            title='test_feed',
            category=self.category
            )
        feed.owners.add(self.user)
        self.assertTrue(isinstance(feed, Feed))
        self.assertEqual(feed.__unicode__(), feed.title)
        self.assertEqual(feed.slug, slugify(feed.title))

    def test_article_custom_slug(self):
        article = Article.objects.create(
            title='test',
            slug='fizza',
            reader=self.user,
            category=self.category,
            source=self.feed
            )
        self.assertNotEqual(article.slug, slugify(article.title))
        self.assertEqual(article.slug, 'fizza')

    def test_category_custom_slug(self):
        category = Category.objects.create(
            name='test',
            slug_name='fizza',
            
            )
        self.assertNotEqual(category.slug_name, slugify(category.name))
        self.assertEqual(category.slug_name, 'fizza')
        
    def test_feed_custom_slug(self):
        feed = Feed.objects.create(
            title='test',
            slug='fizza',
            category=self.category,
            )
        self.assertNotEqual(feed.slug, slugify(feed.title))
        self.assertEqual(feed.slug, 'fizza')
	
