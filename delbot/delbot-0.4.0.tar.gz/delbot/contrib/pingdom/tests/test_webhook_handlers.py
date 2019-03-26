from django.test import TestCase
import json
import os


class WebhookHandlerTests(TestCase):
    path = '/wh/pingdom/'

    def fixture(self, name):
        filename = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    __file__
                )
            ),
            'fixtures',
            'test_pingdom_%s.json' % name
        )

        with open(filename, 'rb') as f:
            return f.read()

    def post(self, fixture):
        response = self.client.generic(
            'POST',
            self.path,
            data=self.fixture(fixture)
        )

        return response, json.loads(response.content.decode('utf-8'))

    def test_down(self):
        response, data = self.post('down')
        self.assertEqual(
            data,
            {
                'created': [
                    ['blog.category', 1],
                    ['blog.tag', 1],
                    ['blog.tag', 2],
                    ['blog.post', 1]
                ],
                'updated': [],
                'deleted': []
            }
        )

    def test_up(self):
        response, data = self.post('up')
        self.assertEqual(
            data,
            {
                'created': [
                    ['blog.category', 1],
                    ['blog.tag', 1],
                    ['blog.tag', 2],
                    ['blog.post', 1]
                ],
                'updated': [],
                'deleted': []
            }
        )
