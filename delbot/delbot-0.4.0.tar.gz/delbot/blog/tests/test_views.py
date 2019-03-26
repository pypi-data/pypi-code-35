from django.test import TestCase


class PostListViewTests(TestCase):
    fixtures = ('test_posts',)

    def test_get_index(self):
        response = self.client.get('/')
        self.assertContains(response, '<h1>testserver</h1>')

    def test_get_tag(self):
        response = self.client.get('/tag/porro/')
        self.assertContains(response, '<h1>Porro</h1>')

    def test_get_category(self):
        response = self.client.get('/category/odit-cum/')
        self.assertContains(response, '<h1>Odit cum</h1>')


class PostDetailViewTests(TestCase):
    fixtures = ('test_posts',)

    def test_get(self):
        response = self.client.get('/1/')
        self.assertContains(response, 'Et provident quo')
