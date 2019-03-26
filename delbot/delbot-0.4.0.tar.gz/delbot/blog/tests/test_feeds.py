from django.test import TestCase
from feedparser import parse


class PostListFeedTests(TestCase):
    fixtures = ('test_posts',)

    def test_get_index(self):
        response = self.client.get('/feed/')
        feed = parse(response.content.decode('utf-8'))
        self.assertEqual(feed.feed.title, 'Notes')
        self.assertEqual(len(feed.entries), 10)

    def test_get_tag(self):
        response = self.client.get('/tag/porro/feed/')
        feed = parse(response.content)
        self.assertEqual(feed.feed.title, 'Porro')

    def test_get_category(self):
        response = self.client.get('/category/odit-cum/feed/')
        feed = parse(response.content)
        self.assertEqual(feed.feed.title, 'Odit cum')


class PostDetailFeedTests(TestCase):
    fixtures = ('test_posts',)

    def test_get(self):
        response = self.client.get('/1/feed/')
        feed = parse(response.content)
        self.assertEqual(feed.feed.title, 'Et provident quo')
        self.assertEqual(len(feed.entries), 1)
