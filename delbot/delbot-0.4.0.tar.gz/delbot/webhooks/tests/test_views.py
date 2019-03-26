from django.test import TestCase
import json


class ReceiverViewTests(TestCase):
    def test_post_404(self):
        response = self.client.post(
            '/wh/test/',
            data={
                'title': 'Title',
                'tags': ('tag',)
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_post_gitlab_invalid(self):
        response = self.client.generic(
            'POST',
            '/wh/gitlab/',
            data=(
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<xml><title>Title</title><tag>tag</tag></xml>'
            )
        )

        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            json_response,
            {
                'status': 400,
                'title': 'Bad Request',
                'detail': 'Malformed JSON data'
            }
        )

    def test_post_gitlab_success(self):
        response = self.client.generic(
            'POST',
            '/wh/gitlab/',
            data=json.dumps({})
        )

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            json_response,
            {
                'created': [],
                'deleted': [],
                'updated': []
            }
        )
